import random

from game.card import Card
from game.player import Player
from game.game_events.click_event import ClickEvent
from game.game_events.init_player_event import InitPlayerEvent
from game.game_events.overwrite_cards_event import OverwriteCardsEvent
from game.game_events.new_player_event import NewPlayerEvent
from game.game_events.remove_player_event import RemovePlayerEvent
from game.game_events.overwrite_players_event import OverwritePlayersEvent

class Game():

	NUM_ARTWORK = 280

	def __init__(self):
		self.cards = None

		self.players = {}
		self.listeners = []

	def deal(self, seed, red, blue, bystander, assassin):
		random.seed(seed)
		artwork = []
		for i in range(0, self.NUM_ARTWORK):
			artwork += [i]

		teams = []
		for i in range(0, red):
			teams += ["red"]
		for i in range(0, blue):
			teams += ["blue"]
		for i in range(0, bystander):
			teams += ["bystander"]
		for i in range(0, assassin):
			teams += ["assassin"]
		while len(teams) < 20:
			teams += ["bystander"]

		self.cards = []
		for x in range(5):
			self.cards += [[]]
			for y in range(4):
				index = random.randrange(0, len(artwork))
				artwork_selection = artwork[index]
				del artwork[index]

				index = random.randrange(0, len(teams))
				team_selection = teams[index]
				del teams[index]

				self.cards[x] += [Card(artwork_selection, team_selection, False)]

		self.notify_listeners(OverwriteCardsEvent(self.cards))

	def overwrite_cards(self, cards):
		self.cards = cards
		self.notify_listeners(OverwriteCardsEvent(self.cards))

	def overwrite_players(self, players):
		self.players = {}
		for player in players:
			self.players[player.uid] = player

		self.notify_listeners(OverwritePlayersEvent(self.players))

	def click(self, x_coord, y_coord):
		self.cards[x_coord][y_coord].revealed = not self.cards[x_coord][y_coord].revealed
		self.notify_listeners(ClickEvent(x_coord, y_coord))

	def new_player(self, uid, name):
		self.players[uid] = Player(uid, name, "spectator", False)
		self.notify_listeners(NewPlayerEvent(self.players[uid]))

	def remove_player(self, uid):
		del self.players[uid]
		self.notify_listeners(RemovePlayerEvent(uid))

	def init_player(self, uid, team, role):
		self.players[uid].team = team
		if (role == "agent"):
			spymaster = False
		if (role == "spymaster"):
			spymaster = True
		print("initializing player and spymater = " + str(spymaster))
		self.players[uid].spymaster = spymaster
		self.notify_listeners(InitPlayerEvent(self.players[uid]))

	def register_game_listener(self, callback):
		self.listeners += [callback]

	def notify_listeners(self, game_event):
		for listener in self.listeners:
			listener(game_event)

	def get_players(self):
		players = []
		for key in self.players.keys():
			players += [self.players[key]]
		return players
