from pydantic import BaseModel, validator
from datetime import datetime
from src.utils.helper import generate_unique_random_string
from src.repositorys import rate_repo


class UpdateProgramReferal(BaseModel):
    """Update referal code."""

    name: str
    expired_at: datetime = None
    rate_id: str

    @validator("name")
    def validate_name(cls, value):
        if len(value) < 5:
            raise ValueError("length of name less 5")
        return value

    @validator("expired_at")
    def validate_expired_at(cls, value):
        """Validate expired at."""
        if value <= datetime:
            raise ValueError("input datetime <= datetime.now()")
        return value


class InProgramReferal(BaseModel):
    """Program referal."""

    user_id: str
    name: str = generate_unique_random_string(10)
    consumer_id: str = None
    is_active: bool = True
    rate_id: str = None
    principal: bool = False
    expired_at: datetime = None

    @validator("rate_id")
    def validate_rate_id(cls, value):
        """Validate rate exists."""
        rate = rate_repo.get(value)
        if not rate:
            raise ValueError("rate_id not found")
        return value


class OutValidateCode(BaseModel):
    """Response of vaidate code"""

    valid: bool
    name: str = None
    user_id: str = None
    consumer_id: str
    rate_id: str = None
    expired_at: datetime = None
