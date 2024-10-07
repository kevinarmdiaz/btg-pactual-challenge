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
async def test_get_all_users(client: AsyncClient):
	"""Test to verify the GET /user endpoint for fetching all users."""
	
	# # Guardar el usuario en la base de datos
	# await new_user.insert()
	# Enviar una solicitud GET al endpoint "/user"
	response = await client.get("/user")
	
	# Verificar que el código de estado sea 200 (OK)
	assert response.status_code == 200
	
	# Obtener la respuesta en formato JSON
	json_data = response.json()
	
	# Verificar que la respuesta contenga los usuarios
	assert "result" in json_data
	
	# Comprobar que la lista de usuarios no está vacía
	assert len(json_data["result"]) > 0
	
	# Obtener todos los usuarios de la base de datos MongoDB para compararlos
	users_in_db = await UsersCollection.find_all().to_list()
	logger.info(users_in_db)
	# Comparar los datos obtenidos de la API con los usuarios en la base de datos
	for i, user in enumerate(users_in_db):
		assert json_data["result"][i]["name"] == user.name
		assert json_data["result"][i]["email"] == user.email
		assert json_data["result"][i]["phone"] == user.phone
		assert json_data["result"][i]["balance"] == user.balance
	
	logger.info("Test for GET /user passed successfully.")
