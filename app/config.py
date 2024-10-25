
def get_version_number():
    with open("VERSION.txt", "r") as f:
        version = f.readline()
    return version

SQLITE_DB_PATH = "app/db/database.db"
SQLITE_DB_TABLE = "urls"
IS_IN_DOCKER = ""
PORT = 8888
APP_NAME = "URL Shortener"
VERSION = get_version_number()
