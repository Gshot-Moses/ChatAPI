import random
import string
from utils import strings as s

def generate_api_key():
	choices = string.ascii_letters + string.digits
	choices = list(choices)
	random.shuffle(choices)
	token_list = []
	for i in range(1, 40):
		token_list.append(random.choice(choices))
	token = "".join(token_list)
	return token
	

def check_authorization(header): # header: Dict
	try:
		key = header["Authorization"]
		return key == s.API_KEY
	except KeyError:
		return False