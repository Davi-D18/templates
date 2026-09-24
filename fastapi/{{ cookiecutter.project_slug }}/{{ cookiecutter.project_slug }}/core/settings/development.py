from .base import BaseSettings


class DevelopmentSettings(BaseSettings):
    """Configurações específicas para o ambiente de desenvolvimento."""

    DEBUG: bool = True
