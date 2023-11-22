from pydantic import BaseModel, root_validator, validator
from src.utils.validators import validate_email, validate_phone
from typing import List


class OutUser(BaseModel):
    id: str
    email: str = None
    phone: str = None
    created_at: int = None
    modified_at: int = None
    consumers: List[str] = []

    @validator("email")
    def validate_email_value(cls, value):
        """validate email."""
        if not validate_email(value):
            raise ValueError("Invalid email.")
        return value

    @validator("phone")
    def validate_phone_value(cls, value):
        """Validate phone."""
        if not validate_phone(value):
            raise ValueError("Invalid phone.")
        return value


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
