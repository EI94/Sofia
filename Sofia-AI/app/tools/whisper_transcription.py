"""
🎙️ Modulo Whisper per trascrizione messaggi vocali WhatsApp
Utilizza OpenAI Whisper API per convertire audio in testo
"""

import os
import logging
import httpx
import base64
import tempfile
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class WhisperTranscription:
    """Gestione trascrizione audio con OpenAI Whisper"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY', '').strip()
        if not self.api_key:
            logger.error("❌ OPENAI_API_KEY non configurata per Whisper")
            raise ValueError("OpenAI API key required for Whisper")
        
        self.base_url = "https://api.openai.com/v1/audio/transcriptions"
        logger.info("🎙️ WhisperTranscription inizializzato")
    
    async def download_audio_from_url(self, media_url: str) -> bytes:
        """Scarica file audio da URL Twilio"""
        try:
            logger.info(f"📥 Scaricando audio da: {media_url}")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(media_url)
                
                if response.status_code == 200:
                    audio_data = response.content
                    logger.info(f"✅ Audio scaricato: {len(audio_data)} bytes")
                    return audio_data
                else:
                    logger.error(f"❌ Errore download audio: HTTP {response.status_code}")
                    raise Exception(f"Failed to download audio: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"❌ Errore download audio: {e}")
            raise
    
    async def transcribe_audio(self, audio_data: bytes, content_type: str = "audio/ogg") -> Dict[str, Any]:
        """Trascrivi audio usando OpenAI Whisper API"""
        try:
            logger.info(f"🎙️ Iniziando trascrizione audio ({len(audio_data)} bytes, {content_type})")
            
            # Determina estensione file dal content type
            file_extension = self._get_file_extension(content_type)
            
            # Crea file temporaneo per Whisper
            with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            try:
                # Prepara richiesta multipart per Whisper API
                async with httpx.AsyncClient(timeout=60.0) as client:
                    with open(temp_file_path, 'rb') as audio_file:
                        files = {
                            'file': (f'audio{file_extension}', audio_file, content_type)
                        }
                        data = {
                            'model': 'whisper-1',
                            'language': 'it',  # Priorità italiano per Studio Immigrato
                            'response_format': 'json'
                        }
                        headers = {
                            'Authorization': f'Bearer {self.api_key}'
                        }
                        
                        response = await client.post(
                            self.base_url,
                            files=files,
                            data=data,
                            headers=headers
                        )
                
                if response.status_code == 200:
                    result = response.json()
                    transcript = result.get('text', '').strip()
                    
                    logger.info(f"✅ Trascrizione completata: '{transcript[:100]}...'")
                    
                    return {
                        "success": True,
                        "transcript": transcript,
                        "language": result.get('language', 'it'),
                        "duration": len(audio_data) / 16000,  # Stima durata
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    logger.error(f"❌ Whisper API error: {response.status_code} - {response.text}")
                    return {
                        "success": False,
                        "error": f"Whisper API error: {response.status_code}",
                        "transcript": ""
                    }
                    
            finally:
                # Pulisci file temporaneo
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
                    
        except Exception as e:
            logger.error(f"❌ Errore trascrizione Whisper: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcript": ""
            }
    
    def _get_file_extension(self, content_type: str) -> str:
        """Determina estensione file dal content type"""
        content_type_map = {
            "audio/ogg": ".ogg",
            "audio/mpeg": ".mp3",
            "audio/mp4": ".m4a",
            "audio/wav": ".wav",
            "audio/webm": ".webm",
            "audio/aac": ".aac"
        }
        return content_type_map.get(content_type, ".ogg")
    
    async def process_whatsapp_voice_message(self, media_url: str, content_type: str, user_phone: str) -> Dict[str, Any]:
        """Processo completo per messaggio vocale WhatsApp"""
        try:
            logger.info(f"🎙️ Processando messaggio vocale da {user_phone}")
            
            # 1. Scarica audio
            audio_data = await self.download_audio_from_url(media_url)
            
            # 2. Trascrivi con Whisper
            transcription_result = await self.transcribe_audio(audio_data, content_type)
            
            if transcription_result["success"]:
                transcript = transcription_result["transcript"]
                
                if transcript:
                    logger.info(f"🎯 Messaggio vocale trascritto: '{transcript}'")
                    return {
                        "success": True,
                        "transcript": transcript,
                        "original_type": "voice_message",
                        "user_phone": user_phone,
                        "processing_time": transcription_result.get("duration", 0),
                        "language": transcription_result.get("language", "it")
                    }
                else:
                    logger.warning("⚠️ Trascrizione vuota")
                    return {
                        "success": False,
                        "error": "Empty transcription",
                        "transcript": ""
                    }
            else:
                return transcription_result
                
        except Exception as e:
            logger.error(f"❌ Errore processo messaggio vocale: {e}")
            return {
                "success": False,
                "error": str(e),
                "transcript": ""
            }

# Istanza globale
whisper_transcription = WhisperTranscription() 