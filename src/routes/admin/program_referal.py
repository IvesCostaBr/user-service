from fastapi.routing import APIRouter
from src.services import program_referals_service
from fastapi import Depends
from starlette import status
from src.models import program_referal
from src.utils.auth import verify_is_admin

router = APIRouter(tags=["Admin - Program Referal"])


@router.get("/user/{user_id}/invitations", status_code=status.HTTP_200_OK)
async def get_all_user_invited(user_id, user=Depends(verify_is_admin)):
    return program_referals_service.get_all_user_invited(user, user_id)


@router.post("")
async def create_referal(data: program_referal.InProgramReferal, user=Depends(verify_is_admin)):
    """Create referal object."""
    return program_referals_service.create(user, data)


@router.get("")
async def get_program_referal_consumer(user=Depends(verify_is_admin)):
    """Get all referal of consumer."""
    return program_referals_service.get_program_referal_consumer(user)


@router.put("/{id}")
async def update_referal(id: str, user=Depends(verify_is_admin)):
    """Update referal code."""
    return program_referals_service.update(user, id)

@router.delete("/{id}")
async def delete_referal(id: str, user=Depends(verify_is_admin)):
    """Delete referal code."""
    return program_referals_service.delete(user, id)