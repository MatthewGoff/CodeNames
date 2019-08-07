
from networking.messaging.messaging_constants import MessagingConstants
from networking.messaging.message import Message

class CMInitPlayer(Message):
	
	def __init__(self, team, role):
		self.team = team
		self.role = role

	def serialize(self):
		byte_array = b""
		byte_array += MessagingConstants.CM_INIT_PLAYER
		byte_array += self.team[0].encode()
		byte_array += self.role[0].encode()
		return byte_array

	def deserialize(byte_array):
		team = chr(byte_array[4])
		role = chr(byte_array[5])
		if (team == "r"):
			team = "red"
		elif (team == "b"):
			team = "blue"
		elif (team == "s"):
			team = "spectator"
		if (role == "a"):
			role = "agent"
		elif (role == "s"):
			role = "spymaster"
		return CMInitPlayer(team, role)

	def __str__(self):
		return "Initializing player to team " + self.team + " and role " + self.role
