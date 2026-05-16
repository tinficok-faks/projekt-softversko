from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./ticketing.db"
    API_TITLE: str = "Helpdesk Ticketing System"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()