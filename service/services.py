from typing import List
from adapters.repo import AbstractUserRepo
from adapters.repo import AbstractChatRepo
from adapters.repo import AbstractTicketRepo
from model.user import User
from model.message import Message
from model.ticket import Ticket
from utils import strings, api_key


class UserExist(Exception):
	pass

class UserDontExist(Exception):
	pass

class NoUsersFound(Exception):
	pass

class LoginFailed(Exception):
	pass

def create_user(user: User, repo: AbstractUserRepo) -> int:
	created_user = repo.create_user(user)
	if (created_user is None):
		raise UserExist(strings.USER_EXIST_MESSAGE.format(user.first_name))
	return created_user.id

def get_user_from_id(id: int, repo: AbstractUserRepo) -> User:
	user = repo.get_user_from_id(id)
	if user is None:
		raise UserDontExist(strings.USER_DONT_EXIST_MSG)
	return user

def update_user(id: int, repo: AbstractUserRepo, **kwargs):
	val = repo.update_user(id, **kwargs)
	if val is None:
		raise UserDontExist(strings.USER_DONT_EXIST_MSG)

def delete_user(id: int, repo: AbstractUserRepo):
	val = repo.delete_user(id)
	if val is None:
		raise UserDontExist(strings.USER_DONT_EXIST_MSG)

def get_all_users(repo: AbstractUserRepo) -> List[User]:
	users = repo.list_all_users()
	if len(users) == 0 or users is None:
		raise NoUsersFound(strings.NO_USERS_FOUND)
	return users

def login(identifier: str, password: str, repo: AbstractUserRepo):
	token = api_key.generate_api_key()
	user = repo.login(identifier, password, token)
	if not user:
		raise LoginFailed(strings.LOGIN_FAILED)
	return user, token


def create_chat(repo: AbstractUserRepo, users):
	chat_obj = repo.create_chat(users)
	return chat_obj

def save_message(repo: AbstractChatRepo, sender_id: int, chat_id: int, content: str, timeStamp: str):
	msg = Message(sender_id, content, chat_id, 0, timeStamp)
	id = repo.save_message(msg, chat_id)
	return id

def get_chat_list(repo: AbstractUserRepo, user_id: int):
	chats = repo.get_chat_list(user_id)
	return chats

def get_chat_from_id(repo: AbstractChatRepo, chat_id: int):
	return repo.get_chat_from_id(chat_id)

def mark_msg_read(repo: AbstractChatRepo, msg_id: int):
	repo.mark_msg_read(msg_id)
	return True

#-----------------------Tickets-------------------------------

def save_ticket(repo: AbstractTicketRepo, creator_id, title, description, priority, type):
	tick = Ticket(creator_id, title, description, priority, type)
	id = repo.save_ticket(tick)
	return id

def get_tickets_for_user(repo: AbstractTicketRepo, user_id: int):
	return repo.get_tickets_for_user(user_id)
