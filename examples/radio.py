from caduceussocket.connection import Client
import asyncio


class Radio(Client):
    def __init__(self):
        super().__init__()
        self.queue = asyncio.Queue()

        self.white_list_functions += [
            "print"
        ]

    def connect(self):
        super().connect()
        self.send_data({
            "type": "register",
            "args": [
                "turtle",
                "test1"
            ]
        })
        self.toServer({"type": "newScreen"})

    async def producer(self, item):
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # loop.run_until_complete(self.queue.put(item))
        await self.queue.put(item)

    async def consumer(self):
        return await self.queue.get()

    def toServer(self, msg):
        self.send_data({
            "type": "broadcast",
            "args": [
                msg,
                "server"
            ]
        })
