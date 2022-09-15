from __future__ import annotations
import abc
from model import user as userModel
from model import message, chat, ticket
from model import token as t
from utils import util

class AbstractUserRepo(abc.ABC):
	@abc.abstractmethod
	def create_user(self, user: user.User):
		raise NotImplementedError

	@abc.abstractmethod
	def login(self, identifier: str, password: str):
		raise NotImplementedError

	@abc.abstractmethod
	def list_all_users(self):
		raise NotImplementedError


class AbstractChatRepo():
	@abc.abstractmethod
	def save_message(self, msg: message.Message, chat_id: int):
		raise NotImplementedError


class AbstractTicketRepo():

	@abc.abstractmethod
	def save_ticket(tick: ticket.Ticket):
		raise NotImplementedError

	@abc.abstractmethod
	def get_ticket(id: int):
		raise NotImplementedError

	@abc.abstractmethod
	def get_tickets_for_user(user_id: int):
		raise NotImplementedError


class TicketRepo(AbstractTicketRepo):
	def __init__(self, session):
		self.session = session

	def save_ticket(self, tick: ticket.Ticket):
		self.session.add(tick)
		self.session.commit()
		id = self._get_ticket_from_creator_and_title_and_description(
			tick.creator_id, tick.title, tick.description
		).id
		return id

	def get_ticket(id: int):
		return self._get_ticket_from_db(id)

	def _get_ticket_from_creator_and_title_and_description(
		self, creator_id: int, title: str, description: str):
		return self.session.query(ticket.Ticket).filter_by(creator_id=creator_id).filter_by(
			title=title	
		).filter_by(description=description).first()

	def _get_ticket_from_db(id: int):
		return self.session.query(ticket.Ticket).filter_by(id=id).first()

	def get_tickets_for_user(self, user_id: int):
		return self.session.query(ticket.Ticket).filter_by(creator_id=user_id).all()

class UserRepo(AbstractUserRepo):
	def __init__(self, session):
		self.session = session

	def create_user(self, user: userModel.User) -> userModel.User:
		if (self.check_user_exist(user)):
			self.session.add(user)
			self.session.commit()
			return self.get_user(user.identifier)
		return None

	def update_user(self, id: int, **kwargs):
		user = self.get_user_from_id(id)
		if user is None:
			return None
		for key in kwargs.keys():
			if key == "identifier":
				user.identifier = kwargs["identifier"]
			elif key == "first_name":
				user.first_name = kwargs["first_name"]
			elif key == "last_name":
				user.last_name = kwargs["last_name"]
			elif key == "title":
				user.title = kwargs["title"]
			elif key == "phone":
				user.phone = kwargs["phone"]
			elif key == "password":
				user.password = kwargs["password"]
		self.session.commit()
		return 1

	def delete_user(self, id: int) -> int:
		user = self.get_user_from_id(id)
		if user is None:
			return None
		self.session.query(userModel.User).filter_by(id=id).delete()
		self.session.commit()
		return 1

	def list_all_users(self):
		return self.session.query(userModel.User).all()

	def get_user(self, identifier: str):
		return self.session.query(userModel.User).filter_by(identifier=identifier).first()

	def get_user_from_id(self, id: int):
		return self.session.query(userModel.User).filter_by(id=id).first()

	def login(self, identifier: str, password: str, token: str):
		if (self.get_user_from_id_and_password(identifier, password)):
			user = self.get_user(identifier)
			token_obj = t.LoginToken(user.id, token)
			self.session.add(token_obj)
			self.session.commit()
			return user
		return None

	def check_user_exist(self, user: userModel.User) -> bool:
		return self.get_user(user.identifier) == None

	def get_user_from_id_and_password(self, identifier: str, password: str) -> bool:
		return self.session.query(userModel.User).filter_by(identifier=identifier).filter_by(password=password).first() is not None

	def create_chat(self, users):
		check = self.get_chat_from_members(users[0], users[1])
		#print(check)
		if check:
			return None
		user1 = self.get_user_from_id(users[0])
		user2 = self.get_user_from_id(users[1])
		val = self.get_latest_chat_ref()
		if val:
			num = util.parse_chat_ref(val)
			ref = util.generate_chat_ref(num + 1)
		else:
			ref = util.generate_chat_ref(1)
		print(ref)
		chat_obj = chat.Chat(ref, user1.id, user2.id)
		user1.add_chat(chat_obj)
		user2.add_chat(chat_obj)
		self.session.commit()
		output = self.get_chat_from_name(ref)
		return output

	def get_chat_from_name(self, ref: str):
		return self.session.query(chat.Chat).filter_by(ref=ref).first()

	def get_latest_chat_ref(self):
		try:
			val = self.session.query(chat.Chat).all()[::-1][0].ref
			return val
		except IndexError:
			return None

	def get_chat_from_members(self, member1, member2):
		user = self.session.query(chat.Chat).filter_by(member1=member1).filter_by(member2=member2).first()
		if not user:
			return self.session.query(chat.Chat).filter_by(member1=member2).filter_by(member2=member1).first()
		return user

	def get_chat_list(self, user_id: int):
		user = self.get_user_from_id(user_id)
		return user.get_chats


class ChatRepo(AbstractChatRepo):
	def __init__(self, session):
		self.session = session

	def save_message(self, msg: message.Message, chat_id: int):
		chat_obj = self.get_chat_from_id(chat_id)
		chat_obj.add_message(msg)
		self.session.commit()
		id = self.get_msg_from_timeStamp(msg.timeStamp, msg.sender_id, chat_id).id
		return id

	def mark_msg_read(self, msg_id: int):
		msg = self.get_msg_from_id(msg_id)
		msg.read = 1
		self.session.commit()

	def get_msg_from_timeStamp(self, timeStamp, sender_id, chat_id):
		return self.session.query(message.Message).filter_by(timeStamp=timeStamp).filter_by(sender_id=sender_id).first()

	def get_msg_from_id(self, msg_id):
		return self.session.query(message.Message).filter_by(id=msg_id).first()

	def get_chat_from_id(self, id: int) -> chat.Chat:
		return self.session.query(chat.Chat).filter_by(id=id).first()
