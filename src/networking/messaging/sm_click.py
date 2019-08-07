
from networking.messaging.messaging_constants import MessagingConstants
from networking.messaging.message import Message

class SMClick(Message):
	
	def __init__(self, x_coord, y_coord):
		self.x_coord = x_coord
		self.y_coord = y_coord

	def serialize(self):
		byte_array = b""
		byte_array += MessagingConstants.SM_CLICK
		byte_array += self.x_coord.to_bytes(4, byteorder = "big")
		byte_array += self.y_coord.to_bytes(4, byteorder = "big")
		return byte_array

	def deserialize(byte_array):
		x_coord = int.from_bytes(byte_array[4:8], byteorder = "big")
		y_coord = int.from_bytes(byte_array[8:12], byteorder = "big")
		return SMClick(x_coord, y_coord)

	def __str__(self):
		return "Click at x = " + str(self.x_coord) + ", y = " + str(self.y_coord)