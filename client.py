import json
import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

'''User needs to know IP address and port'''
if len(sys.argv) != 3:
	print ("Please, write server data in th following order: script, IP address, port number")
	exit()
IP = str(sys.argv[1])
port = int(sys.argv[2])
server.connect((IP, port))


def prepare_message_for_server(input_line):
	if input_line == "\n":
		return {"to": "server", "text" : 1}
	if input_line.strip()[0]!= "@":
		return {"to":0, "text": input_line }
	to_whom = input_line.strip().split()[0][1:]
	text = input_line.strip()[len(to_whom) + 1:]
	return {"to": to_whom, "text": text}


def decode_message(input_str):
	message = json.loads(input_str.decode())
	if message["from"] == "server":
		return message["text"]
	if message["from"] == "you":
		if message["to"] == 0:
			return "<You>: " + message["text"]
		else:
			return "<You> to <" + message["to"] + ">: " + message["text"]
	if message["from"] == "other":
		if message["to"] == 0:
			return "<" + message["nick"] + ">: " + message["text"]
		else:
			return "<" + message["nick"] + "> to <You>: " + message["text"]


while True:
	sockets_list = [sys.stdin, server]
	read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])

	for sockets in read_sockets:
		if sockets == server:
			new_message = decode_message(sockets.recv(2048))
			print (new_message)
		else:
			new_message = prepare_message_for_server(sys.stdin.readline())
			server.send(json.dumps(new_message).encode())
server.close()

