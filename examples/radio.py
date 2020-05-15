from caduceussocket.connection import Client
import asyncio


class Radio(Client):
    def __init__(self, api):
        super().__init__()
        self.api = api

        self.msg = "null"

        self.white_list_functions += [
            "producer"
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

    def producer(self, msg):
        self.msg = msg

    def toServer(self, msg):
        self.send_data({
            "type": "broadcast",
            "args": [
                msg,
                "server"
            ]
        })
