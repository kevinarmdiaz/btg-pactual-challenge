from typing import Callable, Coroutine, Iterable

from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from . import processes
from src.infrastructure.application.errors import (
    pydantic_validation_errors_handler,
    custom_base_errors_handler,
    BaseError,
    python_base_error_handler,
)

__all__ = ("create",)

from ...config import settings


def create(
    *_,
    app_router: APIRouter,
    startup_tasks: Iterable[Callable[[], Coroutine]] | None = None,
    shutdown_tasks: Iterable[Callable[[], Coroutine]] | None = None,
    startup_processes: Iterable[processes._ProcessBlock] | None = None,
    **kwargs,
) -> FastAPI:
    """The application factory using FastAPI framework.
    🎉 Only passing routes is mandatory to start.
    """

    # Initialize the base FastAPI application
    app = FastAPI(**kwargs)

    # Include REST API routers

    app.include_router(app_router, prefix=settings.API_V1_STR)

    # Extend FastAPI default error handlers
    app.exception_handler(RequestValidationError)(pydantic_validation_errors_handler)
    app.exception_handler(BaseError)(custom_base_errors_handler)
    app.exception_handler(ValidationError)(pydantic_validation_errors_handler)
    app.exception_handler(Exception)(python_base_error_handler)
    
    @app.get("/health")
    async def health_check():
        """

        :return:
        """
        return {"status": "ok"}

    @app.on_event("startup")
    async def startup_event():
        """Run startup tasks."""
        if startup_tasks:
            for task in startup_tasks:
                await task()

        # Define startup processes
        if startup_processes:
            for callback, namespace, key in startup_processes:
                processes.run(namespace=namespace, key=key, callback=callback)

    @app.on_event("shutdown")
    async def shutdown_event():
        """Run shutdown tasks."""
        if shutdown_tasks:
            for task in shutdown_tasks:
                await task()

    return app
