from typing import List
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from os import getenv

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://lenner:mg1qD7C28e4xrr73qb6p2SZKC33xS4Va@dpg-cggu2kseoogqfc4kag10-a/faculdade'
    DBBaseModel = declarative_base()

    JWT_SECRET: str = getenv(JWT_SECRET)
    ALGORITHM: str = 'HS256'
    ACESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True

settings: Settings = Settings()