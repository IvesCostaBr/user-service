from fastapi.routing import APIRouter
from src.services import user_service
from fastapi import Depends
from src.models import user
from starlette import status
from src.utils.auth import verify_is_super_user, verify_is_admin

router = APIRouter(tags=["Admin - User"])


@router.post("/register-super-user", responses={status.HTTP_201_CREATED: {
    "model": user.PostComplete}}, status_code=status.HTTP_201_CREATED)
async def register_user_admin(data: user.InUser, user=Depends(verify_is_super_user)):
    return user_service.create_admin(data)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(data: user.InUserAdmin, user=Depends(verify_is_admin)):
    return user_service.create(data, user)


@router.post("/{user_id}/convert-admin", responses={status.HTTP_201_CREATED: {
    "model": user.PostComplete}}, status_code=status.HTTP_201_CREATED)
async def convert_user_to_admin(user_id: str, user=Depends(verify_is_admin)):
    """Convert user to admin."""
    return user_service.convert_user_admin(user, user_id)


@router.get("", status_code=status.HTTP_200_OK)
async def get_users_admin(user=Depends(verify_is_admin)):
    return user_service.get_user_admin(user)


@router.get("/super-admin", status_code=status.HTTP_200_OK)
async def get_users_super_admin(user=Depends(verify_is_super_user)):
    return user_service.get_super_admin()


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user(id: str, user=Depends(verify_is_admin)):
    return user_service.get_user(id, user)
