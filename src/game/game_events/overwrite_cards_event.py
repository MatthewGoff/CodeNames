
from game.game_events.game_event import GameEvent

class OverwriteCardsEvent(GameEvent):

	def __init__(self, cards):
		self.cards = cards