import websockets
import threading
import asyncio
import queue
import json

class NetworkHander:
    def __init__(self, websocketURL: str, master):
        self.wsURL = "ws://localhost:8000"
        self.master = master

        self.queueIncoming = queue.Queue()
        self.queueOutgoing = queue.Queue()

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.master.after(100, self.proccessIncoming)


    def sendAction(self, action: dict):
        self.queueOutgoing.put(json.dumps(action))

    async def reciever(self, websocket: websockets.ClientConnection):
        while True:
            message = await websocket.recv()
            self.queueIncoming.put(message) 

    async def sender(self, websocket: websockets.ClientConnection):
        while True:
            message = await asyncio.to_thread(self.queueOutgoing.get)
            await websocket.send(message)

    async def wsHander(self):
        async with websockets.connect(self.wsURL) as websocket:
            while True:
                await asyncio.gather(self.sender(websocket), self.reciever(websocket))                

    def proccessIncoming(self):
        while not self.queueIncoming.empty():
            data: dict = json.loads(self.queueIncoming.get())
            self.master.action(data)

        self.master.after(100, self.proccessIncoming)

    def startAsyncIoLoop(self):
        self.loop.run_until_complete(self.wsHander())

    def run(self):
        self.wsThread = threading.Thread(target = self.run, daemon=True)
        self.wsThread.start()
        