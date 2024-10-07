from src.domain.funds import (
	FundFlat,
	FundRepository,
	FundUncommited,
)
from src.infrastructure.mongodb import transaction_mongo


#TODO: change for transaction_mongo

async def get_all() -> list[FundFlat]:
	"""Get all products from the database."""

	async with transaction_mongo():
		return [fund async for fund in FundRepository().all()]


async def create(schema: FundUncommited) -> FundFlat:
	"""Create a database record for the product."""

	async with transaction_mongo():
		return await FundRepository().create(schema)
