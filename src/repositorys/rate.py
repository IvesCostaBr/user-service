from src.infra.db.abstract_conneection import AbstractConnection
from src.infra.db import database


class RateRepository:
    def __init__(self) -> None:
        self.db: AbstractConnection = database
        self.entity = "rates"

    def create(self, data: dict):
        """Create a new rate"""
        result = self.db.create(self.entity, data)
        return result

    def get(self, id: str):
        """Get a rate by id"""
        result = self.db.get(self.entity, id)
        return result

    def get_all(self):
        """Get all rates"""
        result = self.db.get_all(self.entity)
        return result

    def filter_query(self, **kwargs):
        """Filter query"""
        filter = kwargs.get("filter")
        try:
            kwargs.pop("filter")
        except KeyError:
            pass
        kwargs.update(filter) if filter else None
        result = self.db.filter_query(self.entity, kwargs)
        return result

    def exists(self, **kwargs):
        """verify exists document."""
        result = self.db.exists(self.entity, kwargs)
        return result

    def update(self, id: str, kwargs):
        """Update document."""
        result = self.db.update(self.entity, id, kwargs)
        return result
