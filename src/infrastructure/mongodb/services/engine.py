from functools import lru_cache
from motor.motor_asyncio import AsyncIOMotorClient
from mongomock_motor import AsyncMongoMockClient

from src.config import settings


@lru_cache(maxsize=1)
def create_motor_client() -> AsyncIOMotorClient:
    """Create a new async motor client unique
    """
    return AsyncIOMotorClient(str(settings.MONGODB_URI),  uuidRepresentation='standard')


# def create_test_motor_client() -> AsyncMongoMockClient:
#     return AsyncMongoMockClient()

