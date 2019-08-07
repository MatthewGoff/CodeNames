
from networking.messaging.messaging_constants import MessagingConstants
from networking.messaging.message import Message

class CMNewPlayer(Message):

	def __init__(self, name):
		self.name = name

	def serialize(self):
		byte_array = b""
		byte_array += MessagingConstants.CM_NEW_PLAYER
		byte_array += self.name.encode()
		return byte_array

	def deserialize(byte_array):
		name = byte_array[4:].decode()
		return CMNewPlayer(name)

	def __str__(self):
		return "New player: " + self.name
