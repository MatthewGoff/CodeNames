import threading

from networking.messaging.messaging_constants import MessagingConstants
from networking.messaging.message_deserializer import MessageDeserializer

class Reciever():

	def __init__(self, socket, new_message_procedure, closing_procedure):
		self.socket = socket
		self.new_message_procedure = new_message_procedure
		self.closing_procedure = closing_procedure
		self.thread = threading.Thread(target = self.__recieve)
		self.active_lock = threading.Lock()
		self.active = False
		self.terminated_lock = threading.Lock()
		self.terminated = False

		self.message_in_progress = False
		self.escape = False
		self.current_message = b""

	def start(self):
		self.active = True
		self.thread.start()

	def stop(self):
		self.active_lock.acquire()
		self.active = False
		self.active_lock.release()

	def __recieve(self):

		while (self.__is_active()):
			try:
				word = self.socket.recv(4)
			except (BlockingIOError):
				continue
			except (ConnectionResetError):
				self.__terminate_immediately()
				return

			if (word == b""):
				self.__terminate_immediately()
				return
			else:
				self.__process_next_word(word)

		self.terminated_lock.acquire()
		self.terminated = True
		self.terminated_lock.release()

	def __terminate_immediately(self):
		self.active_lock.acquire()
		self.active = False
		self.active_lock.release()
		self.terminated_lock.acquire()
		self.terminated = True
		self.terminated_lock.release()

		self.closing_procedure()

	def __process_next_word(self, word):
		if (self.message_in_progress):
			if (self.escape):
				self.current_message += word
				self.escape = False
			else:
				if (word == MessagingConstants.ESCAPE):
					self.escape = True
				elif (word == MessagingConstants.END_MESSAGE):
					self.message_in_progress = False
					message_length = int.from_bytes(self.current_message[0:4], byteorder = "big")
					message = self.current_message[4:4+message_length]
					self.new_message_procedure(MessageDeserializer.deserialize(message))
				else:
					self.current_message += word
		elif (word == MessagingConstants.BEGIN_MESSAGE):
			self.current_message = b""
			self.message_in_progress = True

	def __is_active(self):
		active = None
		self.active_lock.acquire()
		active = self.active
		self.active_lock.release()
		return active

	def is_terminated(self):
		terminated = None
		self.terminated_lock.acquire()
		terminated = self.terminated
		self.terminated_lock.release()
		return terminated