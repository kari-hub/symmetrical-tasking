from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr, ValidationError


class Settings(BaseSettings):
    database_url: str = Field(..., alias="DATABASE_URL")
    secret_key: SecretStr = Field(..., alias="SECRET_KEY")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expiry_minutes: int = Field(..., alias="ACCESS_TOKEN_EXPIRY_MINUTES")

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


def _load_settings() -> Settings:  # type: ignore
    try:
        return Settings(**{})  # for the type checker
    except ValidationError as e:
        raise RuntimeError(
            "failure to load settings from environment (.env or env)."
            f"validation errors: {e.errors()}"
        ) from e


settings = _load_settings()
