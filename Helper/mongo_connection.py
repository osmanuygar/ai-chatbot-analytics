"""
Code which provides a MongoDB connection.
"""

from pymongo import MongoClient
from backend import settings

# MongoDB defaults for test and locak usage
DEFAULT_MONGO_HOST = "localhost"
DEFAULT_MONGO_PORT = 27017
DEFAULT_DB = settings.MONGODB_DB
DEFAULT_USER = settings.MONGODB_USERNAME
DEFAULT_PASSWORD = settings.MONGODB_USERNAME


class MongoConnection(object):
    """
    Base class for connecting to MongoDB.
    """

    def __init__(self, db=DEFAULT_DB, host=DEFAULT_MONGO_HOST, user=None, password=None, port=DEFAULT_MONGO_PORT, tz_aware=True,
                 **kwargs):
        """
        Create & open the connection - and authenticate.
        """
        self.client = MongoClient(
            host=host,
            port=port,
            tz_aware=tz_aware,
            w=0,
            **kwargs
        )
        print(self.client)
        self.db = self.client[db]

        if user is not None and password is not None:
            self.db.authenticate(user, password)

    def get_collection(self, collection):
        return self.db[collection]

    def get_db(self):
        return self.db
