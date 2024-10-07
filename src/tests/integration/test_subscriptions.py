"""
Test user route
"""
from loguru import logger

import pytest
from httpx import AsyncClient
from httpx import ASGITransport, AsyncClient
from asgi_lifespan import LifespanManager

from src.infrastructure.application import SubscriptionConflictError, DatabaseError
from src.infrastructure.mongodb import UsersCollection, FundsCollection, SubscriptionCollection
from src.initial_data import init
from src.main import app

pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_subscribe_fund(client: AsyncClient):
	"""Prueba para el endpoint /subscribe-fund, para verificar la suscripción a un fondo."""
	
	# Preparar el usuario y el fondo
	user = UsersCollection(name="El Usaurio", email="elsuaurio@example.com", phone="1234567890", balance=1000)
	await user.insert()
	
	fund = FundsCollection(name="Fondo 1", category="AFV", minimum_investment_amount=500)
	await fund.insert()
	
	# Realizar la solicitud POST para suscribirse al fondo
	
	response = await client.post(
		"/subscription/subscribe-fund",
		json={"user_id": str(user.id), "fund_id": str(fund.id)}  # Asumiendo que los parámetros se pasan así
	)
	logger.info(response)

	# Verificar la respuesta
	assert response.status_code == 200
	assert response.json() == True


# @pytest.mark.asyncio
# async def test_populate_must_work(client_test: AsyncClient):
#     async with client_test:
#         response = await client_test.get("api/v1/user")
#         assert response.status_code == 200
#         msg = response.json()
#         assert "message" in msg and msg["message"] == []

# async def test_user_creation():
#     # Prepare the test data
#     await factories.create_user()
#
#     # Perform some operations
#     users_number = await UserRepository().count()
#
#     assert users_number == 1
