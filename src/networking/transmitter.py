import threading

from networking.messaging.messaging_constants import MessagingConstants
from util.asynch_queue import AsynchQueue

class Transmitter():

	def __init__(self, socket, closing_procedure):
		self.socket = socket
		self.closing_procedure = closing_procedure
		self.queue = AsynchQueue()
		self.thread = threading.Thread(target = self.__transmit)
		self.active_lock = threading.Lock()
		self.active = False
		self.terminated_lock = threading.Lock()
		self.terminated = False

	def start(self):
		self.active = True
		self.thread.start()

	def stop(self):
		self.active_lock.acquire()
		self.active = False
		self.active_lock.release()

	def enqueue_message(self, message):
		self.queue.enqueue(MessagingConstants.BEGIN_MESSAGE)

		byte_array = message.serialize()
		self.queue.enqueue(len(byte_array).to_bytes(4, byteorder = "big"))
		while (len(byte_array) % 4 != 0):
			byte_array += b"0"

		for i in range(0, len(byte_array), 4):
			word = byte_array[i:i + 4]
			if word in MessagingConstants.RESERVED:
				self.queue.enqueue(MessagingConstants.ESCAPE)
			self.queue.enqueue(word)

		self.queue.enqueue(MessagingConstants.END_MESSAGE)

	def __transmit(self):
		while (self.__is_active()):
			if (not self.queue.empty()):
				try:
					self.socket.sendall(self.queue.dequeue())
				except (ConnectionResetError):
					self.__terminate_immediately()
					return

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