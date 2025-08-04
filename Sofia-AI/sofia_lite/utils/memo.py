"""
TTL Cache Decorator - Δmini Performance Optimization
In-process TTL cache per ridurre chiamate ripetute
"""

import time
import functools
from typing import Any, Callable, Dict, Tuple
import logging

log = logging.getLogger("sofia.memo")

class TTLCache:
    """Simple TTL cache implementation"""
    
    def __init__(self, ttl: int = 30, maxsize: int = 256):
        self.ttl = ttl
        self.maxsize = maxsize
        self.cache: Dict[str, Tuple[Any, float]] = {}
    
    def get(self, key: str) -> Any:
        """Get value from cache if not expired"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any):
        """Set value in cache with timestamp"""
        # Evict oldest if cache is full
        if len(self.cache) >= self.maxsize:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]
        
        self.cache[key] = (value, time.time())
    
    def clear(self):
        """Clear all cached values"""
        self.cache.clear()

def ttl_cache(ttl: int = 30, maxsize: int = 256):
    """
    Decorator per TTL cache - Δmini optimization
    
    Args:
        ttl: Time to live in seconds
        maxsize: Maximum number of cached items
    """
    def decorator(func: Callable) -> Callable:
        cache = TTLCache(ttl=ttl, maxsize=maxsize)
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Create cache key from function name and arguments
            key = f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Try to get from cache
            cached_result = cache.get(key)
            if cached_result is not None:
                log.debug(f"💾 Cache hit for {func.__name__}")
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(key, result)
            log.debug(f"💾 Cache miss for {func.__name__}, cached result")
            
            return result
        
        return wrapper
    return decorator

# Global caches for common functions
_language_cache = TTLCache(ttl=30, maxsize=256)
_similarity_cache = TTLCache(ttl=30, maxsize=256)

def get_language_cache() -> TTLCache:
    """Get global language detection cache"""
    return _language_cache

def get_similarity_cache() -> TTLCache:
    """Get global similarity classification cache"""
    return _similarity_cache 