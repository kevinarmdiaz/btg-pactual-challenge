from src.domain.funds import FundFlat
from src.domain.users import UserFlat

from .entities import SubscriptionFlat

__all__ = ("Subscription",)


class Subscription(SubscriptionFlat):
    """This data model aggregates information of an subscription
    and nested data models from other domains.
    """

    fund: FundFlat
    user: UserFlat
