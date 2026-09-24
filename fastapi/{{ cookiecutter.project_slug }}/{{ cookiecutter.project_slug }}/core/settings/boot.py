from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    """Enum com os ambientes disponíveis da aplicação."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"


class BootSettings(BaseSettings):
    """Configurações de inicialização para determinar o ambiente."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ENVIRONMENT: Environment = Environment.DEVELOPMENT
