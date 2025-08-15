from pydantic_settings import BaseSettings
import os
from functools import lru_cache

class TestSettings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "test_secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    openweather_api_key: str = "test_api_key"
