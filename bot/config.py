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

    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT")

    @property
    def DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}' \
               f'@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
