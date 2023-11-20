from src.repositorys import user_repo
from fastapi.security import APIKeyHeader
from fastapi import Depends, HTTPException
from src.utils.encrypt import validate_access_token
from starlette import status


id_token = APIKeyHeader(name="Authorization")


async def authenticate_user(token: str = Depends(id_token)):
    _, token = token.split()
    # user = get_user_data_firebase(token)
    user = {}
    if not user:
        raise HTTPException(status_code=403, detail="Unauthorized")
    user_data = user_repo.get_aggregate_data(user.uid)
    if not user_data:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return user_data


# Função para validar o token JWT
def verify_token(token: str = Depends(id_token)):
    """Validate token"""
    only_token = token.split("Bearer ")[1]
    result, payload = validate_access_token(only_token)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autorizado",
        )
    user = user_repo.get(payload.get("sub"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autorizado",
        )
    return user
