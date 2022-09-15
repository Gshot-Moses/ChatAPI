from typing import List
from adapters.repo import AbstractUserRepo, UserRepo
from model.user import User
from service import services
from utils import strings
from .fixtures import *


class FakeUserRepo(AbstractUserRepo):
	def __init__(self, users: List[User]):
		self.users = users
		self.id = 0

	def create_user(self, user):
		try:
			check = next(user_check for user_check in self.users if user_check.identifier == user.identifier)
			raise services.UserExist(strings.USER_EXIST_MESSAGE.format(user.first_name))
		except StopIteration:
			self.users.append(user)
			return user

	def login(self, identifier: str, password: str):
		pass


def test_services_throws_exception_if_user_exist(session):
	users = [User("moes", "moussa", 
		"mohaman", "Intern", 
		"656994491")]
	repo = UserRepo(session)       #FakeUserRepo(users)
	services.create_user(users[0], repo)
	try:
		services.create_user(users[0], repo)
	except services.UserExist as e:
		print(e)

def test_services_create_user_succeed(session):
	#users = []
	user = User("moes", "moussa", 
		"mohaman", "Intern", 
		"656994491")
	repo = UserRepo(session)		#FakeUserRepo(users)
	id = services.create_user(user, repo)
	print(id)
	assert id == 1

def test_service_get_user_throws_exception(session):
	repo = UserRepo(session)
	try:
		services.get_user_from_id(1, repo)
	except services.UserDontExist as e:
		print(e)

def test_service_retrieve_user_success(session):
	user = User("moes", "moussa", 
		"mohaman", "Intern", 
		"656994491")
	repo = UserRepo(session)
	repo.create_user(user)
	expected = repo.get_user_from_id(1)
	assert expected == user

def test_service_update_user_success(session):
	user = User("moes", "moussa", 
		"mohaman", "Intern", 
		"656994491")
	repo = UserRepo(session)
	repo.create_user(user)
	update = {"identifier": "andore"}
	services.update_user(1, repo, **update)

def test_service_update_user_fail(session):
	repo = UserRepo(session)
	try:
		services.update_user(2, repo, identifier="town")
	except services.UserDontExist as e:
		print(e)

def test_service_delete_user_success(session):
	user = User("moes", "moussa", 
		"mohaman", "Intern", 
		"656994491")
	repo = UserRepo(session)
	repo.create_user(user)

	services.delete_user(1, repo)

def test_service_delete_user_fail(session):
	user = User("moes", "moussa", 
		"mohaman", "Intern", 
		"656994491")
	repo = UserRepo(session)
	repo.create_user(user)

	try:
		services.delete_user(2, repo)
	except services.UserDontExist as e:
		print(e)

def test_services_raise_exception_when_no_user(session):
	repo = UserRepo(session)
	try:
		services.get_all_users(repo)
	except services.NoUsersFound as e:
		print(e)

def test_service_returns_all_users_success(session):
	user = User("moes", "moussa", 
		"mohaman", "Intern", 
		"656994491")
	repo = UserRepo(session)
	repo.create_user(user)

	users = services.get_all_users(repo)
	assert users == [user]

engine = create_test_engine()
session = create_session(engine)

#test_services_throws_exception_if_user_exist(session)
#test_services_create_user_succeed(session)
#test_service_get_user_throws_exception(session)
#test_service_retrieve_user_success(session)
#test_service_update_user_success(session)
#test_service_update_user_fail(session)
#test_service_delete_user_success(session)
#test_service_delete_user_fail(session)
#test_services_raise_exception_when_no_user(session)
test_service_returns_all_users_success(session)