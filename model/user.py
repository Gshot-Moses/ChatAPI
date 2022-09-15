from . import chat

class User:
	def __init__(self, identifier, first_name, last_name, title, phone, password):
		self.identifier = identifier
		self.first_name = first_name
		self.last_name = last_name
		self.title = title
		self.phone = phone
		self.password = password
		self._chats = []

	def add_chat(self, chat_obj: chat.Chat):
		self._chats.append(chat_obj)

	@property
	def get_chats(self):
		return self._chats