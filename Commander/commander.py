import asyncio
from asyncio import StreamReader, StreamWriter
from asyncio.queues import Queue
# from connUtils import recv_msg, send_msg

ETX = b'\x03'


class Server:
	def __init__(self):
		self.queue = Queue()

	async def handle_piano(self, reader: StreamReader, writer: StreamWriter):

		while True:
			# message = await recv_msg(reader)
			data = await reader.readuntil(ETX)
			message = data[0:-len(ETX)].decode()
			addr = writer.get_extra_info('peername')

			print(f'Received: {addr}')

			if not self.queue.empty():
				message += await self.queue.get()
			else:
				message += "moo"

			await self.queue.put(message)

			# await send_msg(writer, message)
			data = message.encode()
			writer.write(data+ETX+data)
			await writer.drain()

		print("Close the connection")
		writer.close()

	async def run(self):
		server = await asyncio.start_server(self.handle_piano, '127.0.0.1', 8888)

		addr = server.sockets[0].getsockname()
		print(f'Serving on {addr}')

		async with server:
			await server.serve_forever()


def main():
	server = Server()
	asyncio.run(server.run())


if __name__ == "__main__":
	main()
