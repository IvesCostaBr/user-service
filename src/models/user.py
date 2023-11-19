from pydantic import BaseModel


class InUser(BaseModel):
    """Model of register user."""
    email: str
    password: str
    phone: str = None

class User(BaseModel):
    user_id: str
    email: str
    created_at: int
    modified_at: int