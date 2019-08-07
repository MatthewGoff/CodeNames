import tkinter
from PIL import ImageTk, Image

class CardSlot():

	SIZE = 200

	def __init__(self, window, x_coord, y_coord, application_manager):
		self.application_manager = application_manager

		self.x_coord = x_coord
		self.y_coord = y_coord
		self.x_position = 240 + (self.SIZE + 30) * x_coord
		self.y_position = 20 + (self.SIZE + 30) * y_coord

		self.border = tkinter.Canvas(window, highlightthickness = 0)

		image = Image.open("../Resources/CoverArt.jpg").resize((self.SIZE, self.SIZE), Image.ANTIALIAS)
		self.imageTK = ImageTk.PhotoImage(image)
		self.artwork = tkinter.Label(window, anchor = "nw", image = self.imageTK, borderwidth = 0, bd = 0, relief = "ridge")
		self.artwork.bind("<Button-1>", self.submit_click)

		self.cover = tkinter.Canvas(window, highlightthickness = 0, bd = 0, relief = "ridge")
		self.cover.bind("<Button-1>", self.submit_click)

		self.color = None
		self.spymaster = None
		self.revealed = None

	def submit_click(self, event):
		self.application_manager.click(self.x_coord, self.y_coord)

	def recieve_click(self):
		self.revealed = not self.revealed
		self.refresh()

	def overwrite(self, card):
		self.color = CardSlot.team_to_color(card.team)
		self.spymaster = False
		self.revealed = card.revealed

		self.cover.create_rectangle(-1, -1, self.SIZE, self.SIZE, fill = self.color)
		self.border.create_rectangle(-10, -10, self.SIZE + 20, self.SIZE + 20, fill = self.color)

		image = Image.open("../Resources/CoverArt.jpg").resize((self.SIZE, self.SIZE), Image.ANTIALIAS)
		self.imageTK = ImageTk.PhotoImage(image)
		self.artwork.configure(image = self.imageTK)

		self.refresh()

	def refresh(self):
		if (self.spymaster):
			self.border.place(x = (self.x_position - 10), y = (self.y_position - 10), width = (self.SIZE + 20), height = (self.SIZE + 20))
		else:
			self.border.place_forget()

		self.artwork.place(x = self.x_position, y = self.y_position, width = self.SIZE, height = self.SIZE)

		if (self.revealed):
			self.cover.place(x = self.x_position, y = self.y_position, width = self.SIZE, height = self.SIZE)
		else:
			self.cover.place_forget()

	def reveal(self):
		self.spymaster = True
		self.refresh()

	def team_to_color(team):
		if (team == "red"):
			return "red"
		elif (team == "blue"):
			return "blue"
		elif (team == "bystander"):
			return "white"
		elif (team == "assassin"):
			return "black"
		else:
			return "red"

