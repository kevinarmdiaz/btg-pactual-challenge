from fastapi import APIRouter, Request, status
from pydantic import UUID4
from src.application import users
from src.domain.users import (
    UserFlat,
    UserRepository
)
from src.infrastructure.application import Response, ResponseMulti
from .contracts import UserCreateRequestBody, UserPublic

router = APIRouter(prefix="/user", tags=["User"])


@router.get("", status_code=status.HTTP_200_OK)
async def user_list(request: Request) -> ResponseMulti[UserPublic]:
    """Get all products."""

    _users: list[UserFlat] = await users.get_all()

    _funds_public: list[UserPublic] = [
        UserPublic(**user.model_dump()) for user in _users
    ]

    return ResponseMulti[UserPublic](result=_funds_public)


@router.get("/{user_id}/funds/{fund_id}/susbcribe-fund", status_code=status.HTTP_200_OK)
async def susbcribe_fund(user_id: UUID4, fund_id: UUID4) -> Response[UserPublic]:
    """Suscribirse a un fondo"""

    _user: UserFlat = await users.suscribe_in_fund(
        user_id=user_id, fund_id=fund_id
    )

    return Response[UserPublic](result=_user)

@router.get("/{user_id}/funds/{fund_id}/cancel-fund", status_code=status.HTTP_200_OK)
async def cancel_fund(user_id: UUID4, fund_id: UUID4) -> Response[UserPublic]:
    """Darse de baja de fondo"""

    _user: UserFlat = await users.cancel_in_fund(
        user_id=user_id, fund_id=fund_id
    )

    return Response[UserPublic](result=_user)

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
