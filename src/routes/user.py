from fastapi.routing import APIRouter
from src.services import user_service
from fastapi import Depends
from src.models import user, auth
from src.utils.auth import verify_token, verify_is_super_user
from starlette import status
from copy import deepcopy

router = APIRouter(tags=["User"])


@router.post("/login", response_model=auth.Login, status_code=status.HTTP_201_CREATED)
async def login_user(data: user.LoginUser):
    return user_service.login(data)


@router.post("/register")
async def register_user(data: user.InUser):
    return user_service.create(data)


@router.post(
    "/refresh", response_model=auth.RefreshToken, status_code=status.HTTP_201_CREATED
)
async def refresh_token_user(refresh_token: str):
    return user_service.refresh_token(refresh_token)


@router.get(
    "/me",
    responses={200: {"model": user.OutUser, "description": "Return data of user"}},
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def get_user_data(user: dict = Depends(verify_token)):
    user["consumer_data"] = user_service.get_consumer(user.get("consumer_id"))
    return user

@router.post("/otp", status_code=status.HTTP_201_CREATED, response_model=dict)
async def login_user_otp(login: user.LoginUser):
    return user_service.login_passwordless(login)


@router.get("/otp", status_code=status.HTTP_200_OK)
async def verify_otp(otp: str, id: str):
    return user_service.verify_login_code(otp, id)
