
from caduceussocket.connection import Client

class Turtle(Client):
	def __init__(self):
		super().__init__()


async def servant(api):
	print("moo")
	await api.print("moo")
	print("moo2")


