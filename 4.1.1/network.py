from os import _exit
import websockets
import threading
import asyncio
import queue
import json

class NetworkHandler:
    def __init__(self, websocketURL: str, master):
        self.wsURL = websocketURL
        self.master = master

        self.queueIncoming = queue.Queue()
        self.queueOutgoing = queue.Queue()

        self.master.after(100, self.processIncoming)

    def sendAction(self, action: dict):
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
        try:
            async with websockets.connect(self.wsURL) as websocket:
                self.websocket = websocket

                await asyncio.gather(
                    self.sender(websocket),
                    self.receiver(websocket)
                )
        
        except OSError as error:
            print(f"Network error: {error}") 

    def processIncoming(self):
        while not self.queueIncoming.empty():
            data: dict = json.loads(self.queueIncoming.get())
            print(data)
            self.master.runAction(data)

        self.master.after(100, self.processIncoming)

    def runWsHandler(self):
        self.asyncioLoop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.asyncioLoop)

        self.asyncioLoop.run_until_complete(
            self.wsHander()
        )

    def stop(self):
        if hasattr(self, "websocket"):
            self.asyncioLoop.call_soon_threadsafe( 
                lambda: asyncio.create_task(
                    self.websocket.close(code = 1000, reason = "Application Closed")
                )
            )

        _exit(0)


    def run(self):
        self.wsThread = threading.Thread(
            target = self.runWsHandler,
            daemon = True
        )

        self.wsThread.start()
        