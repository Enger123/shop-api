from app.cache.redis import RedisCachedBackend
from app.core.config import settings

cache = RedisCachedBackend(redis_url=settings.REDIS_URL, cache_ttl_seconds=settings.CACHE_TTL_SECONDS)

def test_set_cache():
    cache.set_cache('test_key', {'name': 'Roman'})
    res = cache.list_cache('test_key')
    assert res == {'name': 'Roman'}

def test_delete_cache():
    res = cache.delete_cache('test_key')
    assert res is None

def test_find_unexisting_key():
    res = cache.list_cache('unexisting_key')
    assert res is None 
