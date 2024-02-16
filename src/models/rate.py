from pydantic import BaseModel, validator
from typing import List


class RateValue(BaseModel):
    """Model of rate values."""
    dynamic_value: float = None
    fix_value: float = None


class RateType(BaseModel):
    """Base model of rate"""
    type: str
    value: RateValue

    @property
    def get_object(self):
        return {"type": type, "values": self.value.model_dump()}

    @validator("type")
    def validate_type(cls, v):
        if v not in ["PIX_CASH_OUT", "PIX_CASH_IN", "BETWEEN_ACCOUNTS"]:
            raise ValueError("Invalid type")
        return v


class InRate(BaseModel):
    """Model of input data for rate user"""

    values: List[RateType] = None
    name: str = None
    is_default: bool = True


class UpdateRate(BaseModel):
    """Model of update data for rate user"""
    values: List[RateType] = None


class OutRate(BaseModel):
    """Model of output data for rate user"""

    id: str
    user_id: str = None
    data: dict
    consumer: str = None
    admin_user: dict = None
    created_at: int = None
    updated_at: int = None
