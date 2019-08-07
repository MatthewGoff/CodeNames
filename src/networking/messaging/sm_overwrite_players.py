
from networking.messaging.messaging_constants import MessagingConstants
from networking.messaging.message import Message
from game.player import Player

class SMOverwritePlayers(Message):
	
	def __init__(self, players):
		self.players = players

	def serialize(self):
		byte_array = b""
		byte_array += MessagingConstants.SM_OVERWRITE_PLAYERS
		byte_array += len(self.players).to_bytes(4, byteorder = "big")
		for player in self.players:
			byte_array += player.uid.to_bytes(4, byteorder = "big")
			byte_array += len(player.name).to_bytes(4, byteorder = "big")
			byte_array += player.name.encode()
			byte_array += SMOverwritePlayers.team_to_int(player.team).to_bytes(1, byteorder = "big")
			byte_array += player.spymaster.to_bytes(1, byteorder = "big")
		return byte_array

	def deserialize(byte_array):
		players = []
		num_players = int.from_bytes(byte_array[4:8], byteorder = "big")
		index = 8
		for i in range(0, num_players):
			uid = int.from_bytes(byte_array[index:index + 4], byteorder = "big")
			index += 4
			name_length = int.from_bytes(byte_array[index:index + 4], byteorder = "big")
			index += 4
			name = byte_array[index:index + name_length].decode()
			index += name_length
			team = SMOverwritePlayers.int_to_team(int(byte_array[index]))
			index += 1
			spymaster = bool(byte_array[index])
			index += 1

			players += [Player(uid, name, team, spymaster)]
		return SMOverwritePlayers(players)

	def __str__(self):
		return "Overwriteing players"

	def team_to_int(team):
		if (team == "red"):
			return 0
		elif (team == "blue"):
			return 1
		elif (team == "spectator"):
			return 2
		else:
			return 0

	def int_to_team(integer):
		if (integer == 0):
			return "red"
		elif (integer == 1):
			return "blue"
		elif (integer == 2):
			return "spectator"
		else:
			return "red"
