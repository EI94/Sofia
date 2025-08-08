"""
Sofia Lite - Secrets Management Tests
"""

import os
from unittest.mock import patch

import pytest


def test_llm_missing_openai_key():
    """Test that LLM raises RuntimeError when OPENAI_API_KEY is missing"""
    # Temporarily remove OPENAI_API_KEY
    original_key = os.environ.get("OPENAI_API_KEY")
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]

    try:
        # Test that LLM functions fail without API key
        from sofia_lite.middleware.llm import chat

        with pytest.raises(RuntimeError, match="missing OPENAI_API_KEY"):
            chat("test", "test")
    finally:
        # Restore original key
        if original_key:
            os.environ["OPENAI_API_KEY"] = original_key


def test_memory_missing_credentials():
    """Test that memory raises RuntimeError when credentials are missing"""
    # Temporarily remove credentials
    original_creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    original_project = os.environ.get("GOOGLE_PROJECT_ID")

    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    if "GOOGLE_PROJECT_ID" in os.environ:
        del os.environ["GOOGLE_PROJECT_ID"]

    try:
        # Test that memory functions fail without credentials
        from sofia_lite.middleware.memory import load_context

        with pytest.raises(
            RuntimeError, match="missing GOOGLE_APPLICATION_CREDENTIALS"
        ):
            load_context("+1234567890")
    finally:
        # Restore original credentials
        if original_creds:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = original_creds
        if original_project:
            os.environ["GOOGLE_PROJECT_ID"] = original_project


@pytest.mark.xfail(reason="Expected to fail without secrets")
def test_smoke_live_missing_secrets():
    """Test that smoke_live fails without secrets (expected behavior)"""
    # This test is expected to fail in CI without secrets
    from scripts.smoke_live import main

    main()


if __name__ == "__main__":
    pytest.main([__file__])
