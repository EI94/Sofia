import os
import logging
from elevenlabs import generate, Voice, VoiceSettings, set_api_key
from elevenlabs.client import ElevenLabs
import json
import tempfile
import base64
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Global audio cache for ElevenLabs streaming
_GLOBAL_AUDIO_CACHE = {}

class ElevenLabsTTS:
    """ElevenLabs Text-to-Speech with maximum quality settings"""
    
    def __init__(self):
        self.api_key = self._init_elevenlabs_service()
        self.client = ElevenLabs(api_key=self.api_key)
        self.voices = self.client.voices.get_all()
        logger.info(f"🔥 ElevenLabs API connected - {len(self.voices.voices)} voices available")
        logger.info("🔥🔥🔥 ELEVENLABS REAL TTS CONFIRMED ACTIVE!")
        logger.info("🔥🔥🔥 ELEVENLABS MAXIMUM QUALITY VOICE SYSTEM ACTIVE!")
        logger.info("🔥🔥🔥 NO MORE POLLY BULLSHIT - PREMIUM VOICE READY!")
        self.real_tts_active = True
        logger.info(f"🎤 ElevenLabs TTS initialized - Real: {self.real_tts_active}")

    def _init_elevenlabs_service(self) -> str:
        """Initialize ElevenLabs API key from Secret Manager or environment."""
        elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        if not elevenlabs_api_key:
            try:
                from google.cloud import secretmanager
                client = secretmanager.SecretManagerServiceClient()
                project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
                if project_id:
                    secret_name = f"projects/{project_id}/secrets/ELEVENLABS_API_KEY/versions/latest"
                    response = client.access_secret_version(name=secret_name)
                    elevenlabs_api_key = response.payload.data.decode("UTF-8").strip().replace('\r', '').replace('\n', '')
                    logger.info("🔥 ElevenLabs API key loaded from Google Secret Manager")
                else:
                    logger.warning("⚠️ GOOGLE_CLOUD_PROJECT environment variable not set. Cannot load ElevenLabs API key from Secret Manager.")
            except Exception as e:
                logger.error(f"❌ Error loading ElevenLabs API key from Secret Manager: {e}")
        
        if not elevenlabs_api_key:
            logger.error("❌ ElevenLabs API key not found in environment or Secret Manager.")
            raise ValueError("ElevenLabs API key is not set.")
        
        set_api_key(elevenlabs_api_key)
        logger.info("🔥 ElevenLabs API key loaded from environment")
        logger.info("🔥 ElevenLabs API key hardcoded successfully - REAL TTS ACTIVE!")
        return elevenlabs_api_key

    def _get_elevenlabs_voice(self, language: str) -> Voice:
        """Selects an ElevenLabs voice based on language."""
        if language == "it":
            return Voice(
                voice_id='21m00Tcm4TlvDq8ikWAM',  # Bianca
                settings=VoiceSettings(stability=0.75, similarity_boost=0.75, style=0.0, use_speaker_boost=True)
            )
        elif language == "en":
            return Voice(
                voice_id='EXAVITQu4vr4xnSDxMaL',  # Bella
                settings=VoiceSettings(stability=0.75, similarity_boost=0.75, style=0.0, use_speaker_boost=True)
            )
        elif language == "es":
            return Voice(
                voice_id='MF3mC3DVAio3foVEa4SC',  # Antoni
                settings=VoiceSettings(stability=0.75, similarity_boost=0.75, style=0.0, use_speaker_boost=True)
            )
        elif language == "fr":
            return Voice(
                voice_id='EXAVITQu4vr4xnSDxMaL',  # Bella (fallback for French)
                settings=VoiceSettings(stability=0.75, similarity_boost=0.75, style=0.0, use_speaker_boost=True)
            )
        else:
            logger.warning(f"⚠️ Unsupported language for ElevenLabs: {language}. Falling back to Italian.")
            return self._get_elevenlabs_voice("it")

    def _create_streaming_audio_url(self, text: str, language: str) -> Optional[str]:
        """Generates ElevenLabs audio, caches it, and returns a streaming URL."""
        try:
            voice = self._get_elevenlabs_voice(language)
            logger.info(f"🎤 Generating ElevenLabs speech: {text[:50]}... (lang: {language}, voice: {voice.voice_id})")
            
            audio_data = generate(
                text=text,
                voice=voice,
                model="eleven_multilingual_v2",
                stream=False  # Generate full audio, then stream via URL
            )
            
            if not audio_data:
                logger.error("❌ ElevenLabs audio generation returned empty data.")
                return None

            logger.info(f"✅ ElevenLabs speech generated successfully ({len(audio_data)} bytes)")

            # Create a unique audio ID
            import hashlib
            import time
            audio_id = hashlib.md5(f"{text}_{language}_{time.time()}".encode()).hexdigest()
            
            # Store audio data in GLOBAL cache for endpoint serving
            global _GLOBAL_AUDIO_CACHE
            _GLOBAL_AUDIO_CACHE[audio_id] = {
                'data': audio_data,
                'content_type': 'audio/mpeg',
                'created': time.time()
            }
            
            # Create streaming URL pointing to our audio endpoint
            audio_url = f"https://sofia-lite-jtcm2gle4a-uc.a.run.app/audio/{audio_id}"
            
            logger.info(f"🎤 Created ElevenLabs streaming URL: {audio_url} ({len(audio_data)} bytes)")
            logger.info(f"🎤 Audio cached with ID: {audio_id} - Cache size: {len(_GLOBAL_AUDIO_CACHE)}")
            return audio_url
            
        except Exception as e:
            logger.error(f"❌ Failed to create streaming URL: {e}")
            return None

    def _generate_elevenlabs_streaming_twiml(self, audio_url: str, text: str) -> str:
        """Generate TwiML with ElevenLabs streaming audio + GATHER for user response"""
        # TwiML with Play element + Gather for 30 second user response
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather input="speech" timeout="30" speechTimeout="auto" action="/webhook/voice" method="POST">
        <Play>{audio_url}</Play>
    </Gather>
    <Redirect>/webhook/voice</Redirect>
</Response>"""

        logger.info("🎤🔥🔥🔥 ElevenLabs STREAMING + GATHER 30s - NO HANGUP!")
        return twiml

    def _generate_enhanced_polly_twiml(self, text: str, language: str) -> str:
        """Generate TwiML with Polly TTS (enhanced for better quality) + GATHER for user response"""
        voice_map = {
            "it": "Polly.Bianca",
            "en": "Polly.Joanna",
            "es": "Polly.Penelope",
            "fr": "Polly.Celine"
        }
        voice = voice_map.get(language, "Polly.Bianca")
        
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Gather input="speech" timeout="30" speechTimeout="auto" action="/webhook/voice" method="POST">
        <Say voice="{voice}" rate="medium" pitch="medium">
            {text}
        </Say>
    </Gather>
    <Redirect>/webhook/voice</Redirect>
</Response>"""
        logger.warning(f"⚠️ Using enhanced Polly fallback with {voice}")
        return twiml

    @classmethod
    def get_cached_audio(cls, audio_id: str) -> Optional[Dict[str, Any]]:
        """Get cached audio data by ID"""
        global _GLOBAL_AUDIO_CACHE
        
        audio_data = _GLOBAL_AUDIO_CACHE.get(audio_id)
        if audio_data:
            # Clean up old cache entries (older than 1 hour)
            import time
            current_time = time.time()
            if current_time - audio_data['created'] > 3600:  # 1 hour
                del _GLOBAL_AUDIO_CACHE[audio_id]
                return None
        
        return audio_data

    @classmethod
    def cleanup_audio_cache(cls):
        """Clean up expired audio cache entries"""
        global _GLOBAL_AUDIO_CACHE
        
        import time
        current_time = time.time()
        expired_keys = [
            key for key, data in _GLOBAL_AUDIO_CACHE.items()
            if current_time - data['created'] > 3600  # 1 hour
        ]
        
        for key in expired_keys:
            del _GLOBAL_AUDIO_CACHE[key]
        
        if expired_keys:
            logger.info(f"🧹 Cleaned up {len(expired_keys)} expired audio cache entries")

elevenlabs_tts_service = ElevenLabsTTS()

def generate_premium_voice_response(text: str, language: str) -> str:
    """
    Generates a premium voice response using ElevenLabs, with Polly as fallback.
    Returns TwiML.
    """
    if elevenlabs_tts_service.real_tts_active:
        audio_url = elevenlabs_tts_service._create_streaming_audio_url(text, language)
        if audio_url:
            return elevenlabs_tts_service._generate_elevenlabs_streaming_twiml(audio_url, text)
        else:
            logger.error("❌ Failed to get ElevenLabs streaming URL, falling back to enhanced Polly.")
            return elevenlabs_tts_service._generate_enhanced_polly_twiml(text, language)
    else:
        return elevenlabs_tts_service._generate_enhanced_polly_twiml(text, language)
