import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv(override=True)

class EnvironmentVariables(Enum):
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    REDIS_USER = os.getenv('REDIS_USER')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    REDIS_PORT = os.getenv('REDIS_PORT')
    REDIS_HOST = os.getenv('REDIS_HOST')
    JWT_SECRET = os.getenv('JWT_SECRET')
    SUPERUSER_LOGIN = os.getenv('SUPERUSER_LOGIN')
    SUPERUSER_PASSWORD = os.getenv('SUPERUSER_PASSWORD')
    TEST_USER = os.getenv('TEST_USER')
    TEST_USER_PASSWORD = os.getenv('TEST_USER_PASSWORD')
    FILE_SAVE_ROOT = os.getenv('FILE_SAVE_ROOT')
