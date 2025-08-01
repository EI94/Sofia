"""
Sofia Lite - Simple Orchestrator Test
"""

import pytest
import asyncio
from sofia_lite.agents.orchestrator import Orchestrator
from sofia_lite.agents.context import Context

def test_orchestrator_creation():
    """Test orchestrator can be created"""
    orchestrator = Orchestrator()
    assert orchestrator is not None

def test_orchestrator_process_message():
    """Test orchestrator can process a message"""
    orchestrator = Orchestrator()
    result = orchestrator.process_message("+393001234567", "ciao")
    assert result is not None
    assert "reply" in result
    assert "intent" in result
    assert "state" in result
    assert "lang" in result
    assert "phone" in result

if __name__ == "__main__":
    pytest.main([__file__])
