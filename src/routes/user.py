from fastapi.routing import APIRouter
from src.services import user_service
from fastapi import Depends
from src.models import user, auth, generic
from src.utils.auth import authenticate_user, verify_api_key
from starlette import status

router = APIRouter(tags=["User"])


@router.post("/login", response_model=auth.Login, status_code=status.HTTP_201_CREATED)
async def login_user(data: user.LoginUser):
    return user_service.login(data)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=generic.SignUpUserResponse)
async def register_user(data: user.InUser, consumer: dict = Depends(verify_api_key)):
    return user_service.create(data, consumer_id=consumer)


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
async def get_user_data(user: dict = Depends(authenticate_user)):
    return user


@router.post("/otp", status_code=status.HTTP_201_CREATED, response_model=dict)
async def login_user_otp(login: user.LoginUser):
    return user_service.login_passwordless(login)


@router.get("/otp", status_code=status.HTTP_200_OK)
async def verify_otp(otp: str, id: str):
    return user_service.verify_login_code(otp, id)


@router.post("/generate-token", status_code=status.HTTP_201_CREATED, response_model=auth.Login)
async def generete_unique_token(auth: dict = Depends(authenticate_user)):
    """Generate unique token to user."""
    return user_service.generate_unique_token(auth)

@router.get("/validate-api-key", status_code=status.HTTP_200_OK)
async def validate_api_key_route(consumer: str = Depends(verify_api_key), response_model=generic.SignUpUserResponse):
    if consumer:
        return {"detail": True}
    else:
        return {"detail": False}