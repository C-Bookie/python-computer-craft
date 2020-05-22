import asyncio
from coms import Client


class Piano(Client):
	def __init__(self, api):
		super().__init__()
		self.api = api

		self.white_list_functions += [
			"note"
		]

		self.speaker = await self.api.peripheral.wrap("bottom")

	async def run(self):
		await self.connect()
		await self.send({
			"type": "subscribe",
			"args": [
				"piano"
			]
		})
		await asyncio.gather(
			super().run(),
			# self.loop()
		)

	def note(self, note, state):
		if state:
			await self.api.print(note)
			await self.speaker.playNote("guitar", 3, note)
		else:
			self.msg = False


async def servant(api):

	print("New unit registering")
	await api.print("Connecting...")
	piano = Piano(api)
	reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
	print("New unit online")

	while True:
		msg = await reader.read()
		# radio.loop()  # fixme non async function socket.socket(socket.AF_INET, socket.SOCK_STREAM).accept().recv()
		# msg = radio.msg
		if msg != False:
			note = msg -43
			await api.print(note)
			await self.speaker.playNote("guitar", 3, note)

	writer.close()
