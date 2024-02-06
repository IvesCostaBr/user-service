from fastapi.routing import APIRouter
from src.services import program_referal_service
from fastapi import Depends
from src.models import user
from starlette import status
from src.utils.auth import verify_is_super_user, verify_is_admin

router = APIRouter(tags=["Admin - Program Referal"])


@router.post("/{user_id}", status_code=status.HTTP_201_CREATED)
async def register_user_admin(user_id, user=Depends(verify_is_super_user)):
    return program_referal_service.get_all()
