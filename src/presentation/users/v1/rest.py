from fastapi import APIRouter, Request, status
from pydantic import UUID4
from src.application import users
from src.domain.users import (
    UserFlat,
)
from src.infrastructure.application import Response, ResponseMulti
from .contracts import UserPublic

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
async def user_list() -> ResponseMulti[UserPublic]:
    """Get all products."""

    _users: list[UserFlat] = await users.get_all()

    _funds_public: list[UserPublic] = [
        UserPublic(**user.model_dump()) for user in _users
    ]

    return ResponseMulti[UserPublic](result=_funds_public)