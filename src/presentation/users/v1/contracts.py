from typing import List

from pydantic import UUID4, BaseModel

from src.presentation.funds import FundPublic


class _UserBase(BaseModel):
	name: str
	email: str
	phone: str
	balance: int
	subscribed_funds: List[FundPublic] | None = None


class UserCreateRequestBody(_UserBase):
	"""Product create request body."""

	pass


class UserPublic(_UserBase):
	"""The internal application representation."""

	id: UUID4
