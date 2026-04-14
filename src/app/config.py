from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = (
        "postgresql://hello_fastapi:hello_fastapi@localhost/hello_fastapi_dev"
    )
    environment: str = "development"
    allowed_origins: str = (
        "http://localhost,http://localhost:8080,http://localhost:5173"
    )
    db_pool_size: int = 5
    db_max_overflow: int = 10
    secret_key: str = "your-secret-key-for-jwt-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
