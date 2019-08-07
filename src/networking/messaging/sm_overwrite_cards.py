
from networking.messaging.messaging_constants import MessagingConstants
from networking.messaging.message import Message
from game.card import Card

class SMOverwriteCards(Message):
	
	def __init__(self, cards):
		self.cards = cards

	def serialize(self):
		byte_array = b""
		byte_array += MessagingConstants.SM_OVERWRITE_CARDS
		for x in range(0, 5):
			for y in range(0, 4):
				byte_array += self.cards[x][y].artwork.to_bytes(4, byteorder = "big")
				byte_array += SMOverwriteCards.team_to_int(self.cards[x][y].team).to_bytes(1, byteorder = "big")
				byte_array += self.cards[x][y].revealed.to_bytes(1, byteorder = "big")
		return byte_array

	def deserialize(byte_array):
		cards = []
		index = 4
		for x in range(0, 5):
			cards += [[]]
			for y in range(0, 4):
				artwork = int.from_bytes(byte_array[index:index + 4], byteorder = "big")
				team = SMOverwriteCards.int_to_team(int(byte_array[index + 4]))
				revealed = bool(byte_array[index + 5])
				cards[x] += [Card(artwork, team, revealed)]
				index += 6
		return SMOverwriteCards(cards)

	def __str__(self):
		return "Overwriteing cards"

	def team_to_int(team):
		if (team == "red"):
			return 0
		elif (team == "blue"):
			return 1
		elif (team == "bystander"):
			return 2
		elif (team == "assassin"):
			return 3
		else:
			return 0

	def int_to_team(integer):
		if (integer == 0):
			return "red"
		elif (integer == 1):
			return "blue"
		elif (integer == 2):
			return "bystander"
		elif (integer == 3):
			return "assassin"
		else:
			return "red"
