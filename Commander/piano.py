import asyncio

import pygame
import mido
import pygame.midi

from coms import Client


class MidiKeyboard(Client):
	def __init__(self):
		super().__init__()
		self.step_up = 0

		self.mapping = {
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

		self.height = 300
		self.width = 400

		pygame.init()
		self.screen = pygame.display.set_mode((self.width, self.height))  # , pygame.FULLSCREEN)
		pygame.display.set_caption('jazZy')

		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((250, 250, 250))

	async def run(self):
		await self.connect()
		await self.request("subscribe", "keyboard")
		await asyncio.gather(
			super().run(),
			self.loop()
		)

	async def loop(self):
		while True:
			events = pygame.event.get()
			for event in events:
				if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
					if event.key == pygame.K_SPACE:
						await self.broadcast("sustain", "piano", event.type == pygame.KEYDOWN)
					elif event.key in self.mapping:
						await self.broadcast("note", "piano", self.mapping[event.key] + self.step_up, event.type == pygame.KEYDOWN)
				if event.type == pygame.QUIT:
					return

			self.screen.blit(self.background, (0, 0))
			pygame.display.flip()


if __name__ == "__main__":
	keyboard = MidiKeyboard()
	asyncio.run(keyboard.run())
