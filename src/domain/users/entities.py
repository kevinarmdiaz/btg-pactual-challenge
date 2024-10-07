from typing import List
from src.infrastructure.application import InternalEntity
from pydantic import UUID4

__all__ = ("UserUncommited", "UserFlat")

from src.presentation.funds import FundPublic


class UserUncommited(InternalEntity):
    """This schema is used for creating instance in the database."""

    name: str
    email: str
    phone: str
    balance: int
    subscribed_funds: List[FundPublic] | None = None


class UserFlat(UserUncommited):
    """Existed product representation."""

    id: UUID4
