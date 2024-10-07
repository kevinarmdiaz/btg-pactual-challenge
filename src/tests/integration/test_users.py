"""
Test user route
"""
from loguru import logger
from httpx import AsyncClient

from src.config import settings
from src.infrastructure.mongodb import UsersCollection

USER_ENDPOINT = f"{settings.API_V1_STR}/users"


async def test_get_all_users(client: AsyncClient):
    """Test to verify the GET /user endpoint for fetching all users."""

    # Enviar una solicitud GET al endpoint "/user"

    response = await client.get(USER_ENDPOINT)

    assert response.status_code == 200

    json_data = response.json()

    assert "result" in json_data

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
