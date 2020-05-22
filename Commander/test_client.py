import asyncio
# from connUtils import recv_msg, send_msg


class Radio:
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter

    def __init__(self):
        self.white_list_functions = [
            "print"
        ]

    ETX = b'\x03'

    async def write(self, message):
        data = message.encode()
        self.writer.write(data + self.ETX)
        await self.writer.drain()

    async def read(self):
        data = await self.reader.readuntil(self.ETX)
        message = data[0:-len(self.ETX)].decode()
        return message

    # asyncio.run(radio.client())
    async def client(self):
        self.reader, self.writer = await asyncio.open_connection('127.0.0.1', 8888)

        while True:
            response = await self.read()

            if "type" in response and response["type"] in self.white_list_functions:
                function = getattr(self, response["type"])
                if "args" in response and response["args"] is not None:
                    function(*response["args"])
                else:
                    function()
            else:
                print("Request unrecognised by server: " + str(response))

        await asyncio.gather(
            tcp_echo_client(),
            task2(queue)
        )
        writer.close()

    # asyncio.run(radio.host())
    def host(self):
        server = await asyncio.start_server(self.host_handler, '127.0.0.1', 8888)

        # addr = server.sockets[0].getsockname()
        # print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()

    def print(self, message):
        print(message)
        self.write(message)

    async def host_handler(self):
        pass


if __name__ == "__main__":
    radio = Radio()
    asyncio.run(radio.run())
