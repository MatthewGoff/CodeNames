import tkinter

class AlertDialog(object):

	def __init__(self, parent, text):
		self.window = tkinter.Toplevel(parent)
		self.window.title("Alert")
		width = 200
		height = 70
		x_offset = int(self.window.winfo_screenwidth()/2 - width/2)
		y_offset = int(self.window.winfo_screenheight()/2 - height/2)
		self.window.geometry(str(width)+"x"+str(height)+"+"+str(x_offset)+"+"+str(y_offset))
		self.window.resizable(False, False)
		self.window.protocol("WM_DELETE_WINDOW", self.close)

		self.label = tkinter.Label(self.window, text = text)
		self.label.place(x = 10, y = 10, width = 180, height = 20)

		self.button = tkinter.Button(self.window, text = "OK", command = self.close)
		self.button.place(x = 75, y = 40, width = 50, height = 20)
		self.window.withdraw()

	def open(self, parent):
		self.window.update()
		self.window.deiconify()
		#self.window.transient(parent)
		self.window.grab_set()
		parent.wait_window(self.window)

	def close(self):
		self.window.destroy()