# Wrapper for ElevenLabs TTS
from ..tools.elevenlabs_tts import text_to_speech

def synthesize_speech(text, voice="Polly.Bianca"):
    """Synthesize speech with ElevenLabs"""
    try:
        return text_to_speech(text, voice)
    except Exception:
        return None 