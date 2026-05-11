from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./ticketing.db"
    API_TITLE: str = "Helpdesk Ticketing System"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()