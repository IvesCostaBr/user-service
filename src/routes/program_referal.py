from fastapi.routing import APIRouter
from src.services import program_referals_service
from fastapi import Depends
from starlette import status
from src.models import program_referal
from src.models.program_referal import OutValidateCode
from src.utils.auth import authenticate_user, verify_api_key

router = APIRouter(tags=["Program Referal"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(data: program_referal.InProgramReferal, user=Depends(authenticate_user)):
    return program_referals_service.create(user, data)


@router.get("", status_code=status.HTTP_200_OK)
async def get_referal_code_user(user=Depends(authenticate_user)):
    return program_referals_service.get_user_referal_codes(user)


@router.get("/validate-code", status_code=status.HTTP_200_OK, responses={
    status.HTTP_200_OK: {
        "model": OutValidateCode,
        "description": "Return if code is valid to use."
    }
}
)
async def validate_code(code: str, auth=Depends(verify_api_key)):
    """Validate code referal of user."""
    return program_referals_service.validate_code(auth, code)


@router.get("/user/referal-codes", status_code=status.HTTP_200_OK, responses={
    status.HTTP_200_OK: {
        "model": dict,
        "description": "Return if code is valid to use."
    }
}
)
async def get_rates_referals(auth=Depends(authenticate_user)):
    """Validate code referal of user."""
    return program_referals_service.get_referals_data(auth)
