from src.infra.db.mongo_connection import MongoConnection
import os

database = MongoConnection(os.environ.get("MONGO_HOST"), os.environ.get('MONGO_PORT'), os.environ.get("MONGO_DB_NAME"))
