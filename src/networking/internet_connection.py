import socket
import threading

from networking.reciever import Reciever
from networking.transmitter import Transmitter

class InternetConnection():

	def __init__(self, uid, socket, new_message_procedure, closing_procedure):
		self.uid = uid
		self.socket = socket
		self.new_message_procedure = new_message_procedure
		self.closing_procedure = closing_procedure
		self.active_lock = threading.Lock()
		self.active = False
		self.transmitter = Transmitter(self.socket, self.connection_lost)
		self.reciever = Reciever(self.socket, self.recieve, self.connection_lost)

	def start(self):
		self.active = True
		self.transmitter.start()
		self.reciever.start()

	def send(self, message):
		self.transmitter.enqueue_message(message)

	def recieve(self, message):
		self.new_message_procedure(self.uid, message)

	def disconnect(self):
		self.active_lock.acquire()
		self.active = False
		self.active_lock.release()

		self.transmitter.stop()
		self.reciever.stop()
		while (not (self.transmitter.is_terminated() and self.reciever.is_terminated())):
			None
		self.socket.close()

	def connection_lost(self):
		action_required = False
		self.active_lock.acquire()
		if (self.active):
			self.active = False
			action_required = True
		self.active_lock.release()

		if (action_required):
			self.disconnect()
			self.closing_procedure(self.uid)

