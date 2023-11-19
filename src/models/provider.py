from pydantic import BaseModel, validator


class InProvider(BaseModel):
    """Model of create Provider."""

    name: str
    type: str
    required_keys: list

    @validator("type")
    def validate_type(cls, value):
        type_valid = ["BAAS", "BLOCKCHAIN"]
        if value.upper() not in type_valid:
            raise ValueError("type invalid, available: {}".format(type_valid))
        return value


class OutProvider(InProvider, BaseModel):
    """Out data of providers."""

    id: str
