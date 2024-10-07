from . import funds, subscriptions, users  # noqa: F401
from fastapi import APIRouter
api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(funds.router, prefix="/funds", tags=["funds"])
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])