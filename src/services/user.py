from src.repositorys import user_repo
from src.models import user
from starlette import status
from fastapi import HTTPException
from src.utils.encrypt import (
    encrypt_key,
    generate_tokens,
    validate_refresh_token,
    validate_access_token,
)


class UserService:
    def __init__(self) -> None:
        self.entity = "user"

    def create(self, data: user.InUser):
        user_exists = user_repo.filter_query(email=data.email, phone=data.phone)
        if len(user_exists):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "User already exists."},
            )
        data.password = encrypt_key(data.password)
        doc_id = user_repo.create(data.model_dump())
        return {"detail": doc_id}

    def update(self, data):
        return

    def get(self, id):
        return None

    def me(self, token: str):
        """Get data user."""
        result, data = validate_access_token(token)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"message": "user not authenticated"},
            )
        user_data = user_repo.get(data.get("sub"))
        return user_data

    def login(self, data: user.LoginUser):
        """Login and generete token of user."""
        if not data.passwordless:
            user_exists = user_repo.filter_query(email=data.email)
            if not len(user_exists):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"error": "User already exists."},
                )
            user = user_exists[0]
            data.password = encrypt_key(data.password)
            if data.password != user.get("password"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"error": "email or password incorrect."},
                )
            tokens = generate_tokens(user_exists[0])
            return tokens
        else:
            user_exists = user_repo.filter_query(phone=data.phone)
            return {"detail": "autehntication code sent to phone."}

    def refresh_token(self, token: str):
        """Refresh token."""
        tokens = validate_refresh_token(token)
        if not tokens:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "error generete new token"},
            )
        return tokens
