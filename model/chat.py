from .message import Message

class Chat:
	def __init__(self, ref, member1, member2):
		self.ref = ref
		self.member1 = member1
		self.member2 = member2
		self._messages = []

	def add_message(self, message):
		self._messages.append(message)

	def order_messages_by_date(self):
		pass

	@property
	def get_messages(self):
		return self._messages
	