from os import _exit
import websockets
import threading
import asyncio
from tkinter import messagebox
import queue
import json

class NetworkHandler:
    def __init__(self, master, websocketURL: str):
        self.wsURL: str = websocketURL
        self.master = master

        self.running: bool = False

        self.queueIncoming = queue.Queue()
        self.queueOutgoing = queue.Queue()

        self.master.after(100, self.processIncoming)

    def sendAction(self, action: dict):
        if self.running:
            self.queueOutgoing.put(json.dumps(action))

    async def receiver(self, websocket: websockets.ClientConnection):
        try:
            while True:
                message = await websocket.recv()
                self.queueIncoming.put(message) 

        except websockets.ConnectionClosed:
            print("Disconnecting")

    async def sender(self, websocket: websockets.ClientConnection):
        try:
            while True:
                message = await asyncio.to_thread(self.queueOutgoing.get)
                await websocket.send(message)
        
        except websockets.ConnectionClosed:
            print("Disconnecting")

    async def wsHander(self):
        for attempt in range(10):
            try:
                async with websockets.connect(self.wsURL) as websocket:
                    self.websocket = websocket

                    await asyncio.gather(
                        self.sender(websocket),
                        self.receiver(websocket)
                    )
                    return  

            except OSError as error:
                print(f"Retry {attempt}: {error}")
                await asyncio.sleep(3)

        self.master.after(0, lambda: messagebox.showerror(
            "Connection Error",
            f"Failed to connect after retries:\n{self.wsURL}"
        ))    


    def processIncoming(self):
        while not self.queueIncoming.empty():
            data: dict = json.loads(self.queueIncoming.get())
            self.master.runAction(data)

        self.master.after(100, self.processIncoming)

    def runWsHandler(self):
        self.asyncioLoop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.asyncioLoop)

        self.asyncioLoop.run_until_complete(
            self.wsHander()
        )

    def stop(self):
        if self.running:
            if hasattr(self, "websocket"):
                self.asyncioLoop.call_soon_threadsafe( 
                    lambda: asyncio.create_task(
                        self.websocket.close(code = 1000, reason = "Application Closed")
                    )
                )

            _exit(0)

    def run(self):
        self.running = True

        self.wsThread = threading.Thread(
            target = self.runWsHandler,
            daemon = True
        )

        self.wsThread.start()
        