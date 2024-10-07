from fastapi import FastAPI
from loguru import logger

from src.config import settings
from src.infrastructure.application import create as application_factory
from src.initial_data import init
from src.presentation import api_router

# Adjust the logging
# -------------------------------
logger.add(
    "".join(
        [
            str(settings.root_dir),
            "/logs/",
            settings.logging.file.lower(),
            ".log",
        ]
    ),
    format=settings.logging.format,
    rotation=settings.logging.rotation,
    compression=settings.logging.compression,
    level="INFO",
)


# Adjust the application
# -------------------------------
app: FastAPI = application_factory(
    debug=settings.debug,
    app_router=api_router,
    startup_tasks=[init],
    shutdown_tasks=[],
    startup_processes=[],
)
