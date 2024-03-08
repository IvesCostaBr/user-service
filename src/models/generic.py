from pydantic import BaseModel


class SignUpUserResponse(BaseModel):
    """Return of user register."""

    detail: str
    access_token: str = None


class PostGeneric(BaseModel):
    """Generic model of POST request."""

    detail: str


class Generic(BaseModel):
    """Generic response."""

    detail: bool = False
