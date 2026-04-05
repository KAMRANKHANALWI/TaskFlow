from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./taskflow.db"

    # JWT
    SECRET_KEY: str = "change-this-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # App
    APP_NAME: str = "TaskFlow"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
