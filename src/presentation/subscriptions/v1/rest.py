from fastapi import APIRouter, status, Depends
from src.domain.subscriptions import (
    SubscriptionFlat,
)
from src.infrastructure.application import ResponseMulti
from .contracts import SubscriptionPublic
from src.application.dependency_injection import get_fund, get_user
from src.application import subscriptions
from src.infrastructure.mongodb import FundsCollection, UsersCollection

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
async def subscription_list() -> ResponseMulti[SubscriptionPublic]:
    """Get all subscriptions."""

    _subscriptions: list[SubscriptionFlat] = await subscriptions.get_all()

    _subscriptions_public: list[SubscriptionPublic] = [
        SubscriptionPublic(**subscription.model_dump())
        for subscription in _subscriptions
    ]

    return ResponseMulti[SubscriptionPublic](result=_subscriptions_public)


@router.post("/subscribe-fund", status_code=status.HTTP_200_OK)
async def subscribe(
    db_fund: FundsCollection = Depends(get_fund),
    db_user: UsersCollection = Depends(get_user),
) -> bool:
    """Suscribirse a un fondo"""

    result = await subscriptions.suscribe_in_fund(user=db_user, fund=db_fund)

    return result


@router.post("/cancel-fund", status_code=status.HTTP_200_OK)
async def cancel(
    db_fund: FundsCollection = Depends(get_fund),
    db_user: UsersCollection = Depends(get_user),
) -> bool:
    """Darse de baja de fondo"""

    result = await subscriptions.cancel_in_fund(user=db_user, fund=db_fund)
    return result


# @router.post("", status_code=status.HTTP_201_CREATED)
# async def fund_create(
#     request: Request,
#     schema: FundCreateRequestBody,
# ) -> Response[FundPublic]:
#     """Create a new fund."""
#
#     _fund: FundFlat = await FundRepository().create(
#         FundUncommited(**schema.model_dump())
#     )
#     _fund_public = FundPublic.model_validate(_fund)
#
#     return Response[FundPublic](result=_fund_public)
