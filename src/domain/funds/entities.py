
from src.infrastructure.application import InternalEntity
from pydantic import UUID4

__all__ = ("FundUncommited", "FundFlat")


# Internal models
# ------------------------------------------------------
class _FundBase(InternalEntity):
    name: str
    category: str
    minimum_investment_amount: int | None = None


class FundUncommited(_FundBase):
    """This schema is used for creating instance in the database."""

    pass


class FundFlat(_FundBase):
    """Database record representation."""

    id: UUID4
