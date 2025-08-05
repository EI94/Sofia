#!/usr/bin/env python3
"""
Test per i hotfix della state machine
"""

import pytest
from sofia_lite.agents.state import State, can_transition
from sofia_lite.agents.validator import validate
from sofia_lite.agents.context import Context
from sofia_lite.agents.planner import next_state

def test_self_transition_allowed():
    """Test che self-transition sia permessa"""
    # GREETING + GREET → rimane GREETING
    assert can_transition(State.GREETING, State.GREETING) == True
    
    # ASK_NAME + ASK_NAME → rimane ASK_NAME
    assert can_transition(State.ASK_NAME, State.ASK_NAME) == True
    
    # ASK_SERVICE + ASK_SERVICE → rimane ASK_SERVICE
    assert can_transition(State.ASK_SERVICE, State.ASK_SERVICE) == True

def test_auto_advance_greeting():
    """Test auto-advance da GREETING"""
    from sofia_lite.agents.state import ALLOWED_TRANSITIONS
    
    # GREETING + ASK_SERVICE intent → ASK_SERVICE
    assert ALLOWED_TRANSITIONS.get(("GREETING", "ASK_SERVICE")) == "ASK_SERVICE"
    
    # GREETING + ASK_NAME intent → ASK_NAME
    assert ALLOWED_TRANSITIONS.get(("GREETING", "ASK_NAME")) == "ASK_NAME"
    
    # GREETING + GREET intent → ASK_NAME
    assert ALLOWED_TRANSITIONS.get(("GREETING", "GREET")) == "ASK_NAME"

def test_validator_warning():
    """Test che invalid transition ritorna warning non clarifica"""
    ctx = Context(
        phone="+393521110000",
        lang="it",
        name=None,
        client_type="new",
        state="GREETING",
        asked_name=False,
        slots={},
        history=[]
    )
    
    # Invalid transition: GREETING + ASK_PAYMENT
    new_state, intent, warning = validate(ctx, "ASK_PAYMENT", 0.8)
    assert warning == "WARN_INVALID_TRANS"
    assert intent == "ASK_PAYMENT"  # Ritorna intent originale
    assert new_state == "GREETING"  # Stato corrente

def test_validator_low_confidence():
    """Test che low confidence forza CLARIFY"""
    ctx = Context(
        phone="+393521110000",
        lang="it",
        name=None,
        client_type="new",
        state="GREETING",
        asked_name=False,
        slots={},
        history=[]
    )
    
    # Low confidence
    new_state, intent, warning = validate(ctx, "GREET", 0.2)
    assert new_state == "ASK_CLARIFICATION"
    assert intent == "GREET"
    assert warning == "LOW_CONFIDENCE"

def test_validator_valid_transition():
    """Test che valid transition funziona"""
    ctx = Context(
        phone="+393521110000",
        lang="it",
        name=None,
        client_type="new",
        state="GREETING",
        asked_name=False,
        slots={},
        history=[]
    )
    
    # Valid transition: GREETING + GREET
    new_state, intent, warning = validate(ctx, "GREET", 0.8)
    assert intent == "GREET"
    assert new_state == "ASK_NAME"
    assert warning == "OK"

def test_greeting_auto_advance():
    """Test auto-advance da GREETING con context"""
    from sofia_lite.agents.state import ALLOWED_TRANSITIONS
    
    # Test GREETING + GREET → ASK_NAME (sempre, indipendentemente dal nome)
    new_state = ALLOWED_TRANSITIONS.get(("GREETING", "GREET"))
    assert new_state == "ASK_NAME"

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 