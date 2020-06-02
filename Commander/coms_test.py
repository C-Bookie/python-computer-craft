import asyncio
import unittest

from coms import Host, Client


class Marko(Client):
	def __init__(self):
		super().__init__()
		self.white_list_functions += [
			"echo",
			"pass_along",
			"add"
		]

		self.i = 1

	async def echo(self, message):
		await self.broadcast("test", "print", message)

	async def pass_along(self, tag):
		await self.broadcast(tag, "add", self.i)

	async def add(self, n):
		self.i += n


class MyTestCase(unittest.TestCase):
	host = Host()
	client1 = Marko()
	client2 = Marko()

	ready = False

	async def run_clients(self, callback):
		async def setup():
			await asyncio.gather(
				self.client1.connect(),
				self.client2.connect()
			)
			await asyncio.gather(
				self.client1.request("subscribe", "client1"),
				self.client2.request("subscribe", "client2")
			)
			await asyncio.gather(
				self.client1.run(),
				self.client2.run(),
				callback()
			)
		# await asyncio.gather(
		await self.host.run(),
		await setup()
		# )

	def test_something(self):
		async def broadcast_test():
			await self.client1.broadcast("client2", "pass_along", "client1")
			await self.client1.pass_along("client2")
			await self.client2.pass_along("client1")

			await asyncio.sleep(1)

			await self.host.close()


			print("rsdkyrxdr")

		asyncio.run(self.run_clients(broadcast_test))

		self.assertEqual(3, self.client1.i)
		self.assertEqual(2, self.client2.i)


if __name__ == '__main__':
	unittest.main()
