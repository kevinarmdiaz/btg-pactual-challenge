from pydantic import UUID4, BaseModel


class _SubscriptionBase(BaseModel):
    user_id: UUID4
    fund_id: UUID4


class SubscriptionRequestBody(_SubscriptionBase):
    """Product create request body."""

    pass


class SubscriptionPublic(_SubscriptionBase):
    """The internal application representation."""

    id: UUID4
