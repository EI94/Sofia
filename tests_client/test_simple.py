"""
Sofia Lite - Simple Import Tests
"""

import pytest

from sofia_lite.agents.context import Context
from sofia_lite.agents.prompt_builder import build_system_prompt
from sofia_lite.middleware.llm import chat, classify


def test_context_creation():
    """Test Context creation"""
    ctx = Context(phone="+393001234567", lang="it", state="GREETING")
    assert ctx.phone == "+393001234567"
    assert ctx.lang == "it"
    assert ctx.state == "GREETING"


def test_prompt_builder():
    """Test prompt builder"""
    ctx = Context(phone="+393001234567", lang="it", state="GREETING")
    prompt = build_system_prompt(ctx)
    assert "Sofia" in prompt
    assert "CURRENT_LANG: it" in prompt


def test_llm_functions():
    """Test LLM functions exist"""
    assert callable(classify)
    assert callable(chat)


if __name__ == "__main__":
    pytest.main([__file__])
