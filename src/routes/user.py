from fastapi.routing import APIRouter
from src.services import user_service
from fastapi import Depends
from src.models import user
from src.utils.auth import verify_token

router = APIRouter(tags=["User"])


@router.post("/register")
async def register_user(data: user.InUser):
    return user_service.create(data)


@router.post("/login")
async def login_user(data: user.LoginUser):
    return user_service.login(data)


@router.post("/refresh")
async def refresh_token_user(refresh_token: str):
    return user_service.refresh_token(refresh_token)


@router.get("/me")
async def get_user_data(user: dict = Depends(verify_token)):
    return user
