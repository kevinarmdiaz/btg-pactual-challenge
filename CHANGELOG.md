# ♻️ Changelog

All notable changes to this project will be documented in this file.

The format used in this document is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.1.10] (2023-05-03)

### Added

- Dockerized project.
- Add new schema `CommonHTTPError` for common HTTP error response models in OpenAPI spec.
- Use `UTC` time in `structlog.processors.TimeStamper` processor.
- Add `UVICORN_HOST` and `UVICORN_PORT` as required environment variables to be explicitly
set by user.

### Removed

- Removed flake8 and autopep8 pre-commit hooks.
- Removed `charliermarsh.ruff` extension from VSCode's recommended extensions.
- Removed `scripts/test` script.
- Removed `LOG_FILE_PATH` environment variable and support for log files

### Changed

- Removed `@app.on_event("...")` functions and use `lifespan` feature instead:

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI

@asynccontextmanager
async def lifespan(application: FastAPI):  # noqa
    # On startup
    yield
    # On shutdown


app = FastAPI(
  ...,
  lifespan=lifespan,
)
```

- Set pre-commit ci autoupdate schedule to `monthly`.
- Clean up README file and add instructions for using `Docker`.
- Use enum for validation of `LOG_LEVEL` environment variable instead of pydantic validator.
- Use `structlog.stdlib.BoundLogger` bound logger as `wrapper_class` for all structlog
loggers that we get from calling `structlog.get_logger()`.