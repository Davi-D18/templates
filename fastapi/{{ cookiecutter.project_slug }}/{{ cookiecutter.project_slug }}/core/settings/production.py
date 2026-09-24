from .base import BaseSettings


class ProductionSettings(BaseSettings):
    """Configurações específicas para o ambiente de produção."""

    DEBUG: bool = False

    # CORS / hosts (strings separadas por vírgula)
    CORS_ORIGINS: str = ""
    CORS_METHODS: str = "*"
    CORS_HEADERS: str = "*"
    ALLOWED_HOSTS: str = ""
