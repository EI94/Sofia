import os
import pytest
from twilio.rest import Client

@pytest.fixture(scope="session")
def twilio_client():
    sid = os.getenv("TWILIO_ACCOUNT_SID_TEST") or os.getenv("TWILIO_ACCOUNT_SID")
    tok = os.getenv("TWILIO_AUTH_TOKEN_TEST")  or os.getenv("TWILIO_AUTH_TOKEN")
    if not sid or not tok:
        pytest.skip("No Twilio creds configured for e2e tests")
    if "TEST" not in sid and not sid.startswith("AC"):
        pytest.skip("No Twilio test creds configured for e2e tests")
    return Client(sid, tok)

@pytest.fixture(scope="session")
def staging_url():
    url = os.getenv("SOFIA_STAGING_URL", "").rstrip("/")
    if not url:
        pytest.skip("SOFIA_STAGING_URL not set")
    return url

@pytest.fixture(scope="session")
def wa_from():
    return os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+18149149892")

@pytest.fixture(scope="session")
def voice_from():
    return os.getenv("TWILIO_VOICE_FROM", "+18149149892") 