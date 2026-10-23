from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql://mlstate:mlstate_test@localhost:55432/mlstate"
    jwt_secret: str = "solo-desarrollo-cambiar-en-produccion"
    jwt_algorithm: str = "HS256"
    access_token_expire_seconds: int = 7200
    anonymous_session_expire_hours: int = 24
    cookie_secure: bool = False
    app_host: str = "127.0.0.1"
    app_port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
