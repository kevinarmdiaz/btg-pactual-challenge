from src.domain.subscriptions import (
    SubscriptionFlat,
    SubscriptionsRepository,
)
from src.infrastructure.mongodb import (
    transaction_mongo,
    UsersCollection,
    FundsCollection,
)


# TODO: change for transaction_mongo


async def get_all() -> list[SubscriptionFlat]:
    """Get all users from the database."""

    async with transaction_mongo():
        return [user async for user in SubscriptionsRepository().all()]


async def suscribe_in_fund(user: UsersCollection, fund: FundsCollection) -> bool:
    """Create a database record for the product."""

    async with transaction_mongo():
        return await SubscriptionsRepository().subscribe_in_fund(user=user, fund=fund)


async def cancel_in_fund(user: UsersCollection, fund: FundsCollection) -> bool:
    """Leave out of the fund"""

    async with transaction_mongo():
        return await SubscriptionsRepository().cancel_in_fund(user=user, fund=fund)
