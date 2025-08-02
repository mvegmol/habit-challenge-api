import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # JWT Settings
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Database
    database_url: str = "postgresql://miguel:123@localhost:5432/habit"

    # App Settings
    app_name: str = "Habit Challenge API"
    debug: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
