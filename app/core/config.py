from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "09d25e094faa6ca2556c818"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
