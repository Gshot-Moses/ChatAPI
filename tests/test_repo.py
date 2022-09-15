from model.user import User
#from model import user
from adapters.repo import UserRepo
from .fixtures import *

def test_repo_create_user_success(create_session):
	expected_user = User("moes", "moussa", 
		"mohaman", "Intern", 
		"656994491")
	repo = UserRepo(create_session)
	user = repo.create_user(expected_user)
	assert expected_user == user

def test_repo_create_user_fail_if_user_exist(create_session):
	repo = UserRepo(create_session)
	create_user(repo)
	value = repo.create_user(user1)
	assert value is None

def test_get_user_from_id_success(create_session):
	user1 = User("diaby", "souley",
		"issa", "Intern", "123456789")
	repo = UserRepo(create_session)
	repo.create_user(user1)

	returned_user = repo.get_user_from_id(1)
	assert user1 == returned_user

def test_get_user_from_id_fails(create_session):
	repo = UserRepo(create_session)
	returned_user = repo.get_user_from_id(1)
	assert returned_user is None

def test_update_user_success(create_session):
	repo = UserRepo(create_session)
	create_user(repo)
	updates = {"identifier": "town", "first_name": "andore"}
	repo.update_user(1, identifier=updates["identifier"],
		first_name=updates["first_name"])
	user = repo.get_user_from_id(1)
	assert user.identifier == updates["identifier"]

def test_repo_get_all_users_success(create_session):
	repo = UserRepo(create_session)
	user1 = create_user(repo)
	user = User("monstre", "dragon",
		"cosmos", "intern", "12345678")
	user2 = repo.create_user(user)
	all_users = repo.list_all_users()
	assert all_users == [user1, user2]

def test_repo_delete_user_success(create_session):
	repo = UserRepo(create_session)
	create_user(repo)
	delete = repo.delete_user(1)
	assert delete == 1

def create_user(repo):
	user1 = User("diaby", "souley",
		"issa", "Intern", "123456789")
	return repo.create_user(user1)

engine = create_test_engine()
session = create_session(engine)

#test_repo_create_user_success(session)
#test_repo_create_user_fail_if_user_exist(session)
#test_get_user_from_id_success(session)
#test_get_user_from_id_fails(session)
#test_update_user_success(session)
#test_repo_delete_user_success(session)
test_repo_get_all_users_success(session)