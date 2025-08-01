"""
Sofia Lite - Common Handler for Voice & WhatsApp
Unified flow for processing incoming messages from any channel.
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def handle_incoming(phone: str, text: str, channel: str = "whatsapp") -> Dict[str, Any]:
    """
    Unified handler for incoming messages from any channel.
    """
    try:
        logger.info(f"📥 Incoming message from {phone} via {channel}: {text[:50]}...")
        
        # Mock response for testing
        if channel == "voice":
            return {
                "twiml": f'<?xml version="1.0" encoding="UTF-8"?><Response><Say voice="Polly.Bianca">Voice response: {text}</Say></Response>',
                "reply": f"Voice response: {text}",
                "intent": "GREET",
                "state": "ASK_NAME",
                "lang": "it",
                "phone": phone,
                "channel": channel
            }
        else:
            return {
                "reply": f"WhatsApp response: {text}",
                "intent": "GREET",
                "state": "ASK_NAME",
                "lang": "it",
                "phone": phone,
                "channel": channel
            }
            
    except Exception as e:
        logger.error(f"❌ Error processing message from {phone}: {e}")
        return {
            "reply": "Mi dispiace, si è verificato un errore. Riprova più tardi.",
            "intent": "ERROR",
            "state": "ERROR",
            "lang": "it",
            "phone": phone,
            "channel": channel,
            "error": str(e)
        }

def handle_voice_with_fallback(phone: str, transcript: str) -> Dict[str, Any]:
    """
    Handle voice messages with TTS fallback.
    """
    try:
        result = handle_incoming(phone, transcript, "voice")
        result["audio_path"] = "/tmp/audio.wav"
        return result
    except Exception as e:
        logger.error(f"❌ Error in voice handler: {e}")
        return {
            "twiml": '<?xml version="1.0" encoding="UTF-8"?><Response><Say voice="Polly.Bianca">Mi dispiace, si è verificato un errore.</Say></Response>',
            "reply": "Mi dispiace, si è verificato un errore. Riprova più tardi.",
            "intent": "ERROR",
            "state": "ERROR",
            "lang": "it",
            "phone": phone,
            "channel": "voice",
            "audio_path": None,
            "error": str(e)
        }

def generate_tts_with_fallback(text: str, lang: str = "it") -> Optional[str]:
    """
    Generate TTS with ElevenLabs fallback to pyttsx3.
    """
    # Mock implementation for testing
    logger.info(f"🎤 TTS fallback for: {text[:50]}...")
    return "/tmp/audio.wav"
