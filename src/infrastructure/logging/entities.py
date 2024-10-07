from datetime import datetime

from src.infrastructure.application import InternalEntity
from pydantic import UUID4, Field

__all__ = ("LogUncommited", "_LogFlat")


# Internal models
# ------------------------------------------------------
class _LogBase(InternalEntity):
    user_id: UUID4
    fund_id: UUID4
    transaction_type: str
    message: str | None
    balance: int
    date: datetime = Field(default_factory=datetime.now, description="Date of the transaction")

    class Settings:
        name = "log_transactions_funds"  # Collection name in MongoDB


class LogUncommited(_LogBase):
    """This schema is used for creating instance in the database."""

    pass


class _LogFlat(_LogBase):
    """Database record representation."""

    id: UUID4
