from src.infra.db.abstract_conneection import AbstractConnection
from pymongo.mongo_client import MongoClient
from bson import ObjectId
from datetime import datetime
import time


class MongoConnection(AbstractConnection):
    def __init__(self, connection_string: str, port: int, db_name: str):
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
        object_id = ObjectId(id)
        doc = self.db[entity].find_one({"_id": object_id})
        if doc is not None:
            return doc
        else:
            return None

    def get_all(self, entity: str, limit: int = 100):
        docs = list(self.db["books"].find(limit))
        return docs

    def create(self, entity: str, data: dict):
        data["created_at"] = time.mktime(datetime.now().timetuple())
        new_data = self.db[entity].insert_one(data)
        return str(new_data.inserted_id)

    def update(self, entity: str, id: str, data: dict):
        data["updated_at"] = time.mktime(datetime.now().timetuple())
        update_operation = {
            "$set": data
        }
        try:
            self.db[entity].update_one({"_id": ObjectId(id)}, update_operation, upsert=False)
            return True
        except:
            return False

    def filter_query(self, entity: str, query: dict):
        result = self.db[entity].find(query)
        return list(result)

    def exists(self, entity: str, query: dict):
        result = self.db[entity].find(query)
        return list(result)
