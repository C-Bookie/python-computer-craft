import asyncio
import mido

from coms import Client


class MidiPiano(Client):
	def __init__(self, name):
		super().__init__(name)
		self.step_up = 0

		self.white_list_functions += [
			"midi_hex"
		]

		self.inport = mido.open_input('masterkey 61 0')
		self.outport = mido.open_output('Alex 1')

	def midi_hex(self, hex):
		msg = mido.Message.from_hex(hex)
		self.outport.send(msg)

	async def run(self):
		await self.connect()
		await self.request("subscribe", "piano")  # comment out to disable receiving midi
		await asyncio.gather(
			super().run(),
			self.loop()  # comment out to disable midi transition
		)

	async def loop(self):
		asyncio.current_task().set_name(self.__name__ + "-Transmitter")
		while True:
			for msg in self.inport.iter_pending():
				await self.broadcast("piano", "midi_hex", msg.hex())
			await self.wait()

	def close(self):
		super().close()
		self.outport.close()
		self.inport.close()


if __name__ == "__main__":
	piano = MidiPiano("Piano")
	asyncio.run(piano.run())


