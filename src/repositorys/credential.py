from src.infra.db.abstract_conneection import AbstractConnection
from src.infra.db import database
from src.models import credential
from src.repositorys.provider import ProviderRepository


class CredentialRepository:
    def __init__(self) -> None:
        self.db: AbstractConnection = database
        self.entity = "credentials"

    def create(self, data: credential.InCredential):
        """Create a new transaction"""
        result = self.db.create(self.entity, data.model_dump())
        return result

    def get(self, id: str, use_cache: bool = True):
        """Get a transaction by id"""
        result = self.db.get(self.entity, id, use_cache)
        return result

    def get_all(self):
        """Get all transactions"""
        result = self.db.get_all(self.entity)
        return result

    def update(self, id: str, data: credential.UpdateCredential):
        """Update credential document."""
        result = self.db.update(id, data.model_dump())
        return result

    def exists(self, **kwargs):
        """verify exists document."""
        result = self.db.exists(self.entity, kwargs)
        return result

    def get_aggregate_data(self, id: str):
        """Return all object aggregate data."""
        credential = self.get(id)
        if not credential:
            return None
        provider = ProviderRepository().get(credential.get("provider"))
        if not provider:
            return None
        credential["provider"] = provider
        return credential

    def filter_query(self, **kwargs):
        """Filter query."""
        result = self.db.filter_query(self.entity, kwargs)
        return result
