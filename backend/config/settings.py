from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DATABASE_URL: str
    SYNC_DB_URL: str
    GEMINI_API_KEY : str

    class Config:
        env_file = ".env"
        extra="ignore"

config_settings = Settings()