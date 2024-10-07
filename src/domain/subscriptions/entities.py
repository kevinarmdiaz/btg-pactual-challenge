from datetime import datetime

from src.infrastructure.application import InternalEntity
from pydantic import UUID4

__all__ = ("SubscriptionUncommited", "SubscriptionFlat")


class _SubscriptionBase(InternalEntity):
	fund_id: UUID4
	user_id: UUID4


class SubscriptionUncommited(_SubscriptionBase):
	"""This schema is used for creating a subscription instance in the database."""
	pass
class SubscriptionFlat(_SubscriptionBase):
	"""Existing subscription representation."""
	id: UUID4
	subscription_date: datetime
