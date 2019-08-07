import threading
import queue

class AsynchQueue():
	
	def __init__(self):
		self.lock = threading.Lock()
		self.queue = queue.Queue()

	def enqueue(self, message):
		self.lock.acquire()
		self.queue.put(message)
		self.lock.release()

	def dequeue(self):
		data = None
		self.lock.acquire()
		if (not self.queue.empty()):
			data = self.queue.get()
		self.lock.release()
		return data

	def empty(self):
		return self.queue.empty()