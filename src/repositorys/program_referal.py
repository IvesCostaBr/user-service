from src.infra.db.abstract_conneection import AbstractConnection
from src.infra.db import database
from src.models import program_referal
from src.utils.helper import generate_unique_random_string


class ProgramReferalRepository:
    def __init__(self) -> None:
        self.db: AbstractConnection = database
        self.entity = "program_referal"

    def create(self, **kwargs):
        """Create a new card"""
        is_exists = self.filter_query(
            user_id=kwargs.get('user_id'),
            is_active=True
        )
        if is_exists:
            return is_exists[0].get('code')
        code = generate_unique_random_string(10)
        kwargs["is_active"] = True
        kwargs["code"] = code

        payload = program_referal.InProgramReferal(
            user_id=kwargs.get('user_id'),
            code=code
        )

        self.db.create(self.entity, payload.model_dump())
        return code

    def get(self, id: str):
        """Get card by id"""
        result = self.db.get(self.entity, id)
        return result

    def get_all(self):
        """Get all cards"""
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

    def update(self, id: str, **kwargs):
        """Update document."""
        result = self.db.update(self.entity, id, kwargs)
        return result
