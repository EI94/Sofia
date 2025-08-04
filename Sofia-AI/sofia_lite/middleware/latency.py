"""
Latency Tracking Middleware
F21 PERFORMANCE SWAT - Profiling e ottimizzazioni
"""

import time
import functools
import logging
from typing import Callable, Any, Dict
from datetime import datetime

log = logging.getLogger("sofia.latency")

# Global latency tracking
_latency_stats = {}

def track_latency(tag: str):
    """
    Decoratore per tracciare la latency di funzioni specifiche.
    
    Args:
        tag: Tag identificativo per il tipo di operazione (LLM, LANG, RAG, TOTAL)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            start_ms = int(start_time * 1000)
            
            try:
                result = func(*args, **kwargs)
                end_time = time.time()
                duration_ms = int((end_time - start_time) * 1000)
                
                # Log strutturato per Cloud Run
                log.info(
                    f"LATENCY_TRACK",
                    extra={
                        "tag": tag,
                        "function": func.__name__,
                        "start_ms": start_ms,
                        "end_ms": int(end_time * 1000),
                        "duration_ms": duration_ms,
                        "success": True,
                        "timestamp": datetime.now().isoformat()
                    }
                )
                
                # Aggiorna statistiche globali
                if tag not in _latency_stats:
                    _latency_stats[tag] = []
                _latency_stats[tag].append(duration_ms)
                
                return result
                
            except Exception as e:
                end_time = time.time()
                duration_ms = int((end_time - start_time) * 1000)
                
                # Log errori
                log.error(
                    f"LATENCY_TRACK_ERROR",
                    extra={
                        "tag": tag,
                        "function": func.__name__,
                        "start_ms": start_ms,
                        "end_ms": int(end_time * 1000),
                        "duration_ms": duration_ms,
                        "success": False,
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    }
                )
                raise
                
        return wrapper
    return decorator

def get_latency_stats() -> Dict[str, Dict[str, float]]:
    """
    Restituisce le statistiche di latency aggregate.
    
    Returns:
        Dict con statistiche per tag (min, max, avg, p50, p95, p99)
    """
    stats = {}
    
    for tag, durations in _latency_stats.items():
        if not durations:
            continue
            
        durations.sort()
        n = len(durations)
        
        stats[tag] = {
            "count": n,
            "min": min(durations),
            "max": max(durations),
            "avg": sum(durations) / n,
            "p50": durations[int(n * 0.5)] if n > 0 else 0,
            "p95": durations[int(n * 0.95)] if n > 0 else 0,
            "p99": durations[int(n * 0.99)] if n > 0 else 0
        }
    
    return stats

def reset_latency_stats():
    """Resetta le statistiche di latency."""
    global _latency_stats
    _latency_stats = {}

def log_latency_summary():
    """Logga un riepilogo delle statistiche di latency."""
    stats = get_latency_stats()
    
    if not stats:
        log.info("No latency data available")
        return
    
    log.info("=== LATENCY SUMMARY ===")
    for tag, tag_stats in stats.items():
        log.info(
            f"{tag}: count={tag_stats['count']}, "
            f"avg={tag_stats['avg']:.0f}ms, "
            f"p95={tag_stats['p95']:.0f}ms, "
            f"p99={tag_stats['p99']:.0f}ms"
        )
    log.info("======================") 