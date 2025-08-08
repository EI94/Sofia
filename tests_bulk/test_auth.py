"""
Test autenticazione per Sofia Bulk API
Verifica che le richieste senza API key restituiscano 401/403
"""

import pytest
from fastapi.testclient import TestClient
from sofia_bulk_api.main import app


@pytest.mark.bulk
class TestAuthentication:
    """Test per l'autenticazione API"""
    
    def setup_method(self):
        """Setup per ogni test"""
        self.client = TestClient(app)
        self.base_url = "/api/sofia/conversation"
    
    def test_post_conversation_without_auth(self):
        """Test POST senza autenticazione - deve restituire 403"""
        conversation_data = {
            "conversation_id": "test_conv_1",
            "messages": [
                {"role": "user", "message": "Ciao"},
                {"role": "assistant", "message": ""}
            ]
        }
        
        response = self.client.post(self.base_url, json=conversation_data)
        
        assert response.status_code == 403
        assert "detail" in response.json()
    
    def test_get_conversation_without_auth(self):
        """Test GET senza autenticazione - deve restituire 403"""
        response = self.client.get(f"{self.base_url}/test_conv_1")
        
        assert response.status_code == 403
        assert "detail" in response.json()
    
    def test_post_conversation_with_invalid_auth(self):
        """Test POST con API key non valida - deve restituire 500 (BULK_API_KEY non configurato)"""
        conversation_data = {
            "conversation_id": "test_conv_2",
            "messages": [
                {"role": "user", "message": "Ciao"},
                {"role": "assistant", "message": ""}
            ]
        }
        
        headers = {"Authorization": "Bearer invalid_key"}
        response = self.client.post(self.base_url, json=conversation_data, headers=headers)
        
        assert response.status_code == 500
        assert "detail" in response.json()
        assert "BULK_API_KEY non configurato" in response.json()["detail"]
    
    def test_get_conversation_with_invalid_auth(self):
        """Test GET con API key non valida - deve restituire 500 (BULK_API_KEY non configurato)"""
        headers = {"Authorization": "Bearer invalid_key"}
        response = self.client.get(f"{self.base_url}/test_conv_1", headers=headers)
        
        assert response.status_code == 500
        assert "detail" in response.json()
        assert "BULK_API_KEY non configurato" in response.json()["detail"]
    
    def test_post_conversation_with_malformed_auth(self):
        """Test POST con header Authorization malformato - deve restituire 403"""
        conversation_data = {
            "conversation_id": "test_conv_3",
            "messages": [
                {"role": "user", "message": "Ciao"},
                {"role": "assistant", "message": ""}
            ]
        }
        
        headers = {"Authorization": "InvalidFormat key123"}
        response = self.client.post(self.base_url, json=conversation_data, headers=headers)
        
        assert response.status_code == 403
        assert "detail" in response.json()
    
    def test_health_endpoint_no_auth_required(self):
        """Test che l'endpoint /health non richieda autenticazione"""
        response = self.client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "sofia-bulk-api"
    
    def test_root_endpoint_no_auth_required(self):
        """Test che l'endpoint / non richieda autenticazione"""
        response = self.client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Sofia Bulk API"
        assert data["version"] == "1.0.0"
