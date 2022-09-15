from json import JSONDecoder, JSONEncoder
from datetime import datetime
from flask import Flask, request
from flask_socketio import SocketIO, send, emit, join_room
#from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model.user import User
from model.message import Message
from service import services
from adapters.repo import UserRepo, ChatRepo, TicketRepo
from adapters import orm
from utils import config, strings, api_key, util
#pygame-2.1.2-cp37-cp37m-win32.whl

app = Flask(__name__)
#CORS(app)
app.config["SECRET_KEY"] = "secret_key"
app.config["DEBUG"] = True
socket = SocketIO(app, logger=True, engineio_logger=True, debug=True, cors_allowed_origins="*")
engine = create_engine(config.get_dev_db_uri())
orm.metadata.create_all(engine)
orm.mappers()
session = sessionmaker(bind=engine)
decoder = JSONDecoder()
encoder = JSONEncoder()

clients = {}

@app.route("/create_user", methods=["POST"])
def create_user():
	if not api_key.check_authorization(request.headers):
		return {"message": strings.UNAUTHORIZED_MSG}, strings.Status_Codes.UNAUTHORIZED
	if not request.json:
		return {"message": strings.CHECK_HEADERS}, strings.Status_Codes.BAD_REQUEST_CODE
	try:
		identifier = request.json["identifier"]
		first_name = request.json["first_name"]
		last_name = request.json["last_name"]
		title = request.json["title"]
		phone = request.json["phone"]
		password = request.json["password"]
	except KeyError:
		return {"message": strings.BAD_REQUEST}, strings.Status_Codes.BAD_REQUEST_CODE
	user = User(identifier, first_name,
		last_name, title, phone, password)
	repo = UserRepo(session())
	try:
		id = services.create_user(user, repo)
		return {"message": "success", "user_id": id}, strings.Status_Codes.CREATED
	except services.UserExist as e:
		return {"message": str(e)}, strings.Status_Codes.BAD_REQUEST_CODE

@app.route("/get_user/<int:id>", methods=["GET"])
def get_user(id: int):
	if not api_key.check_authorization(request.headers):
		return {"message": strings.UNAUTHORIZED_MSG}, strings.Status_Codes.UNAUTHORIZED
	repo = UserRepo(session())
	try:
		user = services.get_user_from_id(id, repo)
		return {"message": "success", "user": {"id": user.id, "identifier": user.identifier, "first_name": user.first_name, "last_name": user.last_name, "title": user.title, "phone": user.phone}}, strings.Status_Codes.ACCEPTED
	except services.UserDontExist as e:
		return {"message": str(e)}, strings.Status_Codes.NOT_FOUND

@app.route("/update_user/<int:id>", methods=["PUT"])
def update_user(id):
	if not api_key.check_authorization(request.headers):
		return {"message": strings.UNAUTHORIZED_MSG}, strings.Status_Codes.UNAUTHORIZED
	if not request.json:
		return {"message": strings.CHECK_HEADERS}, strings.Status_Codes.BAD_REQUEST_CODE
	repo = UserRepo(session())
	try:
		services.update_user(id, repo, **request.json)
		return {"message": "success"}, strings.Status_Codes.ACCEPTED
	except services.UserDontExist as e:
		return {"message": str(e)}, strings.Status_Codes.NOT_FOUND

@app.route("/delete_user/<int:id>", methods=["DELETE"])
def delete_user(id: int):
	if not api_key.check_authorization(request.headers):
		return {"message": strings.UNAUTHORIZED_MSG}, strings.Status_Codes.UNAUTHORIZED
	repo = UserRepo(session())
	try:
		services.delete_user(id, repo)
		return {}, strings.Status_Codes.ACCEPTED
	except services.UserDontExist as e:
		return {"message": str(e)}, strings.Status_Codes.NOT_FOUND

@app.route("/users", methods=["GET"])
def get_all_users():
	if not api_key.check_authorization(request.headers):
		return {"message": strings.UNAUTHORIZED_MSG}, strings.Status_Codes.UNAUTHORIZED
	repo = UserRepo(session())
	try:
		users = services.get_all_users(repo)
		return {"message": "success", "data": util.convert_users_to_json(users)}, strings.Status_Codes.ACCEPTED
	except services.NoUsersFound as e:
		return {"message": str(e)}, strings.Status_Codes.NO_CONTENT

@app.route("/login", methods=["POST"])
def login():
	if not api_key.check_authorization(request.headers):
		return {"message": strings.UNAUTHORIZED_MSG}, strings.Status_Codes.UNAUTHORIZED
	if not request.json:
		return {"message": strings.CHECK_HEADERS}, strings.Status_Codes.BAD_REQUEST_CODE
	try:
		identifier = request.json["identifier"]
		password = request.json["password"]
	except KeyError:
		return {"message": strings.BAD_REQUEST}, strings.Status_Codes.BAD_REQUEST_CODE
	repo = UserRepo(session())
	try:
		user, token = services.login(identifier, password, repo)
		return {"message": "success", "data": {"user": util.convert_user_to_json(user), "token": token}}, strings.Status_Codes.ACCEPTED
	except services.LoginFailed as e:
		return {"message": str(e)}, strings.Status_Codes.UNAUTHORIZED

@app.route("/chats/history/<int:id>", methods=["GET"])
def get_all_chats(id: int):
	if not api_key.check_authorization(request.headers):
		return {"message": strings.UNAUTHORIZED_MSG}, strings.Status_Codes.UNAUTHORIZED
	repo = UserRepo(session())
	chats = services.get_chat_list(repo, id)
	if chats:
		chats.reverse()
		return {"status": "success", "data": util.convert_chats_to_json(chats)}, strings.Status_Codes.ACCEPTED
	return {"status": "success", "data": []}, strings.Status_Codes.ACCEPTED

#------------------------Ticket------------------------------

@app.route("/tickets/create", methods=["POST"])
def create_ticket():
	if not api_key.check_authorization(request.headers):
		return {"message": strings.UNAUTHORIZED_MSG}, strings.Status_Codes.UNAUTHORIZED
	try:
		creator_id = request.json["creator_id"]
		title = request.json["title"]
		description = request.json["description"]
		priority = request.json["priority"]
		type = request.json["type"]
	except KeyError:
		return {"message": strings.BAD_REQUEST}, strings.Status_Codes.BAD_REQUEST_CODE
	repo = TicketRepo(session())
	id = services.save_ticket(repo, creator_id, title, description, priority, type)
	return {"message": "success", "id": id}, strings.Status_Codes.CREATED

@app.route("/tickets/get_for_user/<int:user_id>", methods=["GET"])
def get_tickets_for_user(user_id:int):
	if not api_key.check_authorization(request.headers):
		return {"message": strings.UNAUTHORIZED_MSG}, strings.Status_Codes.UNAUTHORIZED
	repo = TicketRepo(session())
	tickets = services.get_tickets_for_user(repo, user_id)
	if len(tickets) == 1:
		return {"message": "success", "tickets": tickets[0]}, strings.Status_Codes.ACCEPTED
	elif len(tickets) == 0:
		return {"message": "success", "tickets": []}, strings.Status_Codes.ACCEPTED
	else: return {"message": "success", "tickets": util.convert_tickets_to_json(tickets)}, strings.Status_Codes.ACCEPTED

@app.after_request
def after_request(response):
	header = response.headers
	header["Access-Control-Allow-Origin"] = "*"
	return response

#----------------Message socketIO-------------------------

@socket.on("msg")
def message(data):
	#print(type(data))
	#data = decoder.decode(data)
	try:
		chat_id = data["chat_id"]
		sender_id = data["sender_id"]
		content = data["content"]
		timeStamp = data["timeStamp"]
	except KeyError:
		emit("msg", {"status": "error", "message": "Check your payload"})
		return
	timeStamp = util.get_datetime_from_str(timeStamp)
	repo = ChatRepo(session())
	message = Message(sender_id, content, chat_id, 0, timeStamp)
	id = services.save_message(repo, sender_id, chat_id, content, timeStamp)
	if id > 0:
		emit("msg", {"status": "success", "data": {"id": id, "sender_id": sender_id, "chat_id": chat_id, "content": message.content, "read": 0, "timeStamp": str(message.timeStamp)}}, broadcast=True)
	else: emit("msg", {"status": "error", "message": "Check your payload"})

@socket.on("create")
def create(data):
	#data = decoder.decode(data)
	try:
		users = data["members"]
	except KeyError:
		emit("create", {"status": "error", "message": "Check your payload"})
		return
	join_room("room1")
	repo = UserRepo(session())
	chat = services.create_chat(repo, users)
	if chat:
		emit("create", {"status": "success", "message": "chat created", "data": util.convert_chat_to_json(chat)}, broadcast=True)
	else: emit("create", {"status": "error", "message": "creation failed, chat exist"}, broadcast=True)

@socket.on("chat")
def get_chat(data):
	try:
		id = data["chat_id"]
	except KeyError:
		emit("chat", {"status": "error", "message": "Check your payload"})
		return
	repo = ChatRepo(session())
	chat = services.get_chat_from_id(id)
	if chat:
		emit("chat", {"status": "success", "message": "Successfully executed", "data": util.convert_chat_to_json(chat)})
	else: emit("chat", {"status": "error", "message": "Chat don't exist"})

@socket.on("read")
def read(data):
	try:
		msg_id = data["msg_id"]
	except KeyError:
		emit("read", {"status": "error", "message": "Check your payload"})
		return
	repo = ChatRepo(session())
	output = services.mark_msg_read(repo, msg_id)
	if output:
		emit("read", {"status": "success", "message": "Message mark read", "data": msg_id})

@socket.on("join")
def join(data):
	clients[data["user_id"]] = request.sid
	#join_room("room1")
	print(clients)

@socket.on("connect")
def connect():
	print("User connected")
	print(request.sid)

@socket.on("disconnect")
def disconnect():
	pass


if __name__ == '__main__':
	socket.run(app)