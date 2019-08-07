import tkinter

class InitPlayerDialog(object):

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

		self.team_label = tkinter.Label(self.window, text = "Choose your team:", font = ("arial", 14, "bold"))
		self.team_label.place(x = 10, y = 10, width = 200, height = 30)

		self.team_variable = tkinter.StringVar()
		self.team_variable.set("red")

		self.red_radiobutton = tkinter.Radiobutton(
			self.window,
			text = "Red",
			variable = self.team_variable,
			value = "red",
			anchor = "nw",
			fg = "red")
		self.red_radiobutton.place(x = 70, y = 40, width = 180, height = 20)

		self.blue_radiobutton = tkinter.Radiobutton(
			self.window,
			text = "Blue",
			variable = self.team_variable,
			value = "blue",
			anchor = "nw",
			fg = "blue")
		self.blue_radiobutton.place(x = 70, y = 60, width = 180, height = 20)

		self.spectator_radiobutton = tkinter.Radiobutton(
			self.window,
			text = "Spectator",
			variable = self.team_variable,
			value = "spectator",
			anchor = "nw",
			fg = "black")
		self.spectator_radiobutton.place(x = 70, y = 80, width = 180, height = 20)

		self.role_label = tkinter.Label(self.window, text = "Choose your role:", font = ("arial", 14, "bold"))
		self.role_label.place(x = 10, y = 110, width = 200, height = 30)

		self.role_variable = tkinter.StringVar()
		self.role_variable.set("agent")

		self.agent_radiobutton = tkinter.Radiobutton(
			self.window,
			text = "Agent",
			variable = self.role_variable,
			value = "agent",
			anchor = "nw")
		self.agent_radiobutton.place(x = 70, y = 140, width = 150, height = 20)

		self.spymaster_radiobutton = tkinter.Radiobutton(
			self.window,
			text = "Spymaster",
			variable = self.role_variable,
			value = "spymaster",
			anchor = "nw")
		self.spymaster_radiobutton.place(x = 70, y = 160, width = 150, height = 20)

		self.button = tkinter.Button(self.window, text = "I'm Ready!", command = self.close)
		self.button.place(x = 70, y = 200, width = 80, height = 20)

		self.window.withdraw()

	def open(self, parent):
		self.window.update()
		self.window.deiconify()
		self.window.transient(parent)
		self.window.grab_set()
		parent.wait_window(self.window)

	def close(self):
		self.window.destroy()
		self.application_manager.init_player(self.team_variable.get(), self.role_variable.get())