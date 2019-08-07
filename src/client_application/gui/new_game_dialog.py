import tkinter

class NewGameDialog(object):

	def __init__(self, parent, application_manager):
		self.application_manager = application_manager

		self.window = tkinter.Toplevel(parent)
		self.window.title("")
		width = 220
		height = 240
		x_offset = int(self.window.winfo_screenwidth()/2 - width/2)
		y_offset = int(self.window.winfo_screenheight()/2 - height/2)
		self.window.geometry(str(width)+"x"+str(height)+"+"+str(x_offset)+"+"+str(y_offset))
		self.window.resizable(False, False)
		self.window.protocol("WM_DELETE_WINDOW", self.close)

		self.team_label = tkinter.Label(self.window, text = "Who goes first:", font = ("arial", 14, "bold"))
		self.team_label.place(x = 10, y = 10, width = 200, height = 30)

		self.team_variable = tkinter.StringVar()
		self.team_variable.set("red")

		self.red_radiobutton = tkinter.Radiobutton(
			self.window,
			text = "Red",
			variable = self.team_variable,
			value = "red",
			anchor = "nw",
			fg = "red",
			command = self.red_team_selected)
		self.red_radiobutton.place(x = 70, y = 40, width = 180, height = 20)

		self.blue_radiobutton = tkinter.Radiobutton(
			self.window,
			text = "Blue",
			variable = self.team_variable,
			value = "blue",
			anchor = "nw",
			fg = "blue",
			command = self.blue_team_selected)
		self.blue_radiobutton.place(x = 70, y = 60, width = 180, height = 20)

		self.role_label = tkinter.Label(self.window, text = "Number of pictures:", font = ("arial", 14, "bold"))
		self.role_label.place(x = 10, y = 80, width = 200, height = 30)

		self.red_var = tkinter.StringVar()
		self.red_var.set("8")
		self.red_entry = tkinter.Entry(self.window, textvariable = self.red_var)
		self.red_entry.place(x = 70, y = 110, width = 25, height = 18)
		self.red_label = tkinter.Label(self.window, text = "Red", anchor = "nw")
		self.red_label.place(x = 100, y = 110, width = 50, height = 20)

		self.blue_var = tkinter.StringVar()
		self.blue_var.set("7")
		self.blue_entry = tkinter.Entry(self.window, textvariable = self.blue_var)
		self.blue_entry.place(x = 70, y = 135, width = 25, height = 18)
		self.blue_label = tkinter.Label(self.window, text = "Blue", anchor = "nw")
		self.blue_label.place(x = 100, y = 135, width = 50, height = 20)

		self.bystander_var = tkinter.StringVar()
		self.bystander_var.set("4")
		self.bystander_entry = tkinter.Entry(self.window, textvariable = self.bystander_var)
		self.bystander_entry.place(x = 70, y = 160, width = 25, height = 18)
		self.bystander_label = tkinter.Label(self.window, text = "Bystander", anchor = "nw")
		self.bystander_label.place(x = 100, y = 160, width = 50, height = 20)

		self.assassin_var = tkinter.StringVar()
		self.assassin_var.set("1")
		self.assassin_entry = tkinter.Entry(self.window, textvariable = self.assassin_var)
		self.assassin_entry.place(x = 70, y = 185, width = 25, height = 18)
		self.assassin_label = tkinter.Label(self.window, text = "Assassin", anchor = "nw")
		self.assassin_label.place(x = 100, y = 185, width = 50, height = 20)

		self.button = tkinter.Button(self.window, text = "OK", command = self.submit)
		self.button.place(x = 70, y = 210, width = 80, height = 20)

		self.window.withdraw()

	def red_team_selected(self):
		self.red_var.set("8")
		self.blue_var.set("7")
		self.bystander_var.set("4")
		self.assassin_var.set("1")

	def blue_team_selected(self):
		self.red_var.set("7")
		self.blue_var.set("8")
		self.bystander_var.set("4")
		self.assassin_var.set("1")

	def open(self, parent):
		self.window.update()
		self.window.deiconify()
		#self.window.transient(parent)
		self.window.grab_set()
		parent.wait_window(self.window)

	def submit(self):
		self.close()

		try:
			red = int(self.red_var.get())
		except:
			red = 0

		try:
			blue = int(self.blue_var.get())
		except:
			blue = 0

		try:
			bystander = int(self.bystander_var.get())
		except:
			bystander = 0

		try:
			assassin = int(self.assassin_var.get())
		except:
			assassin = 0

		self.application_manager.submit_new_game(
			self.team_variable.get(),
			red,
			blue,
			bystander,
			assassin)

	def close(self):
		self.window.destroy()
