from src.repositorys import user_repo
from fastapi.security import APIKeyHeader
from fastapi import Depends, HTTPException, Header
from src.utils.encrypt import validate_access_token, verify_key
from starlette import status
import logging

id_token = APIKeyHeader(name="Authorization")


def raised_unauthorized(msg: str = None):
    if not msg:
        msg = "not authenticated"
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=msg,
    )

def validate_api_key(api_key: str, token: str = None, consumer: str = None):
    """Validate consumer and api_key."""
    user = True
    if token and consumer:
        user = validate_token(token)
        validate_consumer = user.get("consumer_data", {}).get("id") != consumer
    else:
        validate_consumer = False
    if validate_consumer or not verify_key(consumer, api_key):
        raised_unauthorized()
    return user


def validate_token(token: str):
    """Validate token."""
    result, payload = validate_access_token(token)
    if not result:
        raised_unauthorized()
    user = user_repo.get(payload.get("sub"))
    logging.error(f"user not found {payload.get('sub')}")
    if not user:
        raised_unauthorized()
    user["consumer_id"] = user.get("consumer")
    if user.get("consumers") and not user.get("consumer_id"):
        try:
            user["consumer_id"] = user.get("consumers")[0]
        except Exception:
            raised_unauthorized("user not have consumer")
    user["consumer_data"] = user_repo.get_consumer(user.get("consumer_id"))
    return user


def authenticate_user(
    token: str = Depends(id_token),
    consumer: str = Header(alias="Consumer", convert_underscores=False),
    x_api_key: str = Header(None, alias="x-api-key", convert_underscores=False),
):
    """Validate token"""
    only_token = token.split("Bearer ")[1]
    if x_api_key and consumer:
        user = validate_api_key(x_api_key, only_token, consumer)
        user["x_api_auth"] = True
    else:
        user = validate_token(only_token)
    return user


def verify_api_key(
    x_api_key: str = Header(None, alias="x-api-key", convert_underscores=False),
    consumer: str = Header(None, alias="Consumer", convert_underscores=False),
):
    """Verify api key."""
    if x_api_key and consumer:
        validate_api_key(x_api_key, consumer=consumer)
        return consumer
    return None
    
def verify_is_admin(
    token: str = Depends(id_token),
    consumer: str = Header(alias="Consumer", convert_underscores=False),
    x_api_key: str = Header(None, alias="x-api-key", convert_underscores=False)
):
    only_token = token.split("Bearer ")[1]
    if x_api_key and consumer:
        user = validate_api_key(x_api_key, only_token, consumer)
        user["x_api_auth"] = True
    else:
        user = validate_token(only_token)

    if not user.get("is_admin"):
        raised_unauthorized()
    return user


def verify_is_super_user(
    token: str = Depends(id_token),
    x_api_key: str = Header(None, alias="x-api-key", convert_underscores=False),
):
    """Validate token"""
    only_token = token.split("Bearer ")[1]
    if x_api_key:
        user = validate_api_key(x_api_key, only_token)
        user["x_api_auth"] = True
    else:
        user = validate_token(only_token)
    if not user.get("is_super_admin"):
        raised_unauthorized()
    return user
