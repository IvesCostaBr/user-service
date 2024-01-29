from pydantic import BaseModel


class SignUpUserResponse(BaseModel):
    """Return of user register."""
    
    detail: str
    access_token: str = None