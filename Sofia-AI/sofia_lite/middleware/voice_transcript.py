"""
Voice Transcription Middleware - F22 WhatsApp Voice Notes
Trascrive note audio WhatsApp usando OpenAI Whisper
"""

import os
import tempfile
import tenacity
import logging
import requests
import io
from typing import Optional
from pydub import AudioSegment
import openai
from .. import get_config

log = logging.getLogger("sofia.voice_transcript")

# Configurazione Whisper
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "whisper-1")

@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_fixed(2),
    retry=tenacity.retry_if_exception_type((requests.RequestException, openai.APIError))
)
def transcribe_voice(url: str, lang_hint: Optional[str] = None) -> str:
    """
    Trascrive note audio WhatsApp usando OpenAI Whisper.
    
    Args:
        url: URL firmato HTTPS di Twilio per il download audio
        lang_hint: Suggerimento lingua per migliorare accuratezza (opzionale)
    
    Returns:
        Testo trascritto dall'audio
        
    Raises:
        Exception: Se la trascrizione fallisce dopo 3 tentativi
    """
    try:
        log.info(f"🎤 Iniziando trascrizione audio da: {url[:50]}...")
        
        # 1. Scarica l'audio da Twilio (url firmato HTTPS)
        log.info("📥 Downloading audio file...")
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        
        # 2. Converti OGG/OPUS → WAV PCM 16-bit (Whisper-friendly)
        log.info("🔄 Converting audio format...")
        with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
            # Carica audio da bytes e converti in WAV
            audio = AudioSegment.from_file(io.BytesIO(resp.content), format="ogg")
            audio.export(tmp.name, format="wav", parameters=["-ac", "1", "-ar", "16000"])
            tmp.flush()
            
            # 3. Trascrizione con OpenAI Whisper
            log.info(f"🤖 Transcribing with Whisper model: {WHISPER_MODEL}")
            
            # Configura OpenAI client
            cfg = get_config()
            client = openai.OpenAI(api_key=cfg["OPENAI_API_KEY"])
            
            # Parametri Whisper
            whisper_args = {
                "model": WHISPER_MODEL,
                "file": open(tmp.name, "rb")
            }
            
            # Aggiungi suggerimento lingua se disponibile
            if lang_hint:
                whisper_args["language"] = lang_hint
                log.info(f"🌍 Language hint: {lang_hint}")
            
            # Esegui trascrizione
            result = client.audio.transcriptions.create(**whisper_args)
            transcript = result.text.strip()
            
            log.info(f"✅ Trascrizione completata: '{transcript[:50]}...'")
            return transcript
            
    except requests.RequestException as e:
        log.error(f"❌ Errore download audio: {e}")
        raise
    except Exception as e:
        log.error(f"❌ Errore trascrizione: {e}")
        raise

def detect_audio_format(audio_bytes: bytes) -> str:
    """
    Rileva il formato audio dai bytes.
    
    Args:
        audio_bytes: Bytes del file audio
        
    Returns:
        Formato audio rilevato (ogg, mp3, wav, etc.)
    """
    try:
        # Prova a rilevare il formato dai primi bytes
        if audio_bytes.startswith(b'OggS'):
            return "ogg"
        elif audio_bytes.startswith(b'ID3') or audio_bytes.startswith(b'\xff\xfb'):
            return "mp3"
        elif audio_bytes.startswith(b'RIFF'):
            return "wav"
        else:
            # Fallback: prova con pydub
            audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
            return audio.format.lower()
    except Exception as e:
        log.warning(f"⚠️ Impossibile rilevare formato audio: {e}")
        return "ogg"  # Default per WhatsApp

@tenacity.retry(
    stop=tenacity.stop_after_attempt(2),
    wait=tenacity.wait_fixed(1)
)
def transcribe_voice_with_fallback(url: str, lang_hint: Optional[str] = None) -> str:
    """
    Trascrizione con fallback per diversi formati audio.
    
    Args:
        url: URL del file audio
        lang_hint: Suggerimento lingua
        
    Returns:
        Testo trascritto
    """
    try:
        # Download audio
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        
        # Rileva formato
        audio_format = detect_audio_format(resp.content)
        log.info(f"🎵 Audio format detected: {audio_format}")
        
        # Converti in WAV
        with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
            audio = AudioSegment.from_file(io.BytesIO(resp.content), format=audio_format)
            audio.export(tmp.name, format="wav", parameters=["-ac", "1", "-ar", "16000"])
            tmp.flush()
            
            # Trascrizione
            cfg = get_config()
            client = openai.OpenAI(api_key=cfg["OPENAI_API_KEY"])
            
            whisper_args = {
                "model": WHISPER_MODEL,
                "file": open(tmp.name, "rb")
            }
            
            if lang_hint:
                whisper_args["language"] = lang_hint
            
            result = client.audio.transcriptions.create(**whisper_args)
            return result.text.strip()
            
    except Exception as e:
        log.error(f"❌ Trascrizione fallback fallita: {e}")
        raise 