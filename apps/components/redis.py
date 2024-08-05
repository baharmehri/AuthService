import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class RedisConnection:
    __instance = {}

    @staticmethod
    def get_instance(db):
        if str(db) not in RedisConnection.__instance:
            RedisConnection.__instance[str(db)] = RedisConnection(db)
        return RedisConnection.__instance[str(db)]

    def __init__(self, db):
        host = os.environ.get('REDIS_HOST')
        port = os.environ.get('REDIS_PORT')
        username = os.environ.get('REDIS_USERNAME')
        password = os.environ.get('REDIS_PASSWORD')
        self.connection = Redis(host=host, port=port, username=username, password=password, db=db)


class Redis:
    _db_number = None

    def __init__(self):
        self.redis = (RedisConnection.get_instance(self._db_number)).connection

    def insert(self, key, expire_datetime: timedelta, value):
        self.redis.setex(key, expire_datetime, value)

    def key_exist(self, key):
        return self.redis.exists(key)

    def get_key(self, key):
        return self.redis.get(key)
