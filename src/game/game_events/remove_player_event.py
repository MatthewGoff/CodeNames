
from game.game_events.game_event import GameEvent

class RemovePlayerEvent(GameEvent):

	def __init__(self, uid):
		self.uid = uid