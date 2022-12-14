import os

def get_mysql_uri():
	host = os.environ.get("DB_HOST", "localhost")
	port = 3306 if host == "localhost" else 5432
	password = os.environ.get("DB_PASSWORD", "123456")
	user, db_name = "gshot", "intern"
	return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

def get_test_db_uri():
	return "sqlite:///:memory:"

def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5000 if host == "localhost" else 80
    return f"http://{host}:{port}"

def get_dev_db_uri():
	return "sqlite:///C:\\Projects\\InternAPI\\api\\dev.sqlite"