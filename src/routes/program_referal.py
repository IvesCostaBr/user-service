from fastapi.routing import APIRouter
from src.services import program_referal_service
from fastapi import Depends
from starlette import status
from src.models.program_referal import OutValidateCode
from src.utils.auth import authenticate_user

router = APIRouter(tags=["Program Referal"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def get_or_create_referal_code(user=Depends(authenticate_user)):
    return program_referal_service.create(user)


@router.get("", status_code=status.HTTP_200_OK)
async def get_refera_code_user(user=Depends(authenticate_user)):
    return program_referal_service.get_user_referal_code(user)


@router.get("/validate-code", status_code=status.HTTP_200_OK, responses={
    status.HTTP_200_OK: {
        "model": OutValidateCode,
        "description": "Return if code is valid to use."
    }
}
)
async def validate_code(code: str, user=Depends(authenticate_user)):
    """Validate code referal of user."""
    return program_referal_service.validate_code(user, code)
