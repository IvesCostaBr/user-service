from src.infra.db.abstract_conneection import AbstractConnection
from src.infra.db import database
from src.models import provider


class ProviderRepository:
    def __init__(self) -> None:
        self.db: AbstractConnection = database
        self.entity = "providers"

    def create(self, data: provider.InProvider):
        """Create a new provider"""
        result = self.db.create(self.entity, data.model_dump())
        return result

    def get(self, id: str):
        """Get a provider by id"""
        result = self.db.get(self.entity, id)
        return result

    def get_all(self):
        """Get all providers"""
        result = self.db.get_all(self.entity)
        return result

    def filter_query(self, query: list):
        """Filter query"""
        result = self.db.filter_query(self.entity, query)
        return result

    def exists(self, **kwargs):
        """verify exists document."""
        result = self.db.exists(self.entity, kwargs)
        return result
