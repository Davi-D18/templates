from collections.abc import Mapping

from ..messages.env import ENVIRONMENT_INVALID
from .boot import BootSettings
from .development import DevelopmentSettings
from .production import ProductionSettings

_boot = BootSettings()

ALL_ENVIRONMENTS: Mapping[str, type] = {
    "DEVELOPMENT": DevelopmentSettings,
    "PRODUCTION": ProductionSettings,
}

_env_key = _boot.ENVIRONMENT.value.upper()

try:
    Settings = ALL_ENVIRONMENTS[_env_key]
except KeyError as exc:
    raise ValueError(ENVIRONMENT_INVALID) from exc

settings = Settings()

__all__ = ["Settings", "settings"]
