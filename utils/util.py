import datetime as dt


def generate_chat_ref(num):
	output = "CH"
	if len(str(num)) == 1:
		output = "CH00" + str(num)
	elif len(str(num)) == 2:
		output = "CH0" + str(num)
	return output

def parse_chat_ref(ref):
	data = ref[2:]
	return int(data)

def convert_chats_to_json(chats):
	data = []
	for chat in chats:
		output = {}
		print("This is the id", chat.id)
		output["id"] = chat.id
		output["ref"] = chat.ref
		output["member1"] = chat.member1
		output["member2"] = chat.member2
		try:
			output["messages"] = convert_message_to_list(chat.get_messages)
		except Exception as e:
			print(e)
			output["messages"] = []
		data.append(output)
	return data

def convert_chat_to_json(chat):
	output = {}
	output["id"] = chat.id
	output["ref"] = chat.ref
	output["member1"] = chat.member1
	output["member2"] = chat.member2
	try:
		output["messages"] = convert_message_to_list(chat.get_messages)
	except Exception as e:
		print(e)
		output["messages"] = []
	return output


def convert_message_to_list(messages):
	output = []
	for message in messages:
		data = {}
		data["id"] = message.id
		data["sender_id"] = message.sender_id
		data["content"] = message.content
		data["chat_id"] = message.chat_id
		data["read"] = message.read
		data["timeStamp"] = str(message.timeStamp)
		output.insert(0, data)
	return output

def convert_tickets_to_json(tickets):
	output = []
	for ticket in tickets:
		data = {}
		data["id"] = ticket.id
		data["creator_id"] = ticket.creator_id
		data["title"] = ticket.title
		data["description"] = ticket.description
		data["type"] = ticket.type
		data["priority"] = ticket.priority
		output.append(data)
	return output



def convert_user_to_json(user):
	output = {}
	output["id"] = user.id
	output["identifier"] = user.identifier
	output["first_name"] = user.first_name
	output["last_name"] = user.last_name
	output["title"] = user.title
	output["phone"] = user.phone
	return output

def convert_users_to_json(users):
	output = []
	for user in users:
		temp = {}
		temp["id"] = user.id
		temp["first_name"] = user.first_name
		temp["identifier"] = user.identifier
		temp["last_name"] = user.last_name
		temp["password"] = user.password
		temp["phone"] = user.phone
		temp["title"] = user.title
		output.insert(0, temp)
	return output

def get_datetime_from_str(value):
	date, time = value.split(" ")
	yr, mth, dy = date.split("-")
	hr, mins, sec_milli = time.split(":")
	sec, milli = sec_milli.split(".")
	return dt.datetime(
		int(yr), int(mth), int(dy), int(hr), 
		int(mins), int(sec), int(milli))
