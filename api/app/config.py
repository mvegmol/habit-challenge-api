import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # JWT Settings
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Database
    database_url: str = "postgresql://miguel:123@localhost:5432/habit"

    # OpenWeatherMap API
    openweather_api_key: str = "your-openweather-api-key-here"

    # App Settings
    app_name: str = "Habit Challenge API"
    debug: bool = True

    class Config:
        # Buscar .env en la carpeta padre de app/ (es decir, en api/)
        env_file = Path(__file__).parent.parent / ".env"


settings = Settings()
