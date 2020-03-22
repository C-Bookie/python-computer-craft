from unit import Unit

#http://127.0.0.1:8080/start/0/test/

async def test(api):
	unit = Unit(api)
	await api.print("moo")
	print("moo")