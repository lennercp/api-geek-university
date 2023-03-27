from typing import List
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://lenner:mg1qD7C28e4xrr73qb6p2SZKC33xS4Va@dpg-cggu2kseoogqfc4kag10-a.ohio-postgres.render.com/faculdade'
    DBBaseModel = declarative_base()

    JWT_SECRET: str = 'QBseKsK3seN1mmZ-poqnXW3i0vedjcavdP8IDYtsPho'
    ALGORITHM: str = 'HS256'
    ACESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True

settings: Settings = Settings()