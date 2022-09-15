from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from adapters import orm
import pytest


#@pytest.fixture
def create_test_engine():
	engine = create_engine("sqlite:///:memory:")
	orm.metadata.create_all(engine)
	return engine

#@pytest.fixture
def create_session(create_test_engine):
	orm.mappers()
	return sessionmaker(bind=create_test_engine)()
	#clear_mappers()
