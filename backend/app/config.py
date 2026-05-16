from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    DATABASE_URL: str = "sqlite:///./ticketing.db"
    API_TITLE: str = "Helpdesk Ticketing System"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str = "lazanje"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    class Config:
        env_file = ".env"
        case_sensitive = True
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
settings = Settings()