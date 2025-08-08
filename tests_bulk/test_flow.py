"""
Test flow per Sofia Bulk API
Happy path con TinyDB mock
"""

import pytest
import os
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from sofia_bulk_api.main import app


@pytest.mark.bulk
class TestConversationFlow:
    """Test per il flusso di conversazione"""
    
    def setup_method(self):
        """Setup per ogni test"""
        self.client = TestClient(app)
        self.base_url = "/api/sofia/conversation"
        self.valid_api_key = "test_api_key_123"
        
        # Set environment variables for testing
        os.environ["BULK_API_KEY"] = self.valid_api_key
        os.environ["CORE_SOFIA_URL"] = "https://test-sofia-core.run.app"
    
    def teardown_method(self):
        """Cleanup dopo ogni test"""
        # Clean up environment variables
        if "BULK_API_KEY" in os.environ:
            del os.environ["BULK_API_KEY"]
        if "CORE_SOFIA_URL" in os.environ:
            del os.environ["CORE_SOFIA_URL"]
    
    @patch('sofia_bulk_api.main.call_core_sofia')
    def test_post_conversation_happy_path(self, mock_call_core):
        """Test POST conversazione - happy path"""
        # Mock della risposta di Sofia Core
        mock_call_core.return_value = "Ciao! Sono Sofia di Studio Immigrato. Come posso aiutarti?"
        
        conversation_data = {
            "conversation_id": "test_conv_flow_1",
            "messages": [
                {"role": "user", "message": "Ciao, mi chiamo Mario"},
                {"role": "assistant", "message": ""},  # Sarà completato
                {"role": "user", "message": "Vorrei informazioni sulla cittadinanza"},
                {"role": "assistant", "message": ""}   # Sarà completato
            ]
        }
        
        headers = {"Authorization": f"Bearer {self.valid_api_key}"}
        response = self.client.post(self.base_url, json=conversation_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verifica struttura risposta
        assert data["conversation_id"] == "test_conv_flow_1"
        assert len(data["messages"]) == 4
        assert "timestamp_utc" in data
        
        # Verifica che i messaggi assistant siano stati completati
        assert data["messages"][1]["role"] == "assistant"
        assert data["messages"][1]["message"] == "Ciao! Sono Sofia di Studio Immigrato. Come posso aiutarti?"
        assert data["messages"][3]["role"] == "assistant"
        assert data["messages"][3]["message"] == "Ciao! Sono Sofia di Studio Immigrato. Come posso aiutarti?"
        
        # Verifica che call_core_sofia sia stato chiamato 2 volte
        assert mock_call_core.call_count == 2
    
    def test_get_conversation_happy_path(self):
        """Test GET conversazione - happy path"""
        # Prima crea una conversazione
        conversation_data = {
            "conversation_id": "test_conv_get_1",
            "messages": [
                {"role": "user", "message": "Ciao"},
                {"role": "assistant", "message": "Ciao! Come posso aiutarti?"}
            ]
        }
        
        headers = {"Authorization": f"Bearer {self.valid_api_key}"}
        
        # POST per creare la conversazione
        with patch('sofia_bulk_api.main.call_core_sofia') as mock_call_core:
            mock_call_core.return_value = "Ciao! Come posso aiutarti?"
            response = self.client.post(self.base_url, json=conversation_data, headers=headers)
            assert response.status_code == 200
        
        # GET per recuperare la conversazione
        response = self.client.get(f"{self.base_url}/test_conv_get_1", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["conversation_id"] == "test_conv_get_1"
        assert len(data["messages"]) == 2
        assert data["messages"][0]["role"] == "user"
        assert data["messages"][0]["message"] == "Ciao"
        assert data["messages"][1]["role"] == "assistant"
        assert data["messages"][1]["message"] == "Ciao! Come posso aiutarti?"
    
    def test_get_conversation_not_found(self):
        """Test GET conversazione non esistente - deve restituire 404"""
        headers = {"Authorization": f"Bearer {self.valid_api_key}"}
        response = self.client.get(f"{self.base_url}/non_existent_conv", headers=headers)
        
        assert response.status_code == 404
        assert "detail" in response.json()
    
    @patch('sofia_bulk_api.main.call_core_sofia')
    def test_conversation_with_no_empty_assistant_messages(self, mock_call_core):
        """Test conversazione senza messaggi assistant vuoti"""
        conversation_data = {
            "conversation_id": "test_conv_no_empty_1",
            "messages": [
                {"role": "user", "message": "Ciao"},
                {"role": "assistant", "message": "Ciao! Come posso aiutarti?"},
                {"role": "user", "message": "Grazie"},
                {"role": "assistant", "message": "Prego!"}
            ]
        }
        
        headers = {"Authorization": f"Bearer {self.valid_api_key}"}
        response = self.client.post(self.base_url, json=conversation_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verifica che call_core_sofia non sia stato chiamato
        mock_call_core.assert_not_called()
        
        # Verifica che i messaggi siano rimasti invariati
        assert data["messages"][1]["message"] == "Ciao! Come posso aiutarti?"
        assert data["messages"][3]["message"] == "Prego!"
    
    @patch('sofia_bulk_api.main.call_core_sofia')
    def test_conversation_with_mixed_empty_messages(self, mock_call_core):
        """Test conversazione con alcuni messaggi assistant vuoti"""
        # Mock diverse risposte per chiamate diverse
        mock_call_core.side_effect = [
            "Ciao! Sono Sofia.",
            "Ti spiego i requisiti per la cittadinanza."
        ]
        
        conversation_data = {
            "conversation_id": "test_conv_mixed_1",
            "messages": [
                {"role": "user", "message": "Ciao"},
                {"role": "assistant", "message": ""},  # Sarà completato
                {"role": "user", "message": "Vorrei informazioni sulla cittadinanza"},
                {"role": "assistant", "message": "Certo!"},  # Già completo
                {"role": "user", "message": "Quali sono i requisiti?"},
                {"role": "assistant", "message": ""}   # Sarà completato
            ]
        }
        
        headers = {"Authorization": f"Bearer {self.valid_api_key}"}
        response = self.client.post(self.base_url, json=conversation_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verifica che call_core_sofia sia stato chiamato 2 volte
        assert mock_call_core.call_count == 2
        
        # Verifica i messaggi completati
        assert data["messages"][1]["message"] == "Ciao! Sono Sofia."
        assert data["messages"][3]["message"] == "Certo!"  # Invariato
        assert data["messages"][5]["message"] == "Ti spiego i requisiti per la cittadinanza."
