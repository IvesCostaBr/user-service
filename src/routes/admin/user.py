from fastapi.routing import APIRouter
from src.services import user_service
from fastapi import Depends
from src.models import user
from src.utils.auth import verify_is_super_user

router = APIRouter(tags=["Admin - User"])


@router.post("/register-super-user")
async def register_user_admin(data: user.InUser, user=Depends(verify_is_super_user)):
    return user_service.create_admin(data)


@router.post("/register")
async def register_user(data: user.InUserAdmin, user=Depends(verify_is_super_user)):
    return user_service.create(data)
