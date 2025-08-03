#!/usr/bin/env python3
"""
Test per i hotfix della state machine
"""

import pytest
from sofia_lite.agents.state import State, can_transition, auto_advance, advance_from_greeting
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
    # GREETING + ASK_SERVICE intent → stato "ASK_SERVICE"
    result = auto_advance("GREETING", "ASK_SERVICE")
    assert result == "ASK_SERVICE"
    
    # GREETING + ASK_NAME intent → stato "ASK_NAME"
    result = auto_advance("GREETING", "ASK_NAME")
    assert result == "ASK_NAME"
    
    # GREETING + GREET intent → rimane GREETING
    result = auto_advance("GREETING", "GREET")
    assert result == "GREETING"

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
    intent, state, warning = validate(ctx, "ASK_PAYMENT", 0.8)
    assert warning == "WARN_INVALID_TRANS"
    assert intent == "GREETING"  # Mantiene stato corrente
    assert state == "ASK_PAYMENT"  # Intent originale

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
    intent, state, warning = validate(ctx, "GREET", 0.2)
    assert intent == "CLARIFY"
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
    intent, state, warning = validate(ctx, "GREET", 0.8)
    assert intent == "GREET"
    assert warning == ""

def test_greeting_auto_advance():
    """Test auto-advance da GREETING con context"""
    ctx = Context(
        phone="+100",
        lang="it",
        name=None,
        client_type="new",
        state="GREETING",
        asked_name=False,
        slots={},
        history=[]
    )
    
    # Test GREETING + GREET → ASK_NAME (quando name è None)
    new_state = next_state(State.GREETING, "GREET", ctx)
    assert new_state == State.ASK_NAME
    
    # Test GREETING + GREET → ASK_SERVICE (quando name è presente)
    ctx.name = "Mario"
    new_state = next_state(State.GREETING, "GREET", ctx)
    assert new_state == State.ASK_SERVICE

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 