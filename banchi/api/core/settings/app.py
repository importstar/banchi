import logging
import sys
from typing import Any, Dict, List, Tuple

from loguru import logger

from banchi.api.core.logging import InterceptHandler
from banchi.api.core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    DEBUG: bool = False
    DOCS_URL: str = "/docs"
    OPENAPI_PREFIX: str = ""
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    TITLE: str = "Banchi"
    VERSION: str = "0.0.2"

    MONGODB_URI: str = "mongodb://localhost/banchidb"
    # MONGODB_DB: str = "banchaidb"
    # MONGODB_HOST: str = "localhost"
    # MONGODB_PORT: int = 27017
    # MONGODB_USERNAME: str = ""
    # MONGODB_PASSWORD: str = ""

    BANCHI_API_BASE_URL: str = ""
    BANCHI_USERNAME: str = ""
    BANCHI_PASSWORD: str = ""
    BANCHI_API_VERIFY_SSL: bool = False

    REDIS_URL: str = "redis://localhost:6379"

    SECRET_KEY: str = "secret"

    API_PREFIX: str = ""

    JWT_TOKEN_PREFIX: str = "Token"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15   # 15 minute
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60  # 7 days

    ALLOWED_HOSTS: List[str] = ["*"]

    LOGGING_LEVEL: int = logging.INFO
    LOGGERS: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    class Config:
        validate_assignment = True
        extra = "allow"

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.DEBUG,
            "docs_url": self.DOCS_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "title": self.TITLE,
            "version": self.VERSION,
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.LOGGERS:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.LOGGING_LEVEL)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.LOGGING_LEVEL}])
