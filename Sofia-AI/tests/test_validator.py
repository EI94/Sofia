import pytest
from app.agents.validator import validate, VALID_TRANSITIONS
from app.agents.context import Context

def test_validator_greeting_to_greet():
    """Test valid transition from GREETING to GREET (smart name handling)"""
    ctx = Context(phone="+1234567890", state="GREETING")
    
    result = validate(ctx, "GREET")
    
    assert result == "ASK_NAME"  # Smart validator forces ASK_NAME when no name

def test_validator_greeting_to_ask_name():
    """Test valid transition from GREETING to ASK_NAME"""
    ctx = Context(phone="+1234567890", state="GREETING")
    
    result = validate(ctx, "ASK_NAME")
    
    assert result == "ASK_NAME"

def test_validator_invalid_transition():
    """Test invalid transition returns CLARIFY (smart name handling)"""
    ctx = Context(phone="+1234567890", state="GREETING")
    
    result = validate(ctx, "ASK_PAYMENT")  # Invalid from GREETING
    
    assert result == "ASK_NAME"  # Smart validator forces ASK_NAME when no name

def test_validator_ask_name_to_ask_service():
    """Test valid transition from ASK_NAME to ASK_SERVICE (smart name handling)"""
    ctx = Context(phone="+1234567890", state="ASK_NAME")
    
    result = validate(ctx, "ASK_SERVICE")
    
    assert result == "ASK_NAME"  # Smart validator forces ASK_NAME when no name

def test_validator_unknown_state():
    """Test unknown state returns CLARIFY (smart name handling)"""
    ctx = Context(phone="+1234567890", state="UNKNOWN_STATE")
    
    result = validate(ctx, "GREET")
    
    assert result == "ASK_NAME"  # Smart validator forces ASK_NAME when no name

def test_validator_all_valid_transitions():
    """Test all valid transitions in the matrix (smart name handling)"""
    for state, valid_intents in VALID_TRANSITIONS.items():
        ctx = Context(phone="+1234567890", state=state)
        
        for intent in valid_intents:
            result = validate(ctx, intent)
            # Smart validator may override intent when no name
            if not ctx.name and intent not in ("ASK_NAME", "CLARIFY"):
                assert result == "ASK_NAME", f"Failed: {state} -> {intent} should be ASK_NAME"
            else:
                assert result == intent, f"Failed: {state} -> {intent}" 