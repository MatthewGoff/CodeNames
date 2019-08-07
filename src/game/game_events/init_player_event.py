
from game.game_events.game_event import GameEvent

class InitPlayerEvent(GameEvent):

	def __init__(self, player):
		self.player = player