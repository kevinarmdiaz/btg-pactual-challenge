from typing import AsyncGenerator

from src.infrastructure.mongodb import BaseRepository, LogTransactionsFundsCollection

from .entities import _LogFlat, LogUncommited

__all__ = ("LogTransactionRepository",)


class LogTransactionRepository(BaseRepository[LogTransactionsFundsCollection]):
    schema_class = LogTransactionsFundsCollection

    async def all(self) -> AsyncGenerator[_LogFlat, None]:
        """
        *-*-*
        """
        async for instance in self._all():
            yield instance

    async def get(self, id_: int) -> _LogFlat:
        """
                        *-*-*
        :param id_:
        :return:
        """
        instance = await self._get(key="id", value=id_)
        return _LogFlat.model_validate(instance)

    async def create(self, schema: LogUncommited) -> _LogFlat:
        """

        :param schema:
        :return:
        """
        instance: LogTransactionsFundsCollection = await self._save(schema.model_dump())
        return _LogFlat.model_validate(instance)
