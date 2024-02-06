from pydantic import BaseModel


class InProgramReferal(BaseModel):
    """Program referal."""

    name: str = None
    document: str = None
    user_id: str
    code: str
    is_active: bool = True


class OutValidateCode(BaseModel):
    """Response of vaidate code"""

    valid: bool
