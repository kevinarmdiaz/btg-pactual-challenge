"""
Test user route
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_populate_must_work(client_test: AsyncClient):
    response = await client_test.get("api/v1/user")
    assert response.status_code == 200
    msg = response.json()
    assert "message" in msg and msg["message"] == []


# async def test_user_creation():
#     # Prepare the test data
#     await factories.create_user()
#
#     # Perform some operations
#     users_number = await UserRepository().count()
#
#     assert users_number == 1
