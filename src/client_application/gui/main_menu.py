import tkinter
from PIL import ImageTk, Image

class MainMenu(object):
	
	def __init__(self, application_manager):
		self.application_manager = application_manager

		self.window = tkinter.Tk()
		self.window.title("Code Names")
		width = 410
		height = 298
		x_offset = int(self.window.winfo_screenwidth()/2 - width/2)
		y_offset = int(self.window.winfo_screenheight()/2 - height/2)
		self.window.geometry(str(width)+"x"+str(height)+"+"+str(x_offset)+"+"+str(y_offset))
		self.window.resizable(False, False)
		self.window.protocol("WM_DELETE_WINDOW", lambda: self.application_manager.quit())

		image = Image.open("../Resources/CoverArt.jpg").resize((200, 278), Image.ANTIALIAS)
		self.imageTK = ImageTk.PhotoImage(image)
		self.label = tkinter.Label(self.window, anchor = "nw", image = self.imageTK)
		self.label.place(x = 10, y = 10, width = 200, height = 278)

		self.username_label = tkinter.Label(self.window, text = "Username:", anchor = "w")
		self.username_label.place(x = 220, y = 110, width = 100, height = 20)

		self.username_variable = tkinter.StringVar()
		self.username_entry = tkinter.Entry(self.window, textvariable = self.username_variable)
		self.username_entry.place(x = 300, y = 110, width = 100, height = 20)

		self.server_ip_label = tkinter.Label(self.window, text = "Server IP:", anchor = "w")
		self.server_ip_label.place(x = 220, y = 140, width = 100, height = 20)

		self.server_ip_variable = tkinter.StringVar()
		self.server_ip_variable.set("25.82.91.66")
		self.server_ip_entry = tkinter.Entry(self.window, textvariable = self.server_ip_variable)
		self.server_ip_entry.place(x = 300, y = 140, width = 100, height = 20)

		self.server_port_label = tkinter.Label(self.window, text = "Server Port:", anchor = "w")
		self.server_port_label.place(x = 220, y = 170, width = 100, height = 20)

		self.server_port_variable = tkinter.StringVar()
		self.server_port_variable.set("12345")
		self.server_port_entry = tkinter.Entry(self.window, textvariable = self.server_port_variable)
		self.server_port_entry.place(x = 300, y = 170, width = 100, height = 20)

		self.connect_button = tkinter.Button(self.window, text = "Connect", command = self.connect_clicked)
		self.connect_button.place(x = 300, y = 200, width = 100, height = 20)

	def connect_clicked(self):
		self.application_manager.attempt_connection(self.username_variable.get(), self.server_ip_variable.get(), self.server_port_variable.get())

	def show(self):
		self.window.update()
		self.window.deiconify()

	def hide(self):
		self.window.withdraw()

	def close(self):
		self.window.destroy()