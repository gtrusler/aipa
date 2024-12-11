from typing import Any, Optional, Callable
from datetime import datetime, timedelta
import json

class Cache:
    """Simple in-memory cache with TTL"""
    
    def __init__(self):
        self._cache = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache if it exists and hasn't expired"""
        if key not in self._cache:
            return None
            
        entry = self._cache[key]
        if entry['expires'] < datetime.now():
            del self._cache[key]
            return None
            
        return entry['value']
    
    def set(self, key: str, value: Any, ttl_seconds: int):
        """Set a value in cache with TTL"""
        self._cache[key] = {
            'value': value,
            'expires': datetime.now() + timedelta(seconds=ttl_seconds)
        }
    
    def clear(self):
        """Clear all cached values"""
        self._cache.clear()


def cached(ttl_seconds: int):
    """Decorator to cache function results"""
    def decorator(func: Callable):
        cache = Cache()
        
        async def wrapper(*args, **kwargs):
            # Create a cache key from function name and arguments
            key_parts = [func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(key_parts)
            
            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Call function and cache result
            result = await func(*args, **kwargs)
            if result is not None:
                cache.set(cache_key, result, ttl_seconds)
            return result
            
        return wrapper
    return decorator
