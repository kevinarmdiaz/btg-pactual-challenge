from typing import AsyncGenerator
from pydantic import UUID4
from .entities import UserFlat, UserUncommited
from ...infrastructure.mongodb import UsersCollection, BaseRepository

__all__ = ("UserRepository",)


class UserRepository(BaseRepository[UsersCollection]):
	schema_class = UsersCollection

	async def all(self) -> AsyncGenerator[UserFlat, None]:
		"""

        """
		async for instance in self._all():
			yield UserFlat.model_validate(instance)

	async def get(self, id_: UUID4) -> UserFlat:
		"""

        :param id_:
        :return:
        """
		instance = await self._get(key="_id", value=id_)
		return UserFlat.model_validate(instance)

	async def create(self, schema: UserUncommited) -> UserFlat:
		"""

        :param schema:
        :return:
        """
		instance: UsersCollection = await self._save(schema.model_dump())
		return UserFlat.model_validate(instance)



	async def return_balance(self, user_instance: UsersCollection, minimum_investment_amount: int):
		"""

		:param user:
		:param fund:
		"""
		user_instance.balance += minimum_investment_amount
		return user_instance

