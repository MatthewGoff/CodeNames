
from networking.messaging.messaging_constants import MessagingConstants
from networking.messaging.message import Message

class SMRemovePlayer(Message):
	
	def __init__(self, uid):
		self.uid = uid

	def serialize(self):
		byte_array = b""
		byte_array += MessagingConstants.SM_REMOVE_PLAYER
		byte_array += self.uid.to_bytes(4, byteorder = "big")
		return byte_array

	def deserialize(byte_array):
		uid = int.from_bytes(byte_array[4:8], byteorder = "big")
		return SMRemovePlayer(uid)