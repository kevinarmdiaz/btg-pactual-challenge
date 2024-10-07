"""
This module is responsible for describing internal application errors.
"""

from typing import Any
from starlette import status
from pydantic import UUID4

__all__ = (
    "BaseError",
    "BadRequestError",
    "UnprocessableError",
    "NotFoundError",
    "SubscriptionConflictError",
    "InsufficientBalanceError",
    "NotSubscribedError",
    "DatabaseError",
    "ProcessError",
)


class BaseError(Exception):
    def __init__(
        self,
        *_: tuple[Any],
        message: str = "Error de la aplicación",
        detail: str = "Ha ocurrido un error.",
        instance: str = "",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> None:
        """La clase base para todos los errores personalizados."""

        self.message: str = message
        self.detail: str = detail
        self.instance: str = instance
        self.status_code: int = status_code

        super().__init__(message)

    def to_dict(self) -> dict:
        """Convierte el error en un diccionario para ser utilizado en respuestas JSON."""
        return {
            "error": self.message,
            "detail": self.detail,
            "instance": self.instance,
            "status_code": self.status_code,
        }


class BadRequestError(BaseError):
    """Consider cases when the server can not perform the operation due
    wrong request from the user.
    """

    def __init__(self, *_: tuple[Any], message: str = "Bad request") -> None:
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)


class UnprocessableError(BaseError):
    def __init__(self, *_: tuple[Any], message: str = "Validation error") -> None:
        """Consider cases when the server can not perform the operation due
        any sorts of conditions.
        """

        super().__init__(
            message=message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


class NotFoundError(BaseError):
    """Maneja los casos cuando un recurso no se encuentra para esta operación."""

    def __init__(
        self,
        message: str = "Recurso no encontrado.",
        detail: str = "El recurso solicitado no existe o no está disponible.",
        instance: str = "",
        status_code: int = status.HTTP_404_NOT_FOUND,
    ) -> None:
        super().__init__(
            message=message, detail=detail, instance=instance, status_code=status_code
        )


class SubscriptionConflictError(BaseError):
    """Error para cuando el usuario ya está suscrito a un fondo de inversión."""

    def __init__(
        self,
        message: str = "El usuario ya está suscrito a este fondo de inversión.",
        detail: str = "No se puede realizar la suscripción ya que el usuario ya está suscrito.",
        instance: str = "",
        status_code: int = status.HTTP_409_CONFLICT,
    ) -> None:
        super().__init__(
            message=message, detail=detail, instance=instance, status_code=status_code
        )


class InsufficientBalanceError(BaseError):
    """Error raised when user's balance is not enough to subscribe to a fund."""

    def __init__(
        self,
        balance: int,
        fund_name: str,
        minimum_investment: int,
        instance: str = "",
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        message = (
            f"Su balance: {balance} no es suficiente para suscribirse "
            f"al fondo '{fund_name}' con monto mínimo '{minimum_investment}'"
        )
        super().__init__(
            message=message, detail=message, instance=instance, status_code=status_code
        )


class NotSubscribedError(BaseError):
    """Error raised when the user is not subscribed to a fund."""

    def __init__(
        self,
        user_id: UUID4,
        fund_name: str,
        instance: str = "",
        status_code: int = status.HTTP_404_NOT_FOUND,
    ) -> None:
        message = f"Usuario con ID {user_id} no está suscripto al fondo de inversión '{fund_name}'."
        super().__init__(
            message=message, detail=message, instance=instance, status_code=status_code
        )


class DatabaseError(BaseError):
    """Error raised for issues related to database operations."""

    def __init__(
        self,
        message: str = "Ha ocurrido un error en la base de datos.",
        detail: str = "Error al interactuar con la base de datos.",
        instance: str = "",
        _type: str = "Database Error",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> None:
        super().__init__(
            message=message, detail=detail, instance=instance, status_code=status_code
        )


class ProcessError(BaseError):
    def __init__(
        self, *_: tuple[Any], message: str = "Background process error"
    ) -> None:
        """The error that should be raised by the background process."""

        super().__init__(
            message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
