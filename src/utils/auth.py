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
    print(f"user not found {payload.get('sub')}")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated",
        )
    user["consumer_id"] = user.get("consumer")
    if user.get("consumers") and not user.get("consumer_id"):
        try:
            user["consumer_id"] = user.get("consumers")[0]
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="no consumers were found",
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
