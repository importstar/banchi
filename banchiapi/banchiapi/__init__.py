from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.exceptions import RequestValidationError

from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from banchiapi.api.errors.http_error import http_error_handler
from banchiapi.api.errors.validation_error import http422_error_handler
from banchiapi.api import init_router

from banchiapi.core.config import get_app_settings
from banchiapi.worker.redis_rq import init_rq
from banchiapi import models


def get_application() -> FastAPI:
    settings = get_app_settings()
    settings.configure_logging()
    application = FastAPI(**settings.fastapi_kwargs)

    def custom_openapi():
        if application.openapi_schema:
            return application.openapi_schema
        openapi_schema = get_openapi(
            # title="Custom title",
            openapi_version="3.0.3",
            # version="2.5.0",
            # summary="This is a very custom OpenAPI schema",
            # description="Here's a longer description of the custom **OpenAPI** schema",
            routes=application.routes,
            title=settings.fastapi_kwargs["title"],
            version=settings.fastapi_kwargs["version"],
        )
        # print("--->", app.openapi_schema)
        application.openapi_schema = openapi_schema
        return application.openapi_schema

    application.openapi = custom_openapi

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
