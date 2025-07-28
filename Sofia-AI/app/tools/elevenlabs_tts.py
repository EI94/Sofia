import os
import requests
import logging
import tempfile
from typing import Optional
from dotenv import load_dotenv

# Carica variabili ambiente
load_dotenv()

logger = logging.getLogger(__name__)

# Configurazione ElevenLabs
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_BASE_URL = "https://api.elevenlabs.io/v1"

# Voci italiane/femminili ottimizzate per Sofia
SOFIA_VOICES = {
    "aria": "9BWtsMINqrJLrRacOk9x",      # Femminile americana - naturale
    "sarah": "EXAVITQu4vr4xnSDxMaL",     # Femminile americana - calda 
    "laura": "FGY2WhTYpPnrIDTdsKH5",     # Femminile americana - professionale
    "alice": "Xb7hH8MSUJpSbSDYk0k2",     # Femminile britannica - elegante
    "charlotte": "XB0fDUnXU5powFXDhCwa"   # Femminile svedese - neutra
}

# Voce di default per Sofia (calda e professionale)
DEFAULT_VOICE_ID = SOFIA_VOICES["sarah"]


class ElevenLabsTTS:
    """Text-to-Speech engine usando ElevenLabs per Sofia AI"""
    
    def __init__(self, voice_id: str = DEFAULT_VOICE_ID):
        self.api_key = ELEVENLABS_API_KEY
        self.voice_id = voice_id
        self.base_url = ELEVENLABS_BASE_URL
        
        if not self.api_key:
            logger.warning("⚠️ ElevenLabs API key non configurata")
            self.enabled = False
        else:
            logger.info(f"✅ ElevenLabs TTS inizializzato - Voice: {voice_id}")
            self.enabled = True
    
    def is_available(self) -> bool:
        """Controlla se ElevenLabs è disponibile"""
        return self.enabled and bool(self.api_key)
    
    def get_available_voices(self) -> Optional[list]:
        """Recupera la lista delle voci disponibili"""
        if not self.is_available():
            return None
            
        try:
            headers = {"xi-api-key": self.api_key}
            response = requests.get(f"{self.base_url}/voices", headers=headers)
            
            if response.status_code == 200:
                return response.json().get("voices", [])
            else:
                logger.error(f"Errore API voci ElevenLabs: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Errore connessione ElevenLabs: {e}")
            return None
    
    async def synthesize_speech(self, 
                              text: str, 
                              voice_id: Optional[str] = None,
                              model: str = "eleven_multilingual_v2") -> Optional[bytes]:
        """
        Sintetizza testo in audio usando ElevenLabs
        
        Args:
            text: Testo da sintetizzare
            voice_id: ID della voce (default: Sarah)  
            model: Modello ElevenLabs da usare
            
        Returns:
            Audio bytes se successo, None se errore
        """
        if not self.is_available():
            logger.warning("ElevenLabs non disponibile per TTS")
            return None
            
        voice_id = voice_id or self.voice_id
        
        try:
            url = f"{self.base_url}/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }
            
            # Impostazioni vocali ottimizzate per Sofia (consulente italiana)
            data = {
                "text": text,
                "model_id": model,
                "voice_settings": {
                    "stability": 0.6,        # Stabilità voce (0.0-1.0)
                    "similarity_boost": 0.8, # Somiglianza al modello (0.0-1.0)
                    "style": 0.3,           # Stile espressivo (0.0-1.0)
                    "use_speaker_boost": True  # Boost qualità speaker
                }
            }
            
            logger.info(f"🗣️ Sintetizzazione: '{text[:50]}...' con voce {voice_id}")
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                audio_bytes = response.content
                logger.info(f"✅ Audio generato: {len(audio_bytes)} bytes")
                return audio_bytes
            else:
                logger.error(f"Errore sintesi ElevenLabs: {response.status_code}")
                logger.error(f"Risposta: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Errore durante sintesi vocale: {e}")
            return None
    
    async def synthesize_to_file(self, 
                                text: str, 
                                output_path: Optional[str] = None,
                                voice_id: Optional[str] = None) -> Optional[str]:
        """
        Sintetizza testo e salva in file audio
        
        Returns:
            Path del file audio generato
        """
        audio_bytes = await self.synthesize_speech(text, voice_id)
        
        if not audio_bytes:
            return None
            
        try:
            # Genera nome file se non specificato
            if not output_path:
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                    output_path = f.name
            
            # Salva audio su file
            with open(output_path, "wb") as f:
                f.write(audio_bytes)
                
            logger.info(f"💾 Audio salvato: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Errore salvataggio audio: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Test rapido della connessione ElevenLabs"""
        try:
            voices = self.get_available_voices()
            if voices:
                logger.info(f"🎭 Test connessione OK: {len(voices)} voci disponibili")
                return True
            return False
        except Exception as e:
            logger.error(f"Test connessione fallito: {e}")
            return False


# Istanza globale per Sofia
sofia_tts = ElevenLabsTTS()


async def generate_sofia_speech(text: str, voice_name: str = "sarah") -> Optional[bytes]:
    """
    Funzione di utilità per generare speech con la voce di Sofia
    
    Args:
        text: Testo da sintetizzare
        voice_name: Nome della voce Sofia (sarah, aria, laura, etc.)
        
    Returns:
        Audio bytes
    """
    voice_id = SOFIA_VOICES.get(voice_name.lower(), DEFAULT_VOICE_ID)
    return await sofia_tts.synthesize_speech(text, voice_id)


async def test_sofia_voice():
    """Test completo della voce di Sofia"""
    test_text = "Ciao! Sono Sofia dello Studio Immigrato di Milano. Come posso aiutarti oggi?"
    
    print("🎤 Test sintesi vocale Sofia con ElevenLabs...")
    
    # Test connessione
    if not sofia_tts.test_connection():
        print("❌ Connessione ElevenLabs fallita")
        return False
    
    # Test sintesi
    audio_bytes = await generate_sofia_speech(test_text)
    
    if audio_bytes:
        print(f"✅ Audio generato: {len(audio_bytes)} bytes")
        
        # Salva file di test
        output_file = await sofia_tts.synthesize_to_file(test_text)
        if output_file:
            print(f"💾 File audio salvato: {output_file}")
            print("🔊 Puoi riprodurre il file per sentire la voce di Sofia!")
            return True
    
    print("❌ Sintesi vocale fallita")
    return False


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_sofia_voice()) 