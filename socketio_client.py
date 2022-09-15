import socketio
from json import JSONEncoder, JSONDecoder
from datetime import datetime

decoder = JSONDecoder()

client = socketio.Client()
encoder = JSONEncoder()

user = input("Which user?  ")
chat_id = 0

@client.on("msg")
def message(msg):
	#msg = decoder.decode(msg)
	#print("\n<" + msg["data"])
	print(msg["data"])
	#client.emit("read", {"msg_id": msg["data"]["id"]})

@client.on("read")
def read(data):
	print(data)

@client.on("history")
def get_chats(data):
	print(data)

@client.event
def create(data):
	#data = decoder.decode(data)
	print(data)

@client.event
def chat(data):
	print(data)

@client.event
def create(data):
	print(data)

@client.event
def connect():
	print("user connected")
	#client.emit("join", {"user_id": 1})
	#client.emit("history", {"user_id": 2})
	#client.emit("create", {"members": [2, 3]})
	#client.emit("message", {"chat_id": 2, "sender_id": 3, "content": "How's your chick"})
	#client.emit("chat", encoder.encode({"member": 1}))
	#data = input(">>> ")
	while True:
		data = input(">  ")
		if data == "q":
			break
		client.emit("msg", {"chat_id": 1, "sender_id": int(user), "content": data, "timeStamp": str(datetime.now())})


def start():
	client.connect("http://localhost:5000")

if __name__ == '__main__':
	start()
	#2022-05-11 12:41:33.405583