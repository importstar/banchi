from functools import lru_cache
from typing import Dict, Type
import os

from .settings.app import AppSettings
from .settings.base import AppEnvTypes, BaseAppSettings
from .settings.development import DevAppSettings
from .settings.production import ProdAppSettings
from .settings.test import TestAppSettings

environments: Dict[str, Type[AppSettings]] = {
    "dev": DevAppSettings,
    "prod": ProdAppSettings,
    "test": TestAppSettings,
}


@lru_cache
def get_app_settings() -> AppSettings:
    # app_env = BaseAppSettings().APP_ENV
    app_env = os.getenv("APP_ENV", "dev")
    config = environments[app_env]
    return config()


settings = get_app_settings()
