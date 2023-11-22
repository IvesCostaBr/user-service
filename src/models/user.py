from pydantic import BaseModel, root_validator, validator
from src.utils.validators import validate_email, validate_phone_number
from src.repositorys import user_repo
from typing import List


class OutUser(BaseModel):
    id: str
    email: str = None
    phone: str = None
    created_at: int = None
    modified_at: int = None
    consumers: List[str] = []

class InUser(BaseModel):
    """Model of register user."""

    email: str
    password: str
    phone: str = None

    @validator("email")
    def validate_email_value(cls, value):
        """validate email."""
        if not validate_email(value):
            raise ValueError("Invalid email.")
        user_exists = user_repo.filter_query(email=value)
        if user_exists:
            raise ValueError("email cannot be used, try another")
        return value

    @validator("phone")
    def validate_phone_value(cls, value):
        """Validate phone."""
        if not validate_phone_number(value):
            raise ValueError("Invalid phone.")
        user_exists = user_repo.filter_query(phone=value)
        if user_exists:
            raise ValueError("phone cannot be used, try another")
        return value



class User(BaseModel):
    user_id: str
    email: str
    created_at: int
    modified_at: int


class LoginUser(BaseModel):
    email: str = None
    phone: str = None
    password: str = None
    passwordless: bool = False

    @root_validator(pre=True)
    def validate_passwordless(cls, field_values):
        """Validate passwordless login."""
        if field_values.get("passwordless"):
            if not field_values.get("phone"):
                raise ValueError("Phone is required for passwordless login.")
            return field_values
        else:
            if field_values.get("email") and field_values.get("password"):
                return field_values
            else:
                raise ValueError("Email and password are required for login.")
