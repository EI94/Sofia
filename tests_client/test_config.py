"""
Sofia Lite - Configuration Tests
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from sofia_lite import get_config, validate_config


def test_env_loaded(monkeypatch):
    """Test that environment variables are loaded correctly"""
    # Clear cache first
    get_config.cache_clear()

    monkeypatch.setenv("OPENAI_API_KEY", "test_openai_key")
    monkeypatch.setenv("ELEVENLABS_API_KEY", "test_eleven_key")
    monkeypatch.setenv("GOOGLE_PROJECT_ID", "test_project")
    monkeypatch.setenv("TWILIO_ACCOUNT_SID", "test_twilio_sid")
    monkeypatch.setenv("TWILIO_AUTH_TOKEN", "test_twilio_token")
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", "/test/credentials.json")

    config = get_config()

    assert config["OPENAI_KEY"] == "test_openai_key"
    assert config["ELEVEN_KEY"] == "test_eleven_key"
    assert config["GCLOUD_PROJECT"] == "test_project"
    assert config["TWILIO_SID"] == "test_twilio_sid"
    assert config["TWILIO_TOKEN"] == "test_twilio_token"
    assert config["GOOGLE_CREDENTIALS"] == "/test/credentials.json"


def test_config_caching():
    """Test that get_config is cached (returns same object)"""
    config1 = get_config()
    config2 = get_config()
    assert config1 is config2


def test_validate_config_success(monkeypatch):
    """Test that validate_config passes with required keys"""
    # Clear cache first
    get_config.cache_clear()

    monkeypatch.setenv("OPENAI_API_KEY", "test_key")
    monkeypatch.setenv("GOOGLE_PROJECT_ID", "test_project")

    config = validate_config()
    assert config["OPENAI_KEY"] == "test_key"
    assert config["GCLOUD_PROJECT"] == "test_project"


def test_validate_config_missing_keys(monkeypatch):
    """Test that validate_config raises error with missing keys"""
    # Clear cache first
    get_config.cache_clear()

    # Remove required keys
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_PROJECT_ID", raising=False)

    with pytest.raises(RuntimeError, match="Missing required configuration"):
        validate_config()


def test_default_values():
    """Test that default values are set correctly"""
    # Clear cache first
    get_config.cache_clear()

    # Clear all env vars
    for key in [
        "OPENAI_API_KEY",
        "ELEVENLABS_API_KEY",
        "GOOGLE_PROJECT_ID",
        "TWILIO_ACCOUNT_SID",
        "TWILIO_AUTH_TOKEN",
        "GOOGLE_APPLICATION_CREDENTIALS",
    ]:
        if key in os.environ:
            del os.environ[key]

    config = get_config()

    assert config["OPENAI_KEY"] == ""
    assert config["ELEVEN_KEY"] == ""
    assert config["GCLOUD_PROJECT"] == "local-dev"  # Default value
    assert config["TWILIO_SID"] == ""
    assert config["TWILIO_TOKEN"] == ""
    assert config["GOOGLE_CREDENTIALS"] == ""


if __name__ == "__main__":
    pytest.main([__file__])
