from typing import AsyncGenerator
from pydantic import UUID4
from src.infrastructure.mongodb import BaseRepository, FundsCollection

from .entities import FundFlat, FundUncommited

__all__ = ("FundRepository",)


class FundRepository(BaseRepository[FundsCollection]):
    schema_class = FundsCollection

    async def all(self) -> AsyncGenerator[FundFlat, None]:
        """
            +5+56
        """
        async for instance in self._all():
            yield instance

    async def get(self, id_: UUID4) -> FundsCollection:
        """

        :param id_:
        :return:
        """
        instance = await self._get(key="_id", value=id_)
        return instance

    async def create(self, schema: FundUncommited) -> FundFlat:
        instance: FundsCollection = await self._save(schema.model_dump())
        return None
