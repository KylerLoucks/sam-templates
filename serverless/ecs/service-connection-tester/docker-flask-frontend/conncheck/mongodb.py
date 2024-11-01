from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import MONGO_HOST, MONGO_PORT


def create_conn():
    client = None
    try:
        if MONGO_PORT:
            client = MongoClient(
                f"mongodb://{MONGO_HOST}:{MONGO_PORT}/", serverSelectionTimeoutMS=1000
            )
        else:
            client = MongoClient(
                f"mongodb://{MONGO_HOST}/", serverSelectionTimeoutMS=1000
            )
        # The ismaster command is cheap and does not require auth.
        client.admin.command("ismaster")
        print("MongoDB connection successful")
    except ConnectionFailure as e:
        print(f"The error '{e}' occurred")
    return client


def is_mongodb_accessible():
    client = create_conn()
    if client is not None:
        try:
            client.admin.command("ismaster")
            return True
        except ConnectionFailure:
            return False
    return False
