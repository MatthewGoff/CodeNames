
from networking.messaging.messaging_constants import MessagingConstants
from networking.messaging.message import Message

class CMNewGame(Message):
	
	def __init__(self, team, red, blue, bystander, assassin):
		self.team = team
		self.red = red
		self.blue = blue
		self.bystander = bystander
		self.assassin = assassin

	def serialize(self):
		byte_array = b""
		byte_array += MessagingConstants.CM_NEW_GAME
		byte_array += self.red.to_bytes(4, byteorder = "big")
		byte_array += self.blue.to_bytes(4, byteorder = "big")
		byte_array += self.bystander.to_bytes(4, byteorder = "big")
		byte_array += self.assassin.to_bytes(4, byteorder = "big")
		byte_array += self.team[0].encode()
		return byte_array

	def deserialize(byte_array):
		red = int.from_bytes(byte_array[4:8], byteorder = "big")
		blue = int.from_bytes(byte_array[8:12], byteorder = "big")
		bystander = int.from_bytes(byte_array[12:16], byteorder = "big")
		assassin = int.from_bytes(byte_array[16:20], byteorder = "big")
		team = chr(byte_array[20])
		if (team == "r"):
			team = "red"
		elif (team == "b"):
			team = "blue"
		return CMNewGame(team, red, blue, bystander, assassin)

	def __str__(self):
		return "New game: " + self.team + ", " + str(self.red) + ", " + str(self.blue) + ", " + str(self.bystander) + ", " + str(self.assassin)
