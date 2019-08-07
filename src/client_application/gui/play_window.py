import tkinter

from client_application.gui.card_slot import CardSlot
from game.game_events.click_event import ClickEvent
from game.game_events.init_player_event import InitPlayerEvent
from game.game_events.overwrite_cards_event import OverwriteCardsEvent
from game.game_events.new_player_event import NewPlayerEvent
from game.game_events.remove_player_event import RemovePlayerEvent
from game.game_events.overwrite_players_event import OverwritePlayersEvent

class PlayWindow():

	def __init__(self, parent, application_manager):
		self.application_manager = application_manager

		self.player_labels = {}
		
		self.window = tkinter.Toplevel(parent)
		self.window.title("Code Names")
		width = 1380
		height = 950
		x_offset = int(self.window.winfo_screenwidth()/2 - width/2)
		y_offset = int(self.window.winfo_screenheight()/2 - height/2)
		self.window.geometry(str(width)+"x"+str(height)+"+"+str(x_offset)+"+"+str(y_offset))
		self.window.resizable(False, False)
		self.window.protocol("WM_DELETE_WINDOW", lambda: self.application_manager.quit())

		self.menu = tkinter.Menu(self.window)
		self.window.config(menu = self.menu)

		self.file_menu = tkinter.Menu(self.menu)
		self.menu.add_cascade(label = "Menu", menu = self.file_menu)
		self.file_menu.add_command(label = "Disconnect", command = self.disconnect)
		self.file_menu.add_command(label = "New game", command = self.open_new_game_dialog)
		self.card_slots = []
		for x in range (0, 5):
			self.card_slots += [[]]
			for y in range (0, 4):
				self.card_slots[x] += [CardSlot(self.window, x, y, application_manager)]

		self.row4 = tkinter.Label(self.window, text = "4", font = ("ariel", 24, "bold"))
		self.row4.place(x = 200, y = 105, width = 30, height = 30)

		self.row3 = tkinter.Label(self.window, text = "3", font = ("ariel", 24, "bold"))
		self.row3.place(x = 200, y = 335, width = 30, height = 30)

		self.row2 = tkinter.Label(self.window, text = "2", font = ("ariel", 24, "bold"))
		self.row2.place(x = 200, y = 565, width = 30, height = 30)

		self.row1 = tkinter.Label(self.window, text = "1", font = ("ariel", 24, "bold"))
		self.row1.place(x = 200, y = 795, width = 30, height = 30)

		self.colA = tkinter.Label(self.window, text = "A", font = ("ariel", 24, "bold"))
		self.colA.place(x = 325, y = 920, width = 30, height = 30)

		self.colB = tkinter.Label(self.window, text = "B", font = ("ariel", 24, "bold"))
		self.colB.place(x = 555, y = 920, width = 30, height = 30)

		self.colC = tkinter.Label(self.window, text = "C", font = ("ariel", 24, "bold"))
		self.colC.place(x = 785, y = 920, width = 30, height = 30)

		self.colD = tkinter.Label(self.window, text = "D", font = ("ariel", 24, "bold"))
		self.colD.place(x = 1015, y = 920, width = 30, height = 30)

		self.colE = tkinter.Label(self.window, text = "E", font = ("ariel", 24, "bold"))
		self.colE.place(x = 1245, y = 920, width = 30, height = 30)

		self.divider = tkinter.Canvas(self.window, highlightthickness = 0)
		self.divider.create_rectangle(0, 0, 2, 950, fill = "black")
		self.divider.place(x = 200, y = 0, width = 2, height= 950)

		self.hide()

	def show(self):
		self.window.update()
		self.window.deiconify()

	def hide(self):
		self.window.withdraw()

	def close(self):
		self.window.destroy()

	def disconnect(self):
		self.application_manager.disconnect()

	def open_new_game_dialog(self):
		self.application_manager.open_new_game_dialog()

	def game_updated(self, game_event):
		if (isinstance(game_event, ClickEvent)):
			self.handle_click_event(game_event)
		elif (isinstance(game_event, InitPlayerEvent)):
			self.handle_init_player_event(game_event)
		elif (isinstance(game_event, OverwriteCardsEvent)):
			self.handle_overwrite_cards_event(game_event)
		elif (isinstance(game_event, NewPlayerEvent)):
			self.handle_new_player_event(game_event)
		elif (isinstance(game_event, RemovePlayerEvent)):
			self.handle_remove_player_event(game_event)
		elif (isinstance(game_event, OverwritePlayersEvent)):
			self.handle_overwrite_players_event(game_event)

	def handle_click_event(self, click_event):
		self.card_slots[click_event.x_coord][click_event.y_coord].recieve_click()

	def handle_remove_player_event(self, remove_player_event):
		del self.player_labels[remove_player_event.uid]
		self.update_player_list()

	def handle_overwrite_cards_event(self, overwrite_cards_event):
		for x in range (0, 5):
			for y in range (0, 4):
				self.card_slots[x][y].overwrite(overwrite_cards_event.cards[x][y])

	def handle_init_player_event(self, init_player_event):
		if (init_player_event.player.team == "red"):
			color = "red"
		elif (init_player_event.player.team == "blue"):
			color = "blue"
		elif (init_player_event.player.team == "spectator"):
			color = "black"

		if (init_player_event.player.spymaster):
			font = ("ariel", 12, "bold")
		else:
			font = ("ariel", 12)

		self.player_labels[init_player_event.player.uid].config(fg = color, font = font)

	def handle_new_player_event(self, new_player_event):
		self.player_labels[new_player_event.player.uid] = tkinter.Label(
			self.window,
			text = new_player_event.player.name,
			font = ("ariel", 12, "italic"),
			anchor = "nw")
		self.update_player_list()

	def handle_overwrite_players_event(self, overwrite_players_event):
		self.player_labels = {}
		for key in overwrite_players_event.players.keys():
			player = overwrite_players_event.players[key]
			if (player.team == "red"):
				color = "red"
			elif (player.team == "blue"):
				color = "blue"
			elif (player.team == "spectator"):
				color = "black"

			if (player.spymaster):
				font = ("ariel", 12, "bold")
			else:
				font = ("ariel", 12)

			self.player_labels[player.uid] = tkinter.Label(self.window, fg = color, text = player.name, font = font, anchor = "nw")

		self.update_player_list()

	def update_player_list(self):
		vertical_offset = 10
		for uid in self.player_labels.keys():
			self.player_labels[uid].place(x = 10, y = vertical_offset, width = 190, height = 20)
			vertical_offset += 20

	def reveal(self):
		for x in range (0, 5):
			for y in range (0, 4):
				self.card_slots[x][y].reveal()