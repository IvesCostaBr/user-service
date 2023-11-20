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
        self.client = MongoClient(self.host, self.port)
        print("MongoDB connected successfully!!")
        self.db = self.client[self.db_name]

    def get(self, entity: str, id: str, use_cache: bool = True):
        if (doc := self.db[entity].find_one({"_id": id})) is not None:
            return doc
        else:
            return None

    def get_all(self, entity: str, limit: int = 100):
        docs = list(self.db["books"].find(limit))
        return docs

    def create(self, entity: str, data: dict):
        new_data = self.db[entity].insert_one(data)
        return str(new_data.inserted_id)

    def update(self, entity: str, id: str, data: dict):
        return

    def filter_query(self, entity: str, query: dict):
        result = self.db[entity].find(query)
        return list(result)

    def exists(self, entity: str, query: dict):
        result = self.db[entity].find(query)
        return list(result)
