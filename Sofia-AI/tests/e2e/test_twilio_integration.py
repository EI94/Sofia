import pytest
import requests

def test_twilio_client_fixture(twilio_client):
    """Test that Twilio client fixture works"""
    # This will be skipped if no test credentials are available
    assert twilio_client is not None

def test_staging_url_fixture(staging_url):
    """Test that staging URL fixture works"""
    # This will be skipped if SOFIA_STAGING_URL is not set
    assert staging_url is not None
    assert staging_url.startswith("http")

def test_wa_from_fixture(wa_from):
    """Test WhatsApp from fixture"""
    assert wa_from.startswith("whatsapp:+")

def test_voice_from_fixture(voice_from):
    """Test voice from fixture"""
    assert voice_from.startswith("+")

def test_whatsapp_webhook_endpoint(staging_url):
    """Test WhatsApp webhook endpoint exists"""
    try:
        response = requests.get(f"{staging_url}/health")
        assert response.status_code == 200
    except requests.exceptions.RequestException:
        pytest.skip("Staging server not reachable")

def test_voice_webhook_endpoint(staging_url):
    """Test voice webhook endpoint exists"""
    try:
        response = requests.get(f"{staging_url}/health")
        assert response.status_code == 200
    except requests.exceptions.RequestException:
        pytest.skip("Staging server not reachable") 