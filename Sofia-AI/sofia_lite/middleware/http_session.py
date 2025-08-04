"""
HTTP Session Middleware - Δmini Performance Optimization
Singleton aiohttp.ClientSession con keep-alive ottimizzato
"""

import aiohttp
import asyncio
from typing import Optional
import logging

log = logging.getLogger("sofia.http_session")

# Global session singleton
_HTTP_SESSION: Optional[aiohttp.ClientSession] = None
_SESSION_LOCK = asyncio.Lock()

async def get_session() -> aiohttp.ClientSession:
    """
    Restituisce singleton aiohttp.ClientSession con keep-alive ottimizzato.
    
    Returns:
        aiohttp.ClientSession configurato per performance
    """
    global _HTTP_SESSION
    
    if _HTTP_SESSION is None or _HTTP_SESSION.closed:
        async with _SESSION_LOCK:
            if _HTTP_SESSION is None or _HTTP_SESSION.closed:
                # Configurazione ottimizzata per Δmini
                timeout = aiohttp.ClientTimeout(total=3)
                connector = aiohttp.TCPConnector(
                    limit=100,  # Max 100 connessioni simultanee
                    keepalive_timeout=45,  # Keep-alive per 45 secondi
                    enable_cleanup_closed=True,
                    ttl_dns_cache=300,  # Cache DNS per 5 minuti
                    use_dns_cache=True
                )
                
                _HTTP_SESSION = aiohttp.ClientSession(
                    timeout=timeout,
                    connector=connector,
                    headers={
                        "User-Agent": "Sofia-Lite/1.0 (Micro-Perf-Δmini)"
                    }
                )
                
                log.info("✅ HTTP Session singleton creato con keep-alive ottimizzato")
    
    return _HTTP_SESSION

async def close_session():
    """Chiude la sessione HTTP globale."""
    global _HTTP_SESSION
    
    if _HTTP_SESSION and not _HTTP_SESSION.closed:
        await _HTTP_SESSION.close()
        _HTTP_SESSION = None
        log.info("🔒 HTTP Session singleton chiuso")

def get_session_sync() -> Optional[aiohttp.ClientSession]:
    """
    Restituisce la sessione HTTP per uso sincrono (se disponibile).
    
    Returns:
        aiohttp.ClientSession o None se non inizializzata
    """
    return _HTTP_SESSION if _HTTP_SESSION and not _HTTP_SESSION.closed else None 