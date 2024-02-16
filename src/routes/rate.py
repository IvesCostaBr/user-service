from fastapi import APIRouter, Depends
from src.services import rate_service
from src.models import card
from src.utils.auth import authenticate_user
from starlette import status
from typing import List


router = APIRouter(tags=["Rates"])


@router.get(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": dict, "description": "Pay Pix"},
        status.HTTP_400_BAD_REQUEST: {"model": dict, "description": "Bad Request"},
    },
    response_model=dict,
)
async def get(data: card.InCard, auth: dict = Depends(authenticate_user)):
    """Create card of user."""
    return rate_service.create(auth, data)
