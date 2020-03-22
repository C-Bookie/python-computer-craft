import numpy as np
import computercraft.errors


class Unit:
	left = np.array([
		[0, 0, 1],
		[0, 1, 0],
		[-1, 0, 0]
	])

	right = np.array([
		[0, 0, -1],
		[0, 1, 0],
		[1, 0, 0]
	])

	def __init__(self, api):
		self.api = api
		self.cods = np.array([0, 0, 0])
		self.dire = np.array([1, 0, 0])

	async def go_to(self, new_cods):
		if self.cods[0] != new_cods[0]:  # X
			if self.cods[0] < new_cods[0]:
				await self.face([1, 0, 0])
			else:
				await self.face([-1, 0, 0])
			for _ in range(abs(self.cods[0] - new_cods[0])):
				await self.forward()

		if self.cods[2] != new_cods[2]:  # Z
			if self.cods[2] < new_cods[2]:
				await self.face([0, 0, 1])
			else:
				await self.face([0, 0, -1])
			for x in range(abs(self.cods[2] - new_cods[2])):
				await self.forward()

		if self.cods[1] != new_cods[1]:  # Y
			asce = self.cods[1] < new_cods[1]
			for _ in range(abs(self.cods[1] - new_cods[1])):
				if asce:
					await self.up()
				else:
					await self.down()

	async def forward(self):
		await self.fuel_check()
		while True:
			try:
				await self.api.turtle.forward()
				break
			except computercraft.errors.CommandException:
				await self.api.turtle.dig()
		self.cods += self.dire

	async def up(self):
		await self.fuel_check()
		while True:
			try:
				await self.api.turtle.up()
				break
			except computercraft.errors.CommandException:
				await self.api.turtle.digup()
		self.cods += [0, 1, 0]

	async def down(self):
		await self.fuel_check()
		while True:
			try:
				await self.api.turtle.down()
				break
			except computercraft.errors.CommandException:
				await self.api.turtle.digDown()
		self.cods += [0, -1, 0]

	async def fuel_check(self):
		level = await self.api.turtle.getFuelLevel()
		if level == 0:
			for i in range(1, 17):
				await self.api.turtle.select(i)
				try:
					await self.api.turtle.refuel()
					return
				except computercraft.errors.CommandException:
					continue
			self.api.print("Fuel depleted")

	async def face(self, new_dire):
		new_dire = np.array(new_dire)
		while not (self.dire == new_dire).all():
			await self.api.turtle.turnRight()
			self.dire = self.dire @ self.right
