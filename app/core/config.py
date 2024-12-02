from typing import List
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache

# Create db directory in app folder
DB_DIR = Path(__file__).parent.parent / "db"
DB_DIR.mkdir(exist_ok=True)

class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = f"sqlite+aiosqlite:///{DB_DIR}/invoices.db"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_ORIGINS: List[str] = ["http://0.0.0.0:8000"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()