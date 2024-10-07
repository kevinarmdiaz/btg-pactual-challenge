from pydantic import UUID4, BaseModel
from src.infrastructure.application import PublicEntity


class _FundBase(BaseModel):
	name: str
	category: str
	minimum_investment_amount: float | None = None


class FundCreateRequestBody(_FundBase):
	"""Product create request body."""

	pass


class FundPublic(_FundBase):
	"""The internal application representation."""

	id: UUID4

