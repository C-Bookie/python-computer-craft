import numpy as np
from .unit import Unit
import computercraft.errors

async def dig(api):
	unit = Unit(api)
	dim = np.array([10, 5, 10])

	await api.print('Digging begun')
	for y in range(dim[1]):
		for z in range(dim[2]):
			for x in range(dim[0]):
				await unit.go_to([x, -y+1, z])
				try:
					await api.turtle.digDown()
				except computercraft.errors.CommandException:
					continue


