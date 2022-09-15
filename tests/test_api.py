import requests
from utils import config

def test_api_accepts_user_when_token_provided():
	data1 = {"identifier": "ahmed", "first_name": "Ahmed",
		"last_name": "Abakar", "title": "IT",
		"phone": "1234567", "password": "12345"}
	data = {"identifier": "gshot", "first_name": "Moussa",
		"last_name": "Mohaman", "title": "Intern",
		"phone": "1234567", "password": "12345"}
	data2 = {"identifier": "krou", "first_name": "Bayoo",
		"last_name": "Serge", "title": "Intern",
		"phone": "1234567", "password": "12345"}
	url = config.get_api_url()
	response = requests.post(f'{url}/create_user', json=data2,
		headers={"Authorization": "Token e7OFXYTXRAWoS4ZGcbpLTLMyvkYFsv327NXv4if"})
	#print(dir(response))
	print(response.json())
	#assert response.status_code == 201

def test_api_create_user_fails_if_no_token():
	data = {"identifier": "mooo", "first_name": "raph",
		"last_name": "moses", "title": "title",
		"phone": "1234567"}
	url = config.get_api_url()
	response = requests.post(f'{url}/create_user', json=data)
	assert response.status_code == 401
	print(response.json()["message"])

def test_api_create_user_fails_bad_request():
	data = {"first_name": "ghsot",
		"last_name": "moses", "title": "title",
		"phone": "1234567"}
	url = config.get_api_url()
	response = requests.post(f'{url}/create_user', json=data)
	assert response.status_code == 403
	assert response.json()["message"] == "Mauvaise requete"

def test_retrieve_user_success():
	url = config.get_api_url()
	'''data = {"identifier": "moes", "first_name": "raph",
		"last_name": "moses", "title": "title",
		"phone": "1234567"}
	requests.post(f'{url}/create_user', json=data)'''

	response = requests.get(f'{url}/get_user/1')
	print(response.json())
	assert response.status_code == 201
	assert response.json()["user"]["identifier"] == "moes"

def test_api_update_user_success():
	data = {"identifier": "kabal"}
	url = config.get_api_url()
	r = requests.put(f'{url}/update_user/1', json=data)
	assert r.status_code == 200

def test_api_delete_user_success():
	url = config.get_api_url()
	r = requests.delete(f'{url}/delete_user/1')
	assert r.status_code == 204

def test_api_get_all_users_success():
	url = config.get_api_url()
	response = requests.get(f'{url}/users',
		headers={"Authorization": "Token e7OFXYTXRAWoS4ZGcbpLTLMyvkYFsv327NXv4if"})
	assert response.status_code == 200
	print(response.json()["users"])
	assert len(response.json()["users"]) == 1

def test_api_save_ticket_success():
	url = config.get_api_url()
	data = {"creator_id": 1, "title": "Serveur",
	"description": "Pas d'acces au serveur",
	"priority": 1, "type": 1}
	response = requests.post(f'{url}/tickets/create',
		headers={"Authorization": "Token e7OFXYTXRAWoS4ZGcbpLTLMyvkYFsv327NXv4if"},
		json=data)
	print(response.json())
	assert response.status_code == 201

def test_retrieve_tickets_for_user_success():
	url = config.get_api_url()
	response = requests.get(f'{url}/tickets/get_for_user/1',
		headers={"Authorization": "Token e7OFXYTXRAWoS4ZGcbpLTLMyvkYFsv327NXv4if"})
	print(response.json())

def test_history():
	url = config.get_api_url()
	response = requests.get(f'{url}/chats/history/2',
		headers={"Authorization": "Token e7OFXYTXRAWoS4ZGcbpLTLMyvkYFsv327NXv4if"})
	print(response.json())

test_api_accepts_user_when_token_provided()
#test_api_save_ticket_success()
#test_history()
#test_retrieve_tickets_for_user_success()
#test_retrieve_user_success()
#test_api_update_user_success()
#test_api_delete_user_success()
#test_api_create_user_fails_bad_request()
#test_api_create_user_fails_if_no_token()
#test_api_get_all_users_success()