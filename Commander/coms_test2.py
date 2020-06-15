import unittest

import asyncio
from coms import Client


class MidiPiano(Client):
	def __init__(self, name):
		super().__init__(name)
		self.step_up = 0

	async def run(self):
		await self.connect()
		await self.request("subscribe", "keyboard")
		await asyncio.gather(
			super().run(),
			self.loop()
		)

	async def loop(self):
		asyncio.current_task().set_name(self.__name__ + "-Transmitter")
		while True:
			await asyncio.sleep(0)  # todo review



class MyTestCase(unittest.TestCase):
	def test_something(self):
		piano = MidiPiano("Piano")
		asyncio.run(piano.run())
		self.assertEqual(True, False)


if __name__ == '__main__':
	unittest.main()
