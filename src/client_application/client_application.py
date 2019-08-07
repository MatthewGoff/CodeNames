import socket

from client_application.gui.main_menu import MainMenu
from client_application.gui.play_window import PlayWindow
from client_application.gui.alert_dialog import AlertDialog
from client_application.gui.init_player_dialog import InitPlayerDialog
from client_application.gui.new_game_dialog import NewGameDialog
from networking.internet_connection import InternetConnection
from util.asynch_queue import AsynchQueue
from game.game import Game
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

class ClientApplication(object):

	UPDATE_PERIOD = int(1000/60)

	def __init__(self):
		self.main_menu = MainMenu(self)
		self.root_tk = self.main_menu.window
		self.play_window = PlayWindow(self.main_menu.window, self)

		self.message_queue = AsynchQueue()
		self.socket = None
		self.internet_connection = None

		self.game = Game()
		self.game.register_game_listener(self.play_window.game_updated)

		self.username = None

	def update(self):
		if (self.internet_connection is not None):
			message = self.message_queue.dequeue()
			if (message != None):
				self.process_message(message)
				self.display_message(message)

		self.root_tk.after(self.UPDATE_PERIOD, self.update)

	def process_message(self, message):
		if (isinstance(message, SMClick)):
			self.game.click(message.x_coord, message.y_coord)
		elif (isinstance(message, SMInitPlayer)):
			self.game.init_player(message.uid, message.team, message.role)
		elif (isinstance(message, SMOverwriteCards)):
			self.game.overwrite_cards(message.cards)
			self.open_init_player_dialog()
		elif (isinstance(message, SMNewPlayer)):
			self.game.new_player(message.uid, message.name)
		elif (isinstance(message, SMRemovePlayer)):
			self.game.remove_player(message.uid)
		elif (isinstance(message, SMOverwritePlayers)):
			self.game.overwrite_players(message.players)
		else:
			print("Unknown message type recieved from server")

	def display_message(self, message):
		print("Message from server: (" + str(message) + ")")

	def run(self):
		self.root_tk.after(self.UPDATE_PERIOD, self.update)
		self.root_tk.mainloop()

	def attempt_connection(self, username, host, port):
		self.username = username
		try:
			port = int(port)
		except:
			port = 0

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.socket.connect((host, port))
			success = True
		except:
			success = False

		if (success):
			self.connection_succeeded()
		else:
			self.connection_failed()

	def connection_failed(self):
		self.open_alert_dialog("Failed to connect to server")

	def connection_succeeded(self):
		self.socket.setblocking(False)

		self.internet_connection = InternetConnection(0, self.socket, self.new_message, self.connection_lost)
		self.internet_connection.start()
		self.internet_connection.send(CMNewPlayer(self.username))

		self.main_menu.hide()
		self.play_window.show()

	def open_init_player_dialog(self):
		init_player_dialog = InitPlayerDialog(self.play_window.window, self)
		init_player_dialog.open(self.play_window.window)

	def init_player(self, team, role):
		if (role == "spymaster"):
			self.play_window.reveal()
		self.internet_connection.send(CMInitPlayer(team, role))

	def connection_lost(self, uid):
		self.disconnect()
		self.open_alert_dialog("Lost connection to server")

	def new_message(self, uid, message):
		self.message_queue.enqueue(message)

	def open_alert_dialog(self, text):
		alert_dialog = AlertDialog(self.main_menu.window, text)
		alert_dialog.open(self.main_menu.window)

	def quit(self):
		if (self.internet_connection is not None):
			self.internet_connection.disconnect()
		self.play_window.close()
		self.main_menu.close()

	def disconnect(self):
		self.internet_connection.disconnect()
		self.play_window.hide()
		self.main_menu.show()

	def open_new_game_dialog(self):
		new_game_dialog = NewGameDialog(self.play_window.window, self)
		new_game_dialog.open(self.play_window.window)

	def submit_new_game(self, team, red, blue, bystander, assassin):
		self.internet_connection.send(CMNewGame(team, red, blue, bystander, assassin))

	def click(self, x_coord, y_coord):
		self.internet_connection.send(CMClick(x_coord, y_coord))