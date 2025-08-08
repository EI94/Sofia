"""
Rate limiter per Sofia Bulk API
Usa slowapi per limitare a 10 requests/second per API-Key
"""

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request


# Crea il limiter
limiter = Limiter(key_func=get_remote_address)


def get_rate_limiter() -> Limiter:
    """Factory function per creare il rate limiter"""
    return limiter


def rate_limit_by_api_key(request: Request) -> str:
    """Custom key function per rate limiting basato su API key"""
    # Estrai API key dall'header Authorization
    auth_header = request.headers.get("Authorization", "")
    
    if auth_header.startswith("Bearer "):
        api_key = auth_header[7:]  # Rimuovi "Bearer "
        return f"api_key:{api_key}"
    
    # Fallback all'IP se non c'è API key
    return get_remote_address(request)


# Crea limiter con custom key function
api_key_limiter = Limiter(key_func=rate_limit_by_api_key)


def get_api_key_limiter() -> Limiter:
    """Factory function per creare il rate limiter basato su API key"""
    return api_key_limiter


# Decorator per rate limiting
def rate_limit_10_per_second(func):
    """Decorator per limitare a 10 requests/second per API key"""
    return api_key_limiter.limit("10/second")(func)
