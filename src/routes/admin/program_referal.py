from fastapi.routing import APIRouter
from src.services import program_referal_service
from fastapi import Depends
from starlette import status
from src.utils.auth import verify_is_admin

router = APIRouter(tags=["Admin - Program Referal"])


@router.get("/{user_id}", status_code=status.HTTP_201_CREATED)
async def get_all_user_invited(user_id, user=Depends(verify_is_admin)):
    return program_referal_service.get_all_user_invited(user, user_id)
