from pydantic import BaseModel


class Login(BaseModel):

    access_token: str
    refresh_token: str
    expires_in: int
    
class RefreshToken(BaseModel):
    
    access_token: str
    expires_in: int