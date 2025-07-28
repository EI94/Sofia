# Wrapper for Whisper transcription
from ..tools.whisper_transcription import transcribe_audio

def transcribe(audio_data):
    """Transcribe audio with Whisper"""
    try:
        return transcribe_audio(audio_data)
    except Exception:
        return None 