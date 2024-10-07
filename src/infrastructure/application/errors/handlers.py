"""
This module is used for representing FastAPI error handlers
that are dispatched automatically by fastapi engine.
"""

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status
from starlette.requests import Request
from .entities import BaseError

__all__ = (
    "custom_base_errors_handler",
    "python_base_error_handler",
    "pydantic_validation_errors_handler",
)

from src.infrastructure.application import ErrorResponse, ErrorResponseMulti


def custom_base_errors_handler(_: Request, error: BaseError) -> JSONResponse:
    """
    This function is called if the BaseError was raised.
    Generates a response compliant with RFC 7807.
    """

    # Crear un ErrorResponse para cada error
    error_response = ErrorResponse(
        message=error.message.capitalize(),
        detail=error.detail,
        instance=error.instance,
        path=[],  # Puedes ajustar esto según corresponda, si tienes un campo que causó el error
    )

    # Crear un ErrorResponseMulti si hay varios errores
    response = ErrorResponseMulti(results=[error_response])

    # Devolver la respuesta con el Content-Type adecuado para RFC 7807
    return JSONResponse(
        content=response.model_dump(by_alias=True),
        status_code=error.status_code,
        headers={"Content-Type": "application/problem+json"},
    )


def python_base_error_handler(_: Request, error: Exception) -> JSONResponse:
    """This function is called if the Exception was raised."""

    response = ErrorResponseMulti(
        results=[ErrorResponse(message=f"Unhandled error: {error}")]
    )

    return JSONResponse(
        content=jsonable_encoder(response.model_dump(by_alias=True)),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def pydantic_validation_errors_handler(
    _: Request, error: RequestValidationError
) -> JSONResponse:
    """This function is called if the Pydantic validation error was raised."""

    response = ErrorResponseMulti(
        results=[
            ErrorResponse(
                message=err["msg"],
                path=list(err["loc"]),
            )
            for err in error.errors()
        ]
    )

    return JSONResponse(
        content=jsonable_encoder(response.model_dump(by_alias=True)),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
