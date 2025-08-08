"""
Sofia Lite - Handlers Package
Unified handlers for voice and WhatsApp channels.
"""

from .common import (
    generate_tts_with_fallback,
    handle_incoming,
    handle_voice_with_fallback,
)

__all__ = [
    "handle_incoming",
    "handle_voice_with_fallback",
    "generate_tts_with_fallback",
]
