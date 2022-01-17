import json
import socket
import sys
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
	print ("Please, write the server's data in the following order: script, IP address, port number")
	exit()

IP = str(sys.argv[1])

port = int(sys.argv[2])

'''User needs to know the IP address and the port of the server'''

server.bind((IP, port))
print("Server started")

server.listen(500)

addr_to_nick = {}
nick_to_addr = {}
addr_to_conn = {}


def send_from_server(connection, text):
	connection.send(json.dumps({"from": "server", "text": text}).encode())


def remove_user(address):
	if address in addr_to_conn:
		addr_to_conn.pop(address)
	if address in addr_to_nick.keys():
		nick = addr_to_nick[address]
		addr_to_nick.pop(address)
		nick_to_addr.pop(nick)


def choose_nickname(connection, address):
	NickChosen = False

	while not NickChosen:
		try:
			message = connection.recv(2048)
			if message:
				message = json.loads(message.decode())
				if message["text"] == 1:
					send_from_server(connection, "Empty message!")
					continue
				if message["to"] != 0:
					send_from_server(connection, "nickname can not start with '@' symbol")
					continue
				nick = message["text"].strip().split()[0]
				if not nick in nick_to_addr.keys():
					nick_to_addr[nick] = address
					addr_to_nick[address] = nick
					NickChosen = True
					print(str(address) + " chose nickname <" + nick + ">")
					conrgats = "You chose nickname <" + nick + ">!\nYou can start chatting :)"
					send_from_server(connection, conrgats)
				else:
					send_from_server(connection, "This nickname is already taken, try another")
					continue
			else:
				remove_user(connection)
		except:
			continue


def send_to_all(message, connection):
	for address in addr_to_conn.keys():
		target = addr_to_conn[address]
		try:
			if target != connection:
				message["from"] = "other"
			else:
				message["from"] = "you"
			target.send(json.dumps(message).encode())
		except:
			target.close()
			remove_user(address)


def private_message(message, connection, address):
	target_address = nick_to_addr[message["to"]]
	target = addr_to_conn[target_address]
	if target == connection:
		send_from_server(connection, "Forever alone? :(")
		return
	try:
		message["from"] = "you"
		connection.send(json.dumps(message).encode())
	except:
		connection.close()
		remove_user(address)
	try:
		message["from"] = "other"
		message["nick"] = addr_to_nick[address]
		target.send(json.dumps(message).encode())
	except:
		target.close()
		remove_user(target_address)


def start_user_thread(connection, address):

	send_from_server(connection, "Welcome to the chat!\nPlease, write your nickname")
	choose_nickname(connection, address)

	while True:
			try:
				message = connection.recv(4096)
				if message:
					message = json.loads(message.decode())
					if message["text"] == 1:
						send_from_server(connection, "Empty message!")
						continue
					if message["to"] == 0:
						message["nick"] = addr_to_nick[address]
						send_to_all(message, connection)
						continue
					if not message["to"] in nick_to_addr.keys():
						send_from_server(connection, "There is no user with such nickname!")
						continue
					private_message(message, connection, address)
				else:
					remove_user(connection)
			except:
				continue


while True:
	new_connection, new_address = server.accept()
	addr_to_conn[new_address] = new_connection

	print ("user with address " + str(new_address) + " connected")

	start_new_thread(start_user_thread, (new_connection, new_address))

server.close()

