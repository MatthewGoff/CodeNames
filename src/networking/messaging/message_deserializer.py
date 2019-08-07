
from networking.messaging.messaging_constants import MessagingConstants
from networking.messaging.cm_click import CMClick
from networking.messaging.cm_init_player import CMInitPlayer
from networking.messaging.cm_new_game import CMNewGame
from networking.messaging.cm_new_player import CMNewPlayer
from networking.messaging.sm_click import SMClick
from networking.messaging.sm_init_player import SMInitPlayer
from networking.messaging.sm_overwrite_cards import SMOverwriteCards
from networking.messaging.sm_new_player import SMNewPlayer
from networking.messaging.sm_remove_player import SMRemovePlayer
from networking.messaging.sm_overwrite_players import SMOverwritePlayers

class MessageDeserializer(object):

	def deserialize(byte_array):
		message_type = byte_array[0:4]
		if (message_type == MessagingConstants.CM_NEW_PLAYER):
			return CMNewPlayer.deserialize(byte_array)
		elif (message_type == MessagingConstants.CM_NEW_GAME):
			return CMNewGame.deserialize(byte_array)
		elif (message_type == MessagingConstants.CM_INIT_PLAYER):
			return CMInitPlayer.deserialize(byte_array)
		elif (message_type == MessagingConstants.CM_CLICK):
			return CMClick.deserialize(byte_array)
		elif (message_type == MessagingConstants.SM_NEW_PLAYER):
			return SMNewPlayer.deserialize(byte_array)
		elif (message_type == MessagingConstants.SM_OVERWRITE_CARDS):
			return SMOverwriteCards.deserialize(byte_array)
		elif (message_type == MessagingConstants.SM_INIT_PLAYER):
			return SMInitPlayer.deserialize(byte_array)
		elif (message_type == MessagingConstants.SM_CLICK):
			return SMClick.deserialize(byte_array)
		elif (message_type == MessagingConstants.SM_REMOVE_PLAYER):
			return SMRemovePlayer.deserialize(byte_array)
		elif (message_type == MessagingConstants.SM_OVERWRITE_PLAYERS):
			return SMOverwritePlayers.deserialize(byte_array)
		else:
			return None