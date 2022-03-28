import os

from .local_config import *

PROJECT_NAME = "Test"
SERVER_HOST = "https://127.0.0.1:8000"

SECRET_KEY = b"awubsyb872378t^*TG8y68&*&&*8y8yg9POB)*896ft7CR^56dfYUv"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

API_V1_STR = "/api/v1"

# Token 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8

# CORS
BACKEND_CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:4200",
    "http://localhost:3000",
    "http://localhost:8080",
]

# SQLALCHEMY_DATABASE_URI = (
#      f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
# )


DATABASE_URI = f'postgres://{os.environ.get("POSTGRES_USER")}:' \
               f'{os.environ.get("POSTGRES_PASSWORD")}@' \
               f'{os.environ.get("POSTGRES_HOST")}:5432/' \
               f'{os.environ.get("POSTGRES_DB")}'

DATABASE_URI_LOCAL = 'postgres://postgres:Zahita183@localhost:5432/useful_test_tortoise'

USERS_OPEN_REGISTRATION = True

EMAILS_FROM_NAME = PROJECT_NAME
EMAIL_RESET_TOKEN_EXPIRE_HOURS = 48
EMAIL_TEMPLATES_DIR = "src/email-templates/build"
EMAILS_ENABLED = SMTP_HOST and SMTP_PORT and EMAILS_FROM_NAME
EMAIL_TEST_USER = 'test@maio.ru'

APPS_MODELS = [
    "src.app.user.models",
    "src.app.auth.models",
    "src.app.board.models",
    "aerich.models",
]
#
# # Email
# SMTP_TLS = os.environ.get("SMTP_TLS")
# SMTP_PORT = os.environ.get("SMTP_PORT")
# SMTP_HOST = os.environ.get("SMTP_HOST")
# SMTP_USER = os.environ.get("SMTP_USER")
# SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
# EMAILS_FROM_EMAIL = os.environ.get("EMAILS_FROM_EMAIL")
#
# EMAILS_ENABLED = SMTP_HOST and SMTP_PORT and EMAILS_FROM_EMAIL
# EMAIL_TEST_USER = "djwoms@gmail.com"
#
# APPS_MODELS = [
#     "src.app.user.models",
#     "src.app.auth.models",
#     "src.app.board.models",
#     "src.app.blog.models",
#     "aerich.models",
# ]
