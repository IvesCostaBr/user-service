from src.repositorys import user_repo
from fastapi.security import APIKeyHeader
from fastapi import Depends, HTTPException
from src.utils.encrypt import validate_access_token
from starlette import status

id_token = APIKeyHeader(name="Authorization")


def verify_token(token: str = Depends(id_token)):
    """Validate token"""
    only_token = token.split("Bearer ")[1]
    result, payload = validate_access_token(only_token)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated",
        )
    user = user_repo.get(payload.get("sub"))
    user["consumer_id"] = None
    if user.get("consumers"):
        user["consumer_id"] = user.get("consumers")[0]
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated",
        )
    return user


def verify_is_super_user(token: str = Depends(id_token)):
    """Validate token"""
    only_token = token.split("Bearer ")[1]
    result, payload = validate_access_token(only_token)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated",
        )
    user = user_repo.get(payload.get("sub"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated",
        )
    if not user.get("is_admin"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated",
        )
    return user