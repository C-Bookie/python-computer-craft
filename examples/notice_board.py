import computercraft.errors

async def notice_board(api):
	back = await api.peripheral.wrap("back")
	rules = """
	rule 1: don't fuck the ducks
	rule 2: or the geese
	"""
	await back.callRemote("monitor_0", "clear")
	await back.callRemote("monitor_0", "setCursorPos", 1, 1)
	await back.callRemote("monitor_0", "write", rules)
	await api.print('woot!')


