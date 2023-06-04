import os
from pydantic import BaseSettings
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
load_dotenv()
class Settings(BaseSettings):
    DB_URL: str = os.getenv("DB_URL")
    DBBaseModel = declarative_base()

    class Config:
        case_sensitive = True


settings: Settings = Settings()
