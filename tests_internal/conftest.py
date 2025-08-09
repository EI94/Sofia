import json
import os
from datetime import datetime
from unittest.mock import Mock, patch

import pytest

# Mock Twilio calls storage
TWILIO_CALLS_FILE = os.path.join(os.path.dirname(__file__), "_twilio_calls.json")


@pytest.fixture
def twilio_stub(monkeypatch):
    """Mock Twilio client for testing"""
    mock_client = Mock()
    mock_messages = Mock()
    mock_calls = Mock()

    # Mock message creation
    def mock_create(**kwargs):
        call_data = {
            "timestamp": datetime.now().isoformat(),
            "action": "create_message",
            "data": kwargs,
        }
        # Store call data
        calls = []
        if os.path.exists(TWILIO_CALLS_FILE):
            with open(TWILIO_CALLS_FILE, "r") as f:
                calls = json.load(f)
        calls.append(call_data)
        with open(TWILIO_CALLS_FILE, "w") as f:
            json.dump(calls, f, indent=2)

        # Return mock message
        mock_message = Mock()
        mock_message.sid = "MG_test_123"
        mock_message.status = "sent"
        return mock_message

    mock_messages.create = mock_create
    mock_client.messages = mock_messages
    mock_client.calls = mock_calls

    # Patch Twilio client
    with patch("twilio.rest.Client", return_value=mock_client):
        yield mock_client


@pytest.fixture
def calendar_stub(monkeypatch):
    """Mock Calendar gateway for testing"""
    mock_calendar = Mock()

    # Mock get_available_slots
    def mock_get_slots(date_str):
        # Return static slots for testing
        base_time = datetime.strptime(date_str, "%Y-%m-%d")
        slots = []
        for hour in [9, 10, 11, 14, 15, 16, 17]:
            slot_time = base_time.replace(hour=hour, minute=0)
            slots.append(slot_time.strftime("%Y-%m-%d %H:%M"))
        return slots

    # Mock book_appointment
    def mock_book_appointment(date_str, time_str, name, phone):
        return {
            "booking_id": "BK_test_123",
            "date": date_str,
            "time": time_str,
            "name": name,
            "phone": phone,
            "status": "confirmed",
        }

    mock_calendar.get_available_slots = mock_get_slots
    mock_calendar.book_appointment = mock_book_appointment

    # Patch calendar gateway
    with patch(
        "sofia_lite.middleware.calendar.CalendarGateway", return_value=mock_calendar
    ):
        yield mock_calendar


@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment variables"""
    os.environ["TEST_MODE"] = "true"
    os.environ["OPENAI_API_KEY"] = "sk-test"
    os.environ["TWILIO_ACCOUNT_SID"] = "AC_test"
    os.environ["TWILIO_AUTH_TOKEN"] = "tok_test"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/dev/null"
    yield
    # Cleanup
    if os.path.exists(TWILIO_CALLS_FILE):
        os.remove(TWILIO_CALLS_FILE)
