
from game.game_events.game_event import GameEvent

class OverwritePlayersEvent(GameEvent):

	def __init__(self, players):
		self.players = players