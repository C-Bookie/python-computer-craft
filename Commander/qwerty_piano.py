import asyncio

import pygame
import pygame.midi

import mido

from coms import Client


deadzone = 0.1


def correctJoy(n):
	if n < deadzone and n > -deadzone:
		return 0
	if n < 0:
		return -n**2
	return n**2


class JoyManager:
	def __init__(self, joystick):
		self.joystick = joystick
		self.joystick.init()

		self.axes = [correctJoy(self.joystick.get_axis(i)) for i in range(self.joystick.get_numaxes())]
		self.balls = [self.joystick.get_ball(i) for i in range(self.joystick.get_numballs())]
		self.buttons = [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]
		self.hats = [self.joystick.get_hat(i) for i in range(self.joystick.get_numhats())]


mapping = {
	pygame.K_BACKQUOTE: 29,  # F1
	pygame.K_1: 31,  # G1
	pygame.K_2: 33,  # A1
	pygame.K_3: 35,  # B1
	pygame.K_4: 36,  # C2
	pygame.K_5: 38,  # D2
	pygame.K_6: 40,  # E2
	pygame.K_7: 41,  # F2
	pygame.K_8: 43,  # G2
	pygame.K_9: 45,  # A2
	pygame.K_0: 47,  # B2
	pygame.K_MINUS: 48,  # C3
	pygame.K_EQUALS: 50,  # D3

	pygame.K_q: 43,  # G2
	pygame.K_w: 45,  # A2
	pygame.K_e: 47,  # B2
	pygame.K_r: 48,  # C3
	pygame.K_t: 50,  # D3
	pygame.K_y: 52,  # E3
	pygame.K_u: 53,  # F3
	pygame.K_i: 55,  # G3
	pygame.K_o: 57,  # A3
	pygame.K_p: 59,  # B3
	pygame.K_LEFTBRACKET: 60,  # C4
	pygame.K_RIGHTBRACKET: 62,  # D4

	pygame.K_a: 55,  # G3
	pygame.K_s: 57,  # A3
	pygame.K_d: 59,  # B3
	pygame.K_f: 60,  # C4
	pygame.K_g: 62,  # D4
	pygame.K_h: 64,  # E4
	pygame.K_j: 65,  # F4
	pygame.K_k: 67,  # G4
	pygame.K_l: 69,  # A4
	pygame.K_SEMICOLON: 71,  # B4
	pygame.K_QUOTE: 72,  # C5
	92: 74,  # D5  HASH

	60: 65,  # F4  BACKSLASH
	pygame.K_z: 67,  # G4
	pygame.K_x: 69,  # A4
	pygame.K_c: 71,  # B4
	pygame.K_v: 72,  # C5
	pygame.K_b: 74,  # D5
	pygame.K_n: 76,  # E5
	pygame.K_m: 77,  # F5
	pygame.K_COMMA: 79,  # G5
	pygame.K_PERIOD: 81,  # A5
	pygame.K_SLASH: 83  # B5
}

class QwertyPiano(Client):
	def __init__(self, name):
		super().__init__(name)
		self.step_up = 0

		self.height = 300
		self.width = 400

		pygame.init()

		self.joysticks = [JoyManager(pygame.joystick.Joystick(i)) for i in range(pygame.joystick.get_count())]

		self.screen = pygame.display.set_mode((self.width, self.height))  # , pygame.FULLSCREEN)
		pygame.display.set_caption('jazZy')

		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((250, 250, 250))

	async def run(self):
		await self.connect()
		# await self.request("subscribe", "keyboard")
		await asyncio.gather(
			super().run(),
			self.loop()
		)

	async def loop(self):
		asyncio.current_task().set_name(self.__name__ + "-Transmitter")
		while True:
			events = pygame.event.get()  # may need pump=True
			if not self.ready:
				return
			for event in events:
				msg = None
				if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
					if event.key in mapping:
						if event.type == pygame.KEYDOWN:
							msg = mido.Message('note_on', note=mapping[event.key])
						else:
							msg = mido.Message('note_off', note=mapping[event.key])
					elif event.key == pygame.K_SPACE:
						value = 127 if event.type == pygame.KEYDOWN else 0
						msg = mido.Message('control_change', control=64, value=value)

				elif event.type == pygame.JOYAXISMOTION:
					value = int((correctJoy(event.value) + 1)/2 * 127)
					if self.joysticks[event.joy].axes[event.axis] != value:
						self.joysticks[event.joy].axes[event.axis] = value
						msg = mido.Message('control_change', control=[1, 91, 74, 95][event.axis], value=value)
				# elif event.type == pygame.JOYBALLMOTION:
				# 	pass
				elif event.type == pygame.JOYBUTTONDOWN:
					self.joysticks[event.joy].buttons[event.button] = True
					msg = mido.Message('note_on', note=event.button+60)
				elif event.type == pygame.JOYBUTTONUP:
					self.joysticks[event.joy].buttons[event.button] = False
					msg = mido.Message('note_off', note=event.button+60)
				# elif event.type == pygame.JOYHATMOTION:
				# 	pass

				elif event.type == pygame.QUIT:
					await self.quit()
					return

				if msg is not None:
					await self.broadcast("piano", "midi_hex", msg.hex())

			self.screen.blit(self.background, (0, 0))
			pygame.display.update()

			await self.wait()


if __name__ == "__main__":
	piano = QwertyPiano("Piano")
	asyncio.run(piano.run())
