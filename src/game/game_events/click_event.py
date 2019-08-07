
from game.game_events.game_event import GameEvent

class ClickEvent(GameEvent):

	def __init__(self, x_coord, y_coord):
		self.x_coord = x_coord
		self.y_coord = y_coord