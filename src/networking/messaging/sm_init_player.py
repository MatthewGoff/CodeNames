
from networking.messaging.messaging_constants import MessagingConstants
from networking.messaging.message import Message

class SMInitPlayer(Message):
	
	def __init__(self, uid, team, role):
		self.uid = uid
		self.team = team
		self.role = role

	def serialize(self):
		byte_array = b""
		byte_array += MessagingConstants.SM_INIT_PLAYER
		byte_array += self.uid.to_bytes(4, byteorder = "big")
		byte_array += self.team[0].encode()
		byte_array += self.role[0].encode()
		return byte_array

	def deserialize(byte_array):
		uid = int.from_bytes(byte_array[4:8], byteorder = "big")
		team = chr(byte_array[8])
		role = chr(byte_array[9])
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
		return SMInitPlayer(uid, team, role)

	def __str__(self):
		return "Initializing player " + str(self.uid) + " to team " + self.team + " and role " + self.role
