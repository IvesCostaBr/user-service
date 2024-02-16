from pydantic import BaseModel, validator
from datetime import datetime
from src.utils.helper import generate_unique_random_string
from src.repositorys import rate_repo


class InProgramReferal(BaseModel):
    """Program referal."""

    user_id: str = None
    name: str = generate_unique_random_string(10)
    consumer_id: str = None
    rate_id: str
    is_active: bool = True
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
