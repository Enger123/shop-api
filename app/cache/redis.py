from redis import Redis
import json
from app.core.config import settings

class RedisCachedBackend:
    def __init__(self, redis_url: str, cache_ttl_seconds: int):
        self.redis = Redis.from_url(redis_url, decode_responses=True)
        self.cache_ttl_seconds = cache_ttl_seconds

    def list_products(self, key: str):
        value = self.redis.get(key)
        if value is not None:
            return json.loads(self.redis.get(key))

    def set_products(self, key: str, value: str):
        self.redis.set(key, json.dumps(value), ex=self.cache_ttl_seconds)

    def delete_product(self, key: str):
        self.redis.delete(key)

        