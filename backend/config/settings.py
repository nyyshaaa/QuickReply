import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DATABASE_URL: str
    SYNC_DB_URL: str
    GEMINI_API_KEY : str

    class Config:
        # Load .env ONLY in local development
        env_file = ".env" if os.getenv("ENV") != "production" else None
        case_sensitive = True
        extra = "ignore"


config_settings = Settings()