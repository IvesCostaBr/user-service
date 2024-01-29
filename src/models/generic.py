from pydantic import BaseModel


class SignUpUserResponse(BaseModel):
    """Return of user register."""
    
    detail: str
    access_token: str = None
    
class Generic(BaseModel):
    """Generic response."""
    
    detail: bool = False