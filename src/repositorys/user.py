from src.infra.db.abstract_conneection import AbstractConnection
from src.infra.db import database


class UserRepository:
    def __init__(self) -> None:
        self.db: AbstractConnection = database
        self.entity = "users"

    def create(self, data: dict, id: str = None):
        """Create a new User"""
        result = self.db.create(self.entity, data, id)
        return result

    def get(self, id: str):
        """Get a User by id"""
        result = self.db.get(self.entity, id, False)
        if result:
            result.pop("password")
        return result

    def get_all(self):
        """Get all Users"""
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

    def get_password(self, id: str):
        """Get password by id"""
        result = self.db.get(self.entity, id, False)
        if result:
            return result.get("password")
        return result