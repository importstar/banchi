from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.exceptions import RequestValidationError

from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from banchi.api.routers.errors.http_error import http_error_handler
from banchi.api.routers.errors.validation_error import http422_error_handler
from banchi.api.routers import init_router

from .core.config import get_app_settings
from banchi.worker.redis_rq import init_rq
from banchi.api import models


def get_application() -> FastAPI:
    settings = get_app_settings()
    settings.configure_logging()
    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    @application.on_event("startup")
    async def startup_event():
        await models.init_beanie(application, settings)
        await init_router(application, settings)

    # init_rq(settings)
    return application
