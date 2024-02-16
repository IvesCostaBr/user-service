from fastapi import APIRouter, Depends
from src.services import rate_service
from src.models import rate
from src.utils.auth import verify_is_admin
from starlette import status
from typing import List


router = APIRouter(tags=["Admin - Rates"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": dict, "description": "Create object rate"},
        400: {"model": dict, "description": "Bad Request"},
    },
    response_model=dict,
)
async def create_rate(data: rate.InRate, auth: dict = Depends(verify_is_admin)):
    """Create rate."""
    return rate_service.create(data, auth)


@router.get(
    "/{rate_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict
)
async def get_rate_detail(rate_id: str, auth: dict = Depends(verify_is_admin)):
    """Get rate detail."""
    return rate_service.get(auth, rate_id)


@router.get(
    "",
    responses={
        status.HTTP_200_OK: {"model": List[rate.OutRate]}
    }
)
async def get_rates(auth: dict = Depends(verify_is_admin)):
    """Get list rates of consumer_id."""
    return rate_service.list_rates(auth)


@router.patch(
    "/{rate_id}"
)
async def update_rate(rate_id: str, data: rate.InRate, auth: dict = Depends(verify_is_admin)):
    """Update rate."""
    return rate_service.update(auth, rate_id, data)
