"""
Sofia Lite - Voice TTS Middleware
Handles text-to-speech using ElevenLabs API
"""

import logging

from .. import get_config

logger = logging.getLogger(__name__)


class VoiceTTSGateway:
    def __init__(self):
        try:
            cfg = get_config()
            api_key = cfg["ELEVEN_KEY"]
            if not api_key:
                raise RuntimeError("missing ELEVENLABS_API_KEY")

            # Initialize ElevenLabs client here when needed
            self.api_key = api_key
            logger.info("✅ Voice TTS gateway initialized")
        except Exception as e:
            logger.error(f"❌ Voice TTS initialization failed: {e}")
            raise RuntimeError(f"Voice TTS initialization failed: {e}")

    def synthesize_speech(self, text: str, voice_id: str = "default") -> bytes:
        """Synthesize speech from text using ElevenLabs"""
        try:
            # Mock implementation for now
            logger.info(f"🎤 Synthesizing speech: {text[:50]}...")
            return b"mock_audio_data"
        except Exception as e:
            logger.error(f"❌ Speech synthesis failed: {e}")
            raise RuntimeError(f"Speech synthesis failed: {e}")


# Create singleton instance
_voice_tts_gateway = VoiceTTSGateway()


def synthesize_speech(text: str, voice_id: str = "default") -> bytes:
    """Synthesize speech from text"""
    return _voice_tts_gateway.synthesize_speech(text, voice_id)
