from src.infra.db.abstract_conneection import AbstractConnection
from pymongo.mongo_client import MongoClient


class MongoConnection(AbstractConnection):
    def __init__(self, connection_string: str, port: str, db_name: str):
        """Initialize class with connection string and database name."""
        self.host = connection_string
        self.port = int(port)
        self.db_name = db_name
        self.db = None
        self.client = None

        self.create_connection()

    def create_connection(self):
        """Create connection with MongoDB."""
        self.client = MongoClient(host=self.host, port=self.port)
        self.db = self.client[self.db_name]

    def get(self, entity: str, id: str, use_cache: bool = True):
        return super().get(entity, id, use_cache)

    def get_all(self, entity: str):
        return super().get_all(entity)

    def create(self, entity: str, data: dict):
        return super().create(entity, data)

    def update(self, entity: str, id: str, data: dict):
        return super().update(entity, id, data)
