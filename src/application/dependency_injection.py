from src.domain.funds import FundRepository
from src.domain.users import UserRepository
from src.infrastructure.application.errors import NotFoundError
from src.infrastructure.mongodb import (
    FundsCollection,
    transaction_mongo,
    UsersCollection,
)
from fastapi import status

from src.presentation.subscriptions.v1.contracts import SubscriptionRequestBody


async def get_fund(
    request: SubscriptionRequestBody,
) -> FundsCollection:
    """
    Obtener un fondo de inversión por su ID.
    """

    async with transaction_mongo():
        fund = await FundRepository()._get(
            key="_id",
            value=request.fund_id,
        )
        if not fund:
            raise NotFoundError(
                message="Fondo de inversión no encontrado",
                detail=f"No se encontró el fondo con ID: {request.fund_id}",
                status_code=status.HTTP_404_NOT_FOUND,
                instance=f"/fund/{request.fund_id}",
            )
        return fund


async def get_user(request: SubscriptionRequestBody) -> UsersCollection:
    """

    :param user:
    :return:
    """
    async with transaction_mongo():
        user = await UserRepository()._get(key="_id", value=request.user_id)
        if not user:
            raise NotFoundError(
                message="Usuario no encontrado",
                detail=f"No se encontró el usuario con ID: {request.fund_id}",
                status_code=status.HTTP_404_NOT_FOUND,
                instance=f"/user/{request.fund_id}",
            )
        return user
