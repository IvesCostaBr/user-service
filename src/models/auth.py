from pydantic import BaseModel


class Login(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    user_id: str = None


class RefreshToken(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
