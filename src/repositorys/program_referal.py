from src.infra.db.abstract_conneection import AbstractConnection
from src.infra.db import database


class ProgramReferalRepository:
    def __init__(self) -> None:
        self.db: AbstractConnection = database
        self.entity = "program_referals"

    def create(self, **kwargs):
        """Create a new card"""
        is_exists = self.filter_query(
            name=kwargs.get('name'),
        )
        if is_exists:
            return is_exists[0].get('id')

        docid = self.db.create(self.entity, kwargs)
        return docid

    def get(self, id: str):
        """Get card by id"""
        result = self.db.get(self.entity, id)
        if result:
            result["rate"] = self.db.get("rates", result.get("rate_id"), False)
        return result

    def get_all(self):
        """Get all cards"""
        result = self.db.get_all(self.entity)
        return result

    def filter_query(self, get_fields: list = None, **kwargs):
        """Filter query"""
        filter = kwargs.get("filter")
        try:
            kwargs.pop("filter")
        except KeyError:
            pass
        kwargs.update(filter) if filter else None
        result = self.db.filter_query(self.entity, kwargs, get_fields)
        return result

    def exists(self, **kwargs):
        """verify exists document."""
        result = self.db.exists(self.entity, kwargs)
        return result

    def update(self, id: str, **kwargs):
        """Update document."""
        result = self.db.update(self.entity, id, kwargs)
        return result
