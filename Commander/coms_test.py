import asyncio
import unittest

from coms import Host, Client


class Marko(Client):
	def __init__(self):
		super().__init__()
		self.white_list_functions += [
			"echo",
			"print"
		]

	async def echo(self, message):
		print(message)
		await self.broadcast("test1", "print", message)

	async def print(self, message):
		print(message)


class MyTestCase(unittest.TestCase):
	def test_something(self):
		host = Host()
		client1 = Marko()
		client2 = Marko()


		async def run_clients():
			await asyncio.gather(
				client1.connect(),
				client2.connect()
			)
			await asyncio.gather(
				client1.request("subscribe", "test1"),
				client2.request("subscribe", "test2")
			)
			await asyncio.gather(
				client1.run(),
				client2.run(),
				client2.broadcast("test1", "print", "moo")
			)

		async def run():
			await asyncio.gather(
				host.run(),
				run_clients()
			)

		asyncio.run(run())


if __name__ == '__main__':
	unittest.main()
