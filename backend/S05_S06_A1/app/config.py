from functools import lru_cache
from typing import Any

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql://mlstate:mlstate_test@localhost:55432/mlstate"
    jwt_secret: str = "solo-desarrollo-cambiar-en-produccion"
    jwt_algorithm: str = "HS256"
    secret_key: str | None = None
    algorithm: str | None = None
    access_token_expire_seconds: int = 7200
    access_token_expire_minutes: int | None = None
    anonymous_session_expire_hours: int = 24
    cookie_secure: bool = False
    app_host: str = "127.0.0.1"
    app_port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @model_validator(mode="before")
    @classmethod
    def _map_aliases(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if data.get("secret_key") and not data.get("jwt_secret"):
                data["jwt_secret"] = data["secret_key"]
            if data.get("algorithm") and not data.get("jwt_algorithm"):
                data["jwt_algorithm"] = data["algorithm"]
            if data.get("SECRET_KEY") and not data.get("jwt_secret"):
                data["jwt_secret"] = data["SECRET_KEY"]
            if data.get("ALGORITHM") and not data.get("jwt_algorithm"):
                data["jwt_algorithm"] = data["ALGORITHM"]
            if data.get("access_token_expire_minutes") and not data.get("access_token_expire_seconds"):
                data["access_token_expire_seconds"] = int(data["access_token_expire_minutes"]) * 60
        return data

    @property
    def SECRET_KEY(self) -> str:
        return self.jwt_secret

    @property
    def ALGORITHM(self) -> str:
        return self.jwt_algorithm


@lru_cache
def get_settings() -> Settings:
    return Settings()
