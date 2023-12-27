from fastapi.routing import APIRouter
from src.services import user_service
from fastapi import Depends
from src.models import user
from src.utils.auth import verify_is_super_user

router = APIRouter(tags=["Admin - User"])


@router.post("/register-super-user")
async def register_user(data: user.InUser, user = Depends(verify_is_super_user)):
    return user_service.create_admin(data)

@router.post("/register")
async def register_user(data: user.InUserAdmin):
    return user_service.create(data, user = Depends(verify_is_super_user))