import asyncio
from coms import Client
# from computercraft.server import CCAPI
# from subapis.peripheral import CCTSpeaker


class Piano(Client):
	# speaker: CCTSpeaker

	def __init__(self, api):
		super().__init__("Speaker")
		self.api = api

		self.white_list_functions += [
			"note"
		]

	async def run(self):
		await self.connect()
		await self.request("subscribe", "piano")
		self.speaker = await self.api.peripheral.wrap("bottom")
		await asyncio.gather(
			super().run(),
			# self.loop()
		)

	async def note(self, msg, state):
		if state:
			note = msg - 43
			# await self.api.print(note)
			await self.speaker.playNote("guitar", 3, note)


async def servant(api):
	print("New unit registering")
	await api.print("Connecting...")
	piano = Piano(api)
	print("New unit online")

	await piano.run()

# wget http://95.148.187.63:8080 startup