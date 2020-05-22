import json
import struct


def encode(data):
	def set_default(obj):
		if isinstance(obj, set):
			return list(obj)
		return obj

	# raise TypeError
	return json.dumps(data, default=set_default)


def decode(data):
	return json.loads(data)


async def recv_all(reader, n):
	data = b''
	while len(data) < n:  # todo review
		packet = await reader.read(n - len(data))
		print(3, "Packet: ", packet)
		if not packet:  # todo inspect
			return None  # EOF
		data += packet
	return data


async def recv_msg(reader):
	raw_msg_len = await recv_all(reader, 4)
	if not raw_msg_len:  # todo inspect
		return None
	msg_len = struct.unpack('<I', raw_msg_len)[0]
	print(3, "Length: ", msg_len)
	return await recv_all(reader, msg_len)


async def recv_obj(reader):
	msg = await recv_msg(reader)
	return decode(msg)

# async def rec(reader):
# 	raw_data = await recv_msg(reader)
# 	if raw_data is not None:  # todo inspect
# 		msg = raw_data.decode()
# 		if msg != '':
# 			print(2, "Received: ", msg)
# 			if callback is not None:
# 				callback(msg)
# 	else:
# 		print(1, "Connection died")
# 		close()


async def send_msg(writer, msg):
	if msg == '':
		print("Cannot send empty data!")
	else:
		print(1, "Sending: ", msg)
		if type(msg) is str:  # todo remove
			msg = bytearray(msg, 'utf-8')  # todo inspect replacing with .encode()
		size = struct.pack('<I', len(msg))
		# size = (bytes)(len(msg))
		# msg = size + msg
		writer.write(size)
		writer.write(msg)
		await writer.drain()


async def send_obj(writer, obj):
	msg = encode(obj)
	await send_msg(writer, msg)