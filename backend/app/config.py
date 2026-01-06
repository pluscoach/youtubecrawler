from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Anthropic
    anthropic_api_key: str = ""

    # YouTube
    youtube_api_key: str = ""

    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""

    # Backend
    backend_url: str = "http://localhost:8000"

    # CORS
    frontend_url: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
