"""
ElevenLabs Real-Time Streaming per Sofia AI Voice System
Integrazione avanzata con Twilio Media Streams per voice quality superiore
"""

import os
import json
import asyncio
import websockets
import logging
import base64
from typing import Optional, Dict, Any, AsyncIterator
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect
import httpx
from app.tools.elevenlabs_tts import SOFIA_VOICES, ELEVENLABS_API_KEY

logger = logging.getLogger(__name__)

# Configurazione streaming
ELEVENLABS_WS_URL = "wss://api.elevenlabs.io/v1/text-to-speech"
SAMPLE_RATE = 8000  # Twilio richiede 8kHz
AUDIO_CHUNK_SIZE = 1024

class ElevenLabsStreamer:
    """
    ElevenLabs Real-Time Streaming TTS per integrazione Twilio
    Gestisce streaming audio bidirezionale con buffer ottimizzato
    """
    
    def __init__(self, voice_id: str = SOFIA_VOICES["sarah"]):
        self.api_key = ELEVENLABS_API_KEY
        self.voice_id = voice_id
        self.is_streaming = False
        self.audio_buffer = asyncio.Queue()
        self.stream_config = {
            "text": "",
            "voice_settings": {
                "stability": 0.6,
                "similarity_boost": 0.8,
                "style": 0.3,
                "use_speaker_boost": True
            },
            "generation_config": {
                "chunk_length_schedule": [120, 160, 250, 290]  # Chunk schedule per real-time
            },
            "output_format": "pcm_8000"  # 8kHz PCM per Twilio
        }
        
    async def stream_text_to_audio(self, text: str) -> AsyncIterator[bytes]:
        """
        Streaming text-to-speech ElevenLabs con chunking intelligente
        
        Args:
            text: Testo da sintetizzare in streaming
            
        Yields:
            bytes: Audio chunks PCM 8kHz per Twilio
        """
        if not self.api_key:
            logger.error("❌ ElevenLabs API key mancante per streaming")
            return
            
        try:
            # URL streaming con voice ID
            ws_url = f"{ELEVENLABS_WS_URL}/{self.voice_id}/stream"
            
            headers = {
                "xi-api-key": self.api_key,
            }
            
            # Configurazione streaming request
            stream_request = {
                **self.stream_config,
                "text": text
            }
            
            logger.info(f"🎵 Avvio streaming ElevenLabs: '{text[:50]}...'")
            
            async with httpx.AsyncClient() as client:
                # Streaming HTTP request (ElevenLabs supporta streaming via HTTP)
                async with client.stream(
                    "POST",
                    f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream",
                    headers={
                        "Accept": "audio/mpeg",
                        "Content-Type": "application/json", 
                        "xi-api-key": self.api_key
                    },
                    json={
                        "text": text,
                        "model_id": "eleven_multilingual_v2",
                        "voice_settings": self.stream_config["voice_settings"]
                    },
                    timeout=30.0
                ) as response:
                    
                    if response.status_code != 200:
                        logger.error(f"❌ Streaming ElevenLabs fallito: {response.status_code}")
                        return
                    
                    logger.info("✅ Streaming ElevenLabs avviato")
                    chunk_count = 0
                    
                    async for chunk in response.aiter_bytes(chunk_size=AUDIO_CHUNK_SIZE):
                        if chunk:
                            chunk_count += 1
                            logger.debug(f"🎵 Audio chunk {chunk_count}: {len(chunk)} bytes")
                            yield chunk
                            
                            # Micro-pausa per non sovraccaricare
                            await asyncio.sleep(0.001)
                    
                    logger.info(f"✅ Streaming completato: {chunk_count} chunks audio")
                    
        except Exception as e:
            logger.error(f"❌ Errore streaming ElevenLabs: {e}")
            raise


class TwilioMediaStreamHandler:
    """
    Handler WebSocket per Twilio Media Streams
    Gestisce comunicazione bidirezionale audio con Twilio
    """
    
    def __init__(self):
        self.active_streams = {}  # call_sid -> stream_info
        self.elevenlabs_streamer = ElevenLabsStreamer()
        
    async def handle_media_stream(self, websocket: WebSocket, call_sid: str):
        """
        Gestisce WebSocket connection Twilio Media Stream
        
        Args:
            websocket: WebSocket connection da Twilio
            call_sid: Twilio Call SID identificativo
        """
        await websocket.accept()
        logger.info(f"📞 Media Stream connesso: {call_sid}")
        
        try:
            self.active_streams[call_sid] = {
                "websocket": websocket,
                "stream_sid": None,
                "start_time": datetime.now(),
                "audio_sent": 0,
                "audio_received": 0
            }
            
            # Loop principale gestione messaggi Twilio
            async for message in websocket.iter_text():
                await self._process_twilio_message(call_sid, message)
                
        except WebSocketDisconnect:
            logger.info(f"📞 Media Stream disconnesso: {call_sid}")
        except Exception as e:
            logger.error(f"❌ Errore Media Stream {call_sid}: {e}")
        finally:
            # Cleanup
            if call_sid in self.active_streams:
                del self.active_streams[call_sid]
    
    async def _process_twilio_message(self, call_sid: str, message: str):
        """Processa messaggi incoming da Twilio Media Stream"""
        try:
            data = json.loads(message)
            event = data.get("event")
            
            if event == "connected":
                logger.info(f"📞 Stream {call_sid} connesso - Protocol: {data.get('protocol')}")
                
            elif event == "start":
                # Stream started
                stream_sid = data.get("streamSid") 
                self.active_streams[call_sid]["stream_sid"] = stream_sid
                logger.info(f"🎵 Stream audio started: {stream_sid}")
                
            elif event == "media":
                # Audio ricevuto dal cliente (input vocale)
                payload = data.get("media", {})
                audio_b64 = payload.get("payload", "")
                
                if audio_b64:
                    # Decodifica audio PCM dal cliente
                    audio_bytes = base64.b64decode(audio_b64)
                    self.active_streams[call_sid]["audio_received"] += len(audio_bytes)
                    
                    # Speech-to-text gestito dal sistema Whisper
                    logger.debug(f"🎤 Audio ricevuto: {len(audio_bytes)} bytes")
                    
            elif event == "stop":
                logger.info(f"📞 Stream {call_sid} terminato")
                
        except Exception as e:
            logger.error(f"❌ Errore processing message Twilio: {e}")
    
    async def send_audio_to_twilio(self, call_sid: str, text_response: str):
        """
        Invia audio generato da ElevenLabs a Twilio via Media Stream
        
        Args:
            call_sid: Twilio Call SID
            text_response: Testo da sintetizzare e streammare
        """
        if call_sid not in self.active_streams:
            logger.error(f"❌ Stream {call_sid} non attivo")
            return
            
        stream_info = self.active_streams[call_sid]
        websocket = stream_info["websocket"]
        stream_sid = stream_info.get("stream_sid")
        
        if not stream_sid:
            logger.error(f"❌ Stream SID mancante per {call_sid}")
            return
            
        try:
            logger.info(f"🎵 Streaming audio a Twilio: '{text_response[:50]}...'")
            
            # Streaming ElevenLabs → Twilio
            audio_chunks_sent = 0
            
            async for audio_chunk in self.elevenlabs_streamer.stream_text_to_audio(text_response):
                # Codifica audio chunk per Twilio
                audio_b64 = base64.b64encode(audio_chunk).decode('utf-8')
                
                # Messaggio Media Stream per Twilio
                twilio_media_msg = {
                    "event": "media",
                    "streamSid": stream_sid,
                    "media": {
                        "payload": audio_b64
                    }
                }
                
                # Invia chunk audio a Twilio
                await websocket.send_text(json.dumps(twilio_media_msg))
                audio_chunks_sent += 1
                
                # Update statistics
                stream_info["audio_sent"] += len(audio_chunk)
                
                # Rate limiting per non sovraccaricare
                await asyncio.sleep(0.05)  # 50ms tra chunk
            
            logger.info(f"✅ Streaming completato: {audio_chunks_sent} chunks inviati a Twilio")
            
            # Mark fine stream (opzionale)
            mark_msg = {
                "event": "mark",
                "streamSid": stream_sid,
                "mark": {
                    "name": f"sofia_response_complete_{datetime.now().timestamp()}"
                }
            }
            await websocket.send_text(json.dumps(mark_msg))
            
        except Exception as e:
            logger.error(f"❌ Errore invio audio a Twilio: {e}")


class AudioStreamCoordinator:
    """
    Coordinatore principale per pipeline LLM → ElevenLabs → Twilio
    Orchestratore intelligente per streaming audio end-to-end
    """
    
    def __init__(self):
        self.twilio_handler = TwilioMediaStreamHandler()
        self.active_calls = {}
        
    async def process_voice_interaction(self, call_sid: str, user_speech: str) -> str:
        """
        Processa interazione vocale completa con streaming audio
        
        Args:
            call_sid: Twilio Call SID
            user_speech: Testo trascritto dall'utente
            
        Returns:
            str: Testo risposta (per logging, audio streamato separatamente)
        """
        try:
            logger.info(f"🎤 Processing voice interaction: {call_sid}")
            
            # 1. Processa input con Sofia AI (già implementato nel planner)
            from app.planner.planner import sofia_planner
            
            # Simula numero per ora (in produzione verrà da Twilio)
            phone_number = f"+1{call_sid[-10:]}"  # Estrai numero da call_sid
            
            # Genera risposta AI
            ai_response = await sofia_planner.plan_voice_response(
                phone_number, 
                user_speech,
                {"status": "new", "data": {}},  # Default per ora
                "it",
                "richiesta informazioni"
            )
            
            # 2. Streaming audio response via ElevenLabs → Twilio
            await self.twilio_handler.send_audio_to_twilio(call_sid, ai_response)
            
            logger.info(f"✅ Voice interaction completata: {call_sid}")
            return ai_response
            
        except Exception as e:
            logger.error(f"❌ Errore voice interaction: {e}")
            
            # Fallback response
            fallback = "Mi dispiace, c'è stato un problema tecnico. Può ripetere?"
            await self.twilio_handler.send_audio_to_twilio(call_sid, fallback)
            return fallback
    
    def get_stream_stats(self, call_sid: str) -> Optional[Dict[str, Any]]:
        """Statistiche stream per call specifica"""
        if call_sid in self.twilio_handler.active_streams:
            return self.twilio_handler.active_streams[call_sid]
        return None


# Istanze globali
audio_coordinator = AudioStreamCoordinator()
twilio_media_handler = TwilioMediaStreamHandler()

# Export per uso esterno
__all__ = [
    "ElevenLabsStreamer",
    "TwilioMediaStreamHandler", 
    "AudioStreamCoordinator",
    "audio_coordinator",
    "twilio_media_handler"
] 