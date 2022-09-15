from sqlalchemy import Table, MetaData, Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import mapper, relationship
from datetime import datetime
from model import user, message, token, chat, ticket

metadata = MetaData()

users = Table(
	"users",
	metadata,
	Column("id", Integer, primary_key=True, autoincrement=True),
	Column("identifier", String(255)),
	Column("first_name", String(255)),
	Column("last_name", String(255)),
	Column("title", String(255)),
	Column("phone", String(9)),
	Column("password", String(50)),
	Column("creation_date", Date(), server_default=str(datetime.now()))
)

messages = Table(
	"messages",
	metadata,
	Column("id", Integer, primary_key=True, autoincrement=True),
	Column("sender_id", ForeignKey("users.id")),
	Column("content", String(500)),
	Column("read", Integer),
	Column("timeStamp", DateTime(), server_default=str(datetime.now()))
)

msg_recipient = Table(
	"message_recipient",
	metadata,
	Column("id", Integer, primary_key=True, autoincrement=True),
	Column("message_id", ForeignKey("messages.id")),
	Column("chat_id", ForeignKey("chats.id"))
)

tokens = Table(
	"tokens",
	metadata,
	Column("id", Integer, primary_key=True, autoincrement=True),
	Column("user_id", ForeignKey("users.id")),
	Column("token", String(10))
)

user_chat_ref = Table(
	"user_chat_ref",
	metadata,
	Column("id", Integer, primary_key=True ,autoincrement=True),
	Column("user_id", ForeignKey("users.id")),
	Column("chat_id", ForeignKey("chats.id"))
)

chats = Table(
	"chats",
	metadata,
	Column("id", Integer, primary_key=True, autoincrement=True),
	Column("ref", String(200)),
	Column("member1", Integer),
	Column("member2", Integer),
	Column("creation_date", DateTime(), server_default=str(datetime.now())),
)

tickets = Table(
	"tickets",
	metadata,
	Column("id", Integer, primary_key=True, autoincrement=True),
	Column("creator_id", Integer),
	Column("title", String(200)),
	Column("description", String(500)),
	Column("priority", Integer),
	Column("type", Integer),
)

def mappers():
	message_mapper = mapper(message.Message, messages)
	chat_mapper = mapper(
		chat.Chat, 
		chats, 
		properties={
			"_messages": relationship(
				message_mapper,
				secondary=msg_recipient
			)
		})
	user_mapper = mapper(
		user.User, 
		users,
		properties={
			"_chats": relationship(
				chat_mapper,
				secondary=user_chat_ref
			)
		}
	)
	token_mapper = mapper(token.LoginToken, tokens)
	ticket_mapper = mapper(ticket.Ticket, tickets)