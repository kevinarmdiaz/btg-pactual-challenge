from src.domain.users import (
    UserFlat,
    UserRepository,
    UserUncommited,
)
from src.infrastructure.mongodb import transaction_mongo
from pydantic import UUID4


# TODO: change for transaction_mongo


async def get_all() -> list[UserFlat]:
    """Get all users from the database."""

    async with transaction_mongo():
        return [user async for user in UserRepository().all()]


async def suscribe_in_fund(user_id: UUID4, fund_id: UUID4) -> UserFlat:
    """Create a database record for the product."""

    async with transaction_mongo():
        return await UserRepository().suscribe_in_fund(user_id=user_id, fund_id=fund_id)


async def create(schema: UserUncommited) -> UserFlat:
    """Create a database record for the user."""

    async with transaction_mongo():
        return await UserRepository().create(schema)


async def cancel_in_fund(user_id: UUID4, fund_id: UUID4) -> UserFlat:
    """Leave out of the fund"""

    async with transaction_mongo():
        return await UserRepository().cancel_in_fund(user_id=user_id, fund_id=fund_id)
