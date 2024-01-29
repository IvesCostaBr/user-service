from src.infra.db.abstract_conneection import AbstractConnection
from src.infra.db import database


class LoginTokenRepository:
    def __init__(self) -> None:
        self.db: AbstractConnection = database
        self.entity = "login_token"

    def create(self, data: dict):
        """Create a new provider"""
        data["is_active"] = True
        result = self.db.create(self.entity, data)
        return result

    def get(self, id: str):
        """Get a provider by id"""
        result = self.db.get(self.entity, id)
        return result

    def get_all(self):
        """Get all providers"""
        result = self.db.get_all(self.entity)
        return result

    def filter_query(self, **query):
        """Filter query"""
        result = self.db.filter_query(self.entity, query)
        return result

    def exists(self, **kwargs):
        """verify exists document."""
        result = self.db.exists(self.entity, kwargs)
        return result

    def update(self, id: str, kwargs):
        """update document."""
        result = self.db.update(self.entity, id, kwargs)
        return result
