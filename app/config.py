def get_version_number():
    with open("VERSION.txt", "r") as f:
        version = f.readline()
    return version


SQLITE_DB_PATH = "app/db/database.db"
SQLITE_DB_TABLE = "urls"
IS_IN_DOCKER = ""
FASTAPI_PORT = 8000
DASH_APP_PORT = 8888
API_DOMAIN = f"http://localhost:{FASTAPI_PORT}"
APP_NAME = "URL Shortener"
VERSION = get_version_number()
