from dotenv import load_dotenv
import os


load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_NAME = os.environ.get('DB_NAME')
DB_PORT = os.environ.get("DB_PORT")
DB_PASS = os.environ.get("DB_PASS")

DB_HOST_TEST = os.environ.get('DB_HOST_TEST')
DB_USER_TEST = os.environ.get('DB_USER_TEST')
DB_NAME_TEST = os.environ.get('DB_NAME_TEST')
DB_PORT_TEST = os.environ.get('DB_PORT_TEST')
DB_PASS_TEST = os.environ.get('DB_PASS_TEST')

SECRET_AUTH = os.environ.get("SECRET_AUTH")
SECRET_MANAGER = os.environ.get("SECRET_MANAGER")

SMTP_PASS = os.environ.get("SMTP_PASS")
SMTP_USER = os.environ.get("SMTP_USER")

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

