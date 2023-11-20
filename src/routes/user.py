from fastapi.routing import APIRouter
from src.services import user_service
from fastapi import Depends
from src.models import user, auth
from src.utils.auth import verify_token
from starlette import status

router = APIRouter(tags=["User"])


@router.post("/register")
async def register_user(data: user.InUser):
    return user_service.create(data)


@router.post("/login", response_model=auth.Login, status_code=status.HTTP_201_CREATED)
async def login_user(data: user.LoginUser):
    return user_service.login(data)


@router.post("/refresh", response_model=auth.RefreshToken, status_code=status.HTTP_201_CREATED)
async def refresh_token_user(refresh_token: str):
    return user_service.refresh_token(refresh_token)


@router.get("/me", response_model=user.OutUser, status_code=status.HTTP_200_OK)
async def get_user_data(user: dict = Depends(verify_token)):
    user['id'] = str(user['_id'])
    return user
