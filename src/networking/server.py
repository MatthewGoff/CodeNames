import socket
import random
import sys

from networking.internet_connection import InternetConnection
from util.asynch_queue import AsynchQueue
from game.game import Game
from networking.messaging.cm_click import CMClick
from networking.messaging.cm_init_player import CMInitPlayer
from networking.messaging.cm_new_game import CMNewGame
from networking.messaging.cm_new_player import CMNewPlayer
from networking.messaging.sm_click import SMClick
from networking.messaging.sm_init_player import SMInitPlayer
from networking.messaging.sm_overwrite_cards import SMOverwriteCards
from networking.messaging.sm_new_player import SMNewPlayer
from networking.messaging.sm_remove_player import SMRemovePlayer
from networking.messaging.sm_overwrite_players import SMOverwritePlayers

class Server():

	def __init__(self):
		self.message_queue = AsynchQueue()
		self.client_uids = []
		self.client_names = {}
		self.client_connections = {}

	def run(self):
		self.initialize()

		while (True):
			self.accept_new_client()

			message = self.message_queue.dequeue()
			if (message != None):
				self.process_message(message[0], message[1])
				self.display_message(message[0], message[1])

	def process_message(self, uid, message):
		if (isinstance(message, CMClick)):
			self.game.click(message.x_coord, message.y_coord)
			self.broadcast(SMClick(message.x_coord, message.y_coord))
		elif (isinstance(message, CMInitPlayer)):
			self.game.init_player(uid, message.team, message.role)
			self.broadcast(SMInitPlayer(uid, message.team, message.role))
		elif (isinstance(message, CMNewGame)):
			seed = random.randrange(0, 0b1 << 32)
			self.game.deal(seed, message.red, message.blue, message.bystander, message.assassin)
			self.broadcast(SMOverwriteCards(self.game.cards))
		elif (isinstance(message, CMNewPlayer)):
			self.game.new_player(uid, message.name)
			self.client_names[uid] = message.name
			self.broadcast(SMNewPlayer(uid, message.name))
		else:
			print("Unknown message type recieved from client: " + str(uid))

	def display_message(self, uid, message):
		nickname = ""
		if (uid in self.client_names.keys()):
			nickname = " (" + self.client_names[uid] + ")"
		print("Client " + str(uid) + nickname + " says: (" + str(message) + ")")

	def initialize(self):

		self.game = Game()
		self.game.deal(random.randrange(0, 0b1 << 32), 8, 7, 4, 1)

		host_ip = socket.gethostbyname(socket.gethostname())
		port = 12345

		print("Host IP: " + str(host_ip))
		print("Port: " + str(port))

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setblocking(False)
		self.socket.bind((host_ip, port))
		self.socket.listen()

		print("Server is now running...")

	def new_message(self, uid, message):
		self.message_queue.enqueue((uid, message))

	def new_client_uid(self):
		for i in range(0, 1000):
			if i not in self.client_uids:
				self.client_uids += [i]
				return i
		return -1

	def accept_new_client(self):
		try:
			conn, addr = self.socket.accept()
		except (BlockingIOError):
			return

		conn.setblocking(False)
		uid = self.new_client_uid()
		if (uid == -1):
			conn.close()
		else:
			new_connection = InternetConnection(uid, conn, self.new_message, self.client_lost)
			new_connection.start()
			self.client_connections[uid] = new_connection
			print("New client: "+str(uid))

			self.client_connections[uid].send(SMOverwriteCards(self.game.cards))
			self.client_connections[uid].send(SMOverwritePlayers(self.game.get_players()))

	def client_lost(self, uid):
		del self.client_connections[uid]
		self.client_uids.remove(uid)
		nickname = ""
		if (uid in self.client_names.keys()):
			nickname = " (" + self.client_names[uid] + ")"
		print("Lost client: " + str(uid) + nickname)
		del self.client_names[uid]

		self.game.remove_player(uid)
		self.broadcast(SMRemovePlayer(uid))

	def broadcast(self, message):
		for uid in self.client_connections.keys():
			self.client_connections[uid].send(message)

server = Server()
server.run()