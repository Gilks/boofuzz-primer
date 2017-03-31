import socket
import threading
import sys

class ThreadedServer(object):
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((self.host, self.port))

	def stob(self, data):
		return bytes(data, encoding='utf8').upper()


	def listen(self):
		self.sock.listen(5)
		while True:
			client, address = self.sock.accept()
			client.settimeout(15)
			threading.Thread(target = self.listenToClient,args = (client,address)).start()

	def listenToClient(self, client, address):
		size = 1024
		while True:
			try:
				data = client.recv(size).upper()
				print(address[0] + ':' + str(address[1]).lower() + ' --- ' + data.decode("utf-8"))
				if data:
					client.send(self.stob("200\n"))
					if self.stob("HELLO") in data:
						client.recv(size).upper()

					else:
						client.send(self.stob("UNRECOGNIZED COMMAND\n"))
				else:
					raise Exception('Client disconnected')
			except:
				client.close()
				return False

if __name__ == "__main__":
	server_address = ("127.0.0.1", 4444)
	print("Waiting for connection on %s:%s." % server_address)
	ThreadedServer(server_address[0],server_address[1]).listen()
