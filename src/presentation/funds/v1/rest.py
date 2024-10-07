from fastapi import APIRouter, Request, status

from src.application import funds
from src.domain.funds import (
    FundFlat,
    FundRepository,
    FundUncommited,
)
from src.infrastructure.application import Response, ResponseMulti

from .contracts import FundCreateRequestBody, FundPublic

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
async def funds_list() -> ResponseMulti[FundPublic]:
    """Get all products."""

    _funds: list[FundFlat] = await funds.get_all()

    _funds_public: list[FundPublic] = [
        FundPublic(**fund.model_dump()) for fund in _funds
    ]

    return ResponseMulti[FundPublic](result=_funds_public)


@router.post("", status_code=status.HTTP_201_CREATED)
async def fund_create(
    request: Request,
    schema: FundCreateRequestBody,
) -> Response[FundPublic]:
    """Create a new fund."""

    _fund: FundFlat = await FundRepository().create(
        FundUncommited(**schema.model_dump())
    )
    _fund_public = FundPublic.model_validate(_fund)

    return Response[FundPublic](result=_fund_public)
