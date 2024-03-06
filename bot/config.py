import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    class Config:
        env_file = '.env'

    NAME: str = os.getenv("NAME")

    TOKEN: str = os.getenv("TOKEN")

    DEFAULT_LOCALE: str = os.getenv("DEFAULT_LOCALE")

