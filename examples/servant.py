import asyncio

from .unit import Unit
from .radio import Radio


async def servant(api):
	print("New unit registering")
	await api.print("Connecting...")
	radio = Radio()
	radio.start()
	print("New unit online")

	# unit = Unit(api)

	await asyncio.sleep(3)

	while True:
		print("consume")
		radio.loop()
		# cmd = await radio.consumer()
		cmd = await radio.queue.get()
		await api.print(cmd)



