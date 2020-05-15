import asyncio

from .unit import Unit
from .radio import Radio


async def servant(api):
	print("New unit registering")
	await api.print("Connecting...")
	radio = Radio(api)
	print("New unit online")

	while True:
		radio.loop()
		await api.print(radio.msg)
		await asyncio.sleep(1)



