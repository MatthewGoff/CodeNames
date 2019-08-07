
from networking.messaging.messaging_constants import MessagingConstants
from networking.messaging.message import Message

class SMNewPlayer(Message):

	def __init__(self, uid, name):
		self.uid = uid
		self.name = name

	def serialize(self):
		byte_array = b""
		byte_array += MessagingConstants.SM_NEW_PLAYER
		byte_array += self.uid.to_bytes(4, byteorder = "big")
		byte_array += self.name.encode()
		return byte_array

	def deserialize(byte_array):
		uid = int.from_bytes(byte_array[4:8], byteorder = "big")
		name = byte_array[8:].decode()
		return SMNewPlayer(uid, name)

	def __str__(self):
		return "New player: " + str(self.uid) + ", " + self.name
