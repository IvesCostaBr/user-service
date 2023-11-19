from pydantic import BaseModel, root_validator
from src.repositorys.provider import ProviderRepository


class InCredential(BaseModel):
    """Create credential."""

    provider: str
    keys: dict
    webhook_validate: bool = True
    webhook_url: str = None
    webhook_key: str = None

    @root_validator(pre=True)
    def validate_required_keys(cls, fields_value):
        """Validate required_keys."""
        provider_id = fields_value.get("provider")
        provider = ProviderRepository().get(provider_id)
        if not provider:
            raise ValueError("provider not found.")
        for key, _ in fields_value.get("keys").items():
            if key not in provider.get("required_keys"):
                raise ValueError(
                    "one or more keys required not found. keys required: {}".format(
                        provider.get("required_keys")
                    )
                )
        return fields_value


class UpdateCredential(BaseModel):
    """Update credential."""

    pass


class OutCredential(BaseModel):
    """Return credential."""

    id: str
    provider: str
    webhook_validate: bool = True
    webhook_url: str = None
    key_webhook: str = None


class OutCredentialDetail(OutCredential):
    """Return credential detail."""

    keys: dict
