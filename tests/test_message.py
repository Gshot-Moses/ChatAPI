from adapters.repo import ChatRepo
from model.message import Message
from model.user import User
from model.chat import Chat
from .fixtures import *

def test_save_chat_success(session):
	user1 = User("identifier1", "name1", "name2", 
		"title1", "12345", "password")
	user2 = User("identifier2", "name12", "name22",
		"title1", "12345", "password")
	msg = Message(1, "Follow my lead", 1)
	session.add(user1)
	session.add(user2)
	session.commit()
	chat = Chat(1, 2)
	repo = ChatRepo(session)
	repo.create_chat(1, 2)
	repo.save(msg, 1)
	back = repo.get_all_chats_from_member(1)
	print(back)
	#assert chat == back

engine = create_test_engine()
session = create_session(engine)

test_save_chat_success(session)