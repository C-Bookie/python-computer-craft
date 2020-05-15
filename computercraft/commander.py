import computercraft.server as server

from caduceussocket.session import SessionManager
from caduceussocket.connection import Client

# import mido

import asyncio


class Piano(Client):
	def __init__(self):
		super().__init__()
		# print(mido.get_output_names())
		# self.midiPort = mido.open_input("moo 1")

	def connect(self):
		super().connect()
		self.send_data({
			"type": "register",
			"args": [
				"server",
				"test1"
			]
		})

	def run(self):
		while True:
			self.send_command("moo")

			loop = asyncio.new_event_loop()
			asyncio.set_event_loop(loop)
			loop.run_until_complete(asyncio.sleep(1))

	def send_command(self, cmd):
		self.send_data({
			"type": "broadcast",
			"args": [
				{
					"type": "producer",
					"args": [
						cmd
					]
				},
				"turtle"
			]
		})


def run():
	sm: SessionManager = SessionManager()
	sm.start()
	# server.main()
	piano: Piano = Piano()
	piano.run()


if __name__ == "__main__":
	# print(mido.get_output_names())
	run()


# wget http://95.148.187.63:8080/ startup


