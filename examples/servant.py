import asyncio
from caduceussocket.connection import Client


class Radio(Client):
	def __init__(self, api):
		super().__init__()
		self.api = api

		self.msg = "null"

		self.white_list_functions += [
			"note"
		]

	def connect(self):
		super().connect()
		self.send_data({
			"type": "register",
			"args": [
				"piano",
				"2077"
			]
		})

	def note(self, msg, state):
		if state:
			self.msg = msg
		else:
			self.msg = False

		# def toServer(self, msg):
	#     self.send_data({
	#         "type": "broadcast",
	#         "args": [
	#             msg,
	#             "server"
	#         ]
	#     })


async def servant(api):
	speaker = await api.peripheral.wrap("bottom")

	print("New unit registering")
	await api.print("Connecting...")
	radio = Radio(api)
	print("New unit online")

	while True:
		radio.loop()  # fixme non async function socket.socket(socket.AF_INET, socket.SOCK_STREAM).accept().recv()
		msg = radio.msg
		if msg != False:
			note = msg -43
			await api.print(note)
			await speaker.playNote("guitar", 3, note)
