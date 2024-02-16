from src.infra.db.abstract_conneection import AbstractConnection
from pymongo.mongo_client import MongoClient
from bson import ObjectId
from datetime import datetime
from src.infra.cache import cache_manager
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
        try:
            self.client = MongoClient(self.host, self.port)
            print("MongoDB connected successfully!!")
            self.db = self.client[self.db_name]
        except Exception as e:
            self.db = None

    def get(self, entity: str, id: str, use_cache: bool = True):
        value_cached = cache_manager.get(id) if use_cache else False
        if not value_cached:
            try:
                object_id = ObjectId(id)
            except:
                object_id = id
            doc = self.db[entity].find_one({"_id": object_id})
            if doc is not None:
                doc["id"] = str(doc.pop("_id"))
                cache_manager.save(id, doc, 1200)
                return doc
            else:
                return None
        else:
            return value_cached

    def get_all(self, entity: str, limit: int = 100):
        docs = list(self.db[entity].find(limit))
        return docs

    def create(self, entity: str, data: dict, id: str = None):
        """Create a new document in MongoDB."""
        data["created_at"] = time.mktime(datetime.now().timetuple())
        if id:
            data["_id"] = id
        new_data = self.db[entity].insert_one(data)
        return str(new_data.inserted_id)

    def update(self, entity: str, id: str, data: dict):
        data["updated_at"] = time.mktime(datetime.now().timetuple())
        update_operation = {"$set": data}
        try:
            self.db[entity].update_one(
                {"_id": ObjectId(id)}, update_operation, upsert=False
            )
            return True
        except:
            return False

    def __format_filter(self, query: dict) -> list:
        filter_formated = []
        for key, value in query.items():
            if "__" not in key.lower():
                filter_formated.append({key: value})
            elif "__lt" in key.lower():
                filter_formated.append(
                    {key.replace("__lt", ""): {"$lt": value}})
            elif "__lte" in key.lower():
                filter_formated.append(
                    {key.replace("__lte", ""): {"$lte": value}})
            elif "__range" in key.lower():
                start, end = value
                filter_formated.append(
                    {key.replace("__range", ""): {"$gte": start, "$lte": end}}
                )
            elif "__gt" in key.lower():
                filter_formated.append(
                    {key.replace("__gt", ""): {"$gt": value}})
            elif "__gte" in key.lower():
                filter_formated.append(
                    {key.replace("__gte", ""): {"$gte": value}})
            elif "__in" in key.lower():
                filter_formated.append(
                    {key.replace("__in", ""): {"$in": value}})
            elif "__in" in key.lower():
                filter_formated.append(
                    {key.replace("__nt", ""): {"$not": value}})
        return filter_formated

    def filter_query(self, entity: str, query: dict, get_fields: list = None):
        response_list = []
        formatted_query = self.__format_filter(query)
        result = self.db[entity].find({"$and": formatted_query})
        if not result:
            return []
        for each in result:
            each["id"] = str(each["_id"])
            each.pop("_id")
            if get_fields:
                each = {
                    key: value
                    for key, value in each.items()
                    if key in get_fields
                }
            try:
                each.pop("password")
            except:
                None
            response_list.append(each)
        return response_list

    def exists(self, entity: str, query: dict):
        result = self.db[entity].find(query)
        return list(result)
