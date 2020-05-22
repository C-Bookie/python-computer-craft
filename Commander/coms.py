import asyncio
import json

ETX = b'\x03'
ETX_LEN = len(ETX)


class Radio:
	def __init__(self, reader, writer):
		self.reader = reader
		self.writer = writer

	async def send(self, message):
		data = message.encode()
		self.writer.write(data + ETX)
		await self.writer.drain()

	async def receive(self):
		data = await self.reader.readuntil(ETX)
		message = data[0:-ETX_LEN].decode()
		return message


class Responder(Radio):
	def __init__(self, reader, writer):
		super().__init__(reader, writer)

		self.white_list_functions = []

	async def callback(self, response):
		if "type" in response and response["type"] in self.white_list_functions:
			function = getattr(self, response["type"])
			if "args" in response and response["args"] is not None:
				args = response["args"]
			else:
				args = ()
			await function(*args)
		else:
			print("Request unrecognised by server: " + str(response))

	async def send(self, data):
		def set_default(obj):
			if isinstance(obj, set):
				return list(obj)
			return obj.list()

		# raise TypeError
		message = json.dumps(data, default=set_default)
		await super().send(message)

	async def receive(self):
		message = await super().receive()
		return json.loads(message)

	async def run(self):
		try:
			while True:
				message = await self.receive()
				await self.callback(message)
		finally:
			self.writer.close()
			self.reader, self.writer = None, None


class Client(Responder):
	def __init__(self, addr='127.0.0.1', port=8888):
		super().__init__(None, None)
		self.addr = addr
		self.port = port

		self.white_list_functions = []

	# asyncio.run(client.client())
	async def connect(self):
		self.reader, self.writer = await asyncio.open_connection('127.0.0.1', 8888)

	async def request(self, function, *args):
		await self.send({
			"type": function,
			"args": args
		})

	async def broadcast(self, tag, function, *args):
		await self.request("broadcast", {
					"type": function,
					"args": args
				},
				tag
		)


class Node(Responder):
	def __init__(self, host, reader, writer):
		super().__init__(reader, writer)
		self.host = host

		self.subscriptions = {"all"}
		self.white_list_functions += [
			"subscribe",
			"broadcast"
		]

	async def subscribe(self, tag):
		self.subscriptions.add(tag)

	async def broadcast(self, message, tag):
		for node in self.host.connections:
			if tag in node.subscriptions:  # todo change to channels containing Nodes to avoid for loops
				await node.send(message)


class Host:
	def __init__(self):
		super().__init__()
		self.connections = []

	async def handler(self, reader, writer):
		node = Node(self, reader, writer)
		self.connections.append(node)
		try:
			await node.run()
		finally:
			self.connections.remove(node)

	# asyncio.run(radio.host())
	async def run(self):
		server = await asyncio.start_server(self.handler, '127.0.0.1', 8888)

		async with server:
			await server.serve_forever()


def main():
	host = Host()
	asyncio.run(host.run())


if __name__ == "__main__":
	main()
