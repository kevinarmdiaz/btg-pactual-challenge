"""
Test user route
"""
from loguru import logger
import pytest
from httpx import AsyncClient

from src.config import settings
from src.infrastructure.mongodb import UsersCollection, FundsCollection


pytestmark = pytest.mark.asyncio

SUBSCRIPTIONS_ENDPOINT = f"{settings.API_V1_STR}/subscriptions/"


@pytest.mark.asyncio
async def test_subscribe_fund(client: AsyncClient):
    """Prueba para el endpoint /subscribe-fund, para verificar la suscripción a un fondo."""

    # Preparar el usuario y el fondo
    user = UsersCollection(
        name="El Usaurio",
        email="elsuaurio@example.com",
        phone="1234567890",
        balance=1000,
    )
    await user.insert()

    fund = FundsCollection(
        name="Fondo 1", category="AFV", minimum_investment_amount=500
    )
    await fund.insert()

    response = await client.post(
        f"{SUBSCRIPTIONS_ENDPOINT}subscribe-fund",
        json={"user_id": str(user.id), "fund_id": str(fund.id)},
    )
    logger.info(response)

    # Verificar la respuesta
    assert response.status_code == 200
    assert response.json() is True
