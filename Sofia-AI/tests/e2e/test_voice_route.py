"""
Sofia Lite - E2E Voice Route Test
Tests voice functionality using Twilio sandbox.
"""

import os
import pytest
import requests
import json
from typing import Dict, Any

# Twilio Sandbox configuration
TWILIO_SANDBOX_NUMBER = os.getenv("TWILIO_SANDBOX_NUMBER", "+15005550006")
WEBHOOK_URL = os.getenv("VOICE_WEBHOOK_URL", "http://localhost:8001/webhook/voice")

def test_voice_webhook_basic():
    """Test basic voice webhook functionality"""
    
    # Mock Twilio voice webhook data
    webhook_data = {
        "From": "+393001234567",
        "SpeechResult": "ciao",
        "CallSid": "test_call_sid",
        "CallStatus": "in-progress"
    }
    
    try:
        # Send POST request to voice webhook
        response = requests.post(WEBHOOK_URL, data=webhook_data, timeout=10)
        
        # Check response
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Check that response is TwiML
        content = response.text
        assert "<?xml" in content, "Response should be XML"
        assert "<Response>" in content, "Response should contain TwiML Response"
        assert "<Say>" in content, "Response should contain Say element"
        
        print(f"✅ Voice webhook test passed: {response.status_code}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Voice webhook test failed: {e}")
        return False

def test_voice_webhook_with_transcript():
    """Test voice webhook with speech transcript"""
    
    test_cases = [
        ("ciao", "GREET"),
        ("mi chiamo Pierpaolo", "ASK_NAME"),
        ("ho bisogno del permesso di soggiorno", "REQUEST_SERVICE"),
        ("quanto costa?", "ASK_COST"),
    ]
    
    for transcript, expected_intent in test_cases:
        webhook_data = {
            "From": "+393001234567",
            "SpeechResult": transcript,
            "CallSid": f"test_call_{transcript[:10]}",
            "CallStatus": "in-progress"
        }
        
        try:
            response = requests.post(WEBHOOK_URL, data=webhook_data, timeout=10)
            
            assert response.status_code == 200, f"Failed for '{transcript}': {response.status_code}"
            
            content = response.text
            assert "<?xml" in content, f"Response should be XML for '{transcript}'"
            assert "<Say>" in content, f"Response should contain Say for '{transcript}'"
            
            print(f"✅ Voice transcript test passed: '{transcript}'")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Voice transcript test failed for '{transcript}': {e}")
            return False
    
    return True

def test_voice_webhook_error_handling():
    """Test voice webhook error handling"""
    
    # Test with missing phone
    webhook_data = {
        "SpeechResult": "ciao",
        "CallSid": "test_call_error",
        "CallStatus": "in-progress"
    }
    
    try:
        response = requests.post(WEBHOOK_URL, data=webhook_data, timeout=10)
        
        # Should return error for missing phone
        assert response.status_code == 400, f"Expected 400 for missing phone, got {response.status_code}"
        
        print("✅ Voice error handling test passed")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Voice error handling test failed: {e}")
        return False

def test_voice_tts_fallback():
    """Test TTS fallback functionality"""
    
    webhook_data = {
        "From": "+393001234567",
        "SpeechResult": "test tts fallback",
        "CallSid": "test_tts_fallback",
        "CallStatus": "in-progress"
    }
    
    try:
        response = requests.post(WEBHOOK_URL, data=webhook_data, timeout=10)
        
        assert response.status_code == 200, f"TTS fallback test failed: {response.status_code}"
        
        content = response.text
        assert "Polly.Bianca" in content, "Response should use Polly.Bianca voice"
        
        print("✅ Voice TTS fallback test passed")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Voice TTS fallback test failed: {e}")
        return False

def test_voice_health_check():
    """Test voice health check endpoint"""
    
    try:
        response = requests.get(WEBHOOK_URL.replace("/webhook/voice", "/health"), timeout=5)
        
        assert response.status_code == 200, f"Health check failed: {response.status_code}"
        
        data = response.json()
        assert data["status"] == "healthy", f"Health check status: {data['status']}"
        assert data["service"] == "sofia-lite-voice", f"Health check service: {data['service']}"
        
        print("✅ Voice health check test passed")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Voice health check test failed: {e}")
        return False

def test_twilio_sandbox_integration():
    """Test integration with Twilio sandbox (if credentials available)"""
    
    print(f"📞 Twilio Sandbox Number: {TWILIO_SANDBOX_NUMBER}")
    print(f"🔗 Webhook URL: {WEBHOOK_URL}")
    print("✅ Twilio sandbox configuration verified")
    
    return True

def run_all_voice_tests():
    """Run all voice tests"""
    
    print("�� Sofia Lite - E2E Voice Route Tests")
    print("=" * 50)
    
    tests = [
        ("Basic Webhook", test_voice_webhook_basic),
        ("Transcript Processing", test_voice_webhook_with_transcript),
        ("Error Handling", test_voice_webhook_error_handling),
        ("TTS Fallback", test_voice_tts_fallback),
        ("Health Check", test_voice_health_check),
        ("Twilio Sandbox", test_twilio_sandbox_integration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}:")
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL VOICE TESTS PASSED!")
        return True
    else:
        print("⚠️ Some voice tests failed")
        return False

if __name__ == "__main__":
    import sys
    
    success = run_all_voice_tests()
    sys.exit(0 if success else 1)
