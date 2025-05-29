import redis
import json
import os


class RedisAdapter:
    def cache_or_set(self, key: str, fetch_func, expire=None):
        
        cached = self.get(key)
        if cached is not None:
            return cached
        value = fetch_func()
        if value is not None:
            self.set(key, value, expire=expire)
        return value
    def __init__(self, db=0):
        self.host = os.getenv("REDIS_HOST")
        self.port = os.getenv("REDIS_PORT")
        self.db = db
        self.client = redis.StrictRedis(
            host=self.host, port=self.port, db=self.db, decode_responses=True
        )

    def set(self, key: str, value: any, expire=None):
        try:
            self.client.set(key, json.dumps(value), ex=expire)
        except Exception as e:
            raise Exception(f"Failed to set key {key} in Redis: {e}")

    def get(self, key: str):
        try:
            value = self.client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            raise Exception(f"Failed to get key {key} from Redis: {e}")

    def delete(self, key: str):
        try:
            self.client.delete(key)
        except Exception as e:
            raise Exception(f"Failed to delete key {key} from Redis: {e}")
