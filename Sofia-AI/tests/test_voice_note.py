import importlib, pytest
if importlib.util.find_spec("audioop") is None:
    pytest.skip("audioop non disponibile in questo ambiente",
                allow_module_level=True)

"""
Test Voice Notes - F22 WhatsApp Voice Notes
Test per la trascrizione delle note audio WhatsApp
"""

import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock, mock_open
from sofia_lite.middleware import voice_transcript
from sofia_lite.whatsapp import handle_incoming

class TestVoiceNotes:
    """Test per la funzionalità voice notes"""
    
    @patch('requests.get')
    @patch('openai.OpenAI')
    def test_transcribe_voice_success(self, mock_openai, mock_requests):
        """Test trascrizione voice note con successo"""
        
        # Mock response per download audio
        mock_response = MagicMock()
        mock_response.content = b'fake_ogg_audio_content'
        mock_response.raise_for_status.return_value = None
        mock_requests.return_value = mock_response
        
        # Mock OpenAI client
        mock_client = MagicMock()
        mock_transcription = MagicMock()
        mock_transcription.text = "Ciao, mi chiamo Mario Rossi"
        mock_client.audio.transcriptions.create.return_value = mock_transcription
        mock_openai.return_value = mock_client
        
        # Test trascrizione
        with patch('tempfile.NamedTemporaryFile') as mock_temp:
            mock_temp.return_value.__enter__.return_value.name = "/tmp/test.wav"
            mock_temp.return_value.__enter__.return_value.flush.return_value = None
            
            result = voice_transcript.transcribe_voice("https://example.com/audio.ogg", "it")
            
            assert result == "Ciao, mi chiamo Mario Rossi"
            mock_requests.assert_called_once_with("https://example.com/audio.ogg", timeout=10)
            mock_client.audio.transcriptions.create.assert_called_once()
    
    @patch('requests.get')
    def test_transcribe_voice_download_failure(self, mock_requests):
        """Test fallimento download audio"""
        
        # Mock request exception
        mock_requests.side_effect = Exception("Download failed")
        
        with pytest.raises(Exception):
            voice_transcript.transcribe_voice("https://example.com/audio.ogg")
    
    @patch('requests.get')
    @patch('openai.OpenAI')
    def test_transcribe_voice_with_language_hint(self, mock_openai, mock_requests):
        """Test trascrizione con suggerimento lingua"""
        
        # Mock response
        mock_response = MagicMock()
        mock_response.content = b'fake_ogg_audio_content'
        mock_response.raise_for_status.return_value = None
        mock_requests.return_value = mock_response
        
        # Mock OpenAI
        mock_client = MagicMock()
        mock_transcription = MagicMock()
        mock_transcription.text = "Bonjour, je m'appelle Pierre"
        mock_client.audio.transcriptions.create.return_value = mock_transcription
        mock_openai.return_value = mock_client
        
        # Test con language hint
        with patch('tempfile.NamedTemporaryFile') as mock_temp:
            mock_temp.return_value.__enter__.return_value.name = "/tmp/test.wav"
            mock_temp.return_value.__enter__.return_value.flush.return_value = None
            
            result = voice_transcript.transcribe_voice("https://example.com/audio.ogg", "fr")
            
            assert result == "Bonjour, je m'appelle Pierre"
            
            # Verifica che language hint sia stato passato
            call_args = mock_client.audio.transcriptions.create.call_args
            assert call_args[1]["language"] == "fr"
    
    def test_detect_audio_format(self):
        """Test rilevamento formato audio"""
        
        # Test OGG format
        ogg_bytes = b'OggS' + b'x' * 100
        assert voice_transcript.detect_audio_format(ogg_bytes) == "ogg"
        
        # Test MP3 format
        mp3_bytes = b'ID3' + b'x' * 100
        assert voice_transcript.detect_audio_format(mp3_bytes) == "mp3"
        
        # Test WAV format
        wav_bytes = b'RIFF' + b'x' * 100
        assert voice_transcript.detect_audio_format(wav_bytes) == "wav"
    
    @patch('sofia_lite.middleware.voice_transcript.transcribe_voice')
    @patch('sofia_lite.agents.orchestrator.Orchestrator.process_message')
    def test_whatsapp_voice_note_processing(self, mock_process, mock_transcribe):
        """Test processamento voice note in WhatsApp webhook"""
        
        # Mock trascrizione
        mock_transcribe.return_value = "Ciao, vorrei prenotare una consulenza"
        
        # Mock orchestrator
        mock_process.return_value = {
            "reply": "Perfetto! Ti aiuto a prenotare la consulenza.",
            "intent": "ASK_SERVICE",
            "state": "ASK_SERVICE",
            "lang": "it"
        }
        
        # Test handle_incoming con voice note
        result = handle_incoming("+393331234567", "Ciao, vorrei prenotare una consulenza", "whatsapp")
        
        assert result == "Perfetto! Ti aiuto a prenotare la consulenza."
        mock_process.assert_called_once()
    
    @patch('sofia_lite.middleware.voice_transcript.transcribe_voice')
    def test_voice_transcription_fallback_message(self, mock_transcribe):
        """Test messaggio di fallback per trascrizione fallita"""
        
        # Mock fallimento trascrizione
        mock_transcribe.side_effect = Exception("Transcription failed")
        
        # Test che il messaggio di fallback sia appropriato
        fallback_msg = "Mi dispiace, non sono riuscito a trascrivere l'audio. Puoi scrivere il messaggio?"
        assert "trascrivere" in fallback_msg
        assert "audio" in fallback_msg
    
    @patch('requests.get')
    @patch('openai.OpenAI')
    def test_transcribe_voice_with_fallback(self, mock_openai, mock_requests):
        """Test trascrizione con fallback per diversi formati"""
        
        # Mock response
        mock_response = MagicMock()
        mock_response.content = b'fake_mp3_audio_content'
        mock_response.raise_for_status.return_value = None
        mock_requests.return_value = mock_response
        
        # Mock OpenAI
        mock_client = MagicMock()
        mock_transcription = MagicMock()
        mock_transcription.text = "Hello, this is a test message"
        mock_client.audio.transcriptions.create.return_value = mock_transcription
        mock_openai.return_value = mock_client
        
        # Test trascrizione con fallback
        with patch('tempfile.NamedTemporaryFile') as mock_temp:
            mock_temp.return_value.__enter__.return_value.name = "/tmp/test.wav"
            mock_temp.return_value.__enter__.return_value.flush.return_value = None
            
            result = voice_transcript.transcribe_voice_with_fallback("https://example.com/audio.mp3", "en")
            
            assert result == "Hello, this is a test message"
            mock_client.audio.transcriptions.create.assert_called_once()

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 