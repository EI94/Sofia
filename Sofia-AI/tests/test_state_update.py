#!/usr/bin/env python3
"""
Test per verificare che lo stato persista correttamente dopo l'esecuzione dello skill
"""

import pytest
from sofia_lite.agents.context import Context
from sofia_lite.agents import executor, state

def test_state_persists_after_greet():
    """Test che lo stato passa da GREETING a ASK_NAME dopo GREET"""
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
    
    # Esegui dispatch con intent GREET
    response = executor.dispatch("GREET", ctx, "Ciao")
    
    # Verifica che lo stato sia cambiato da GREETING a ASK_NAME
    assert ctx.state == "ASK_NAME"
    assert "Ciao" in response or "Sofia" in response

def test_state_persists_after_greet_with_name():
    """Test che lo stato passa da GREETING a ASK_SERVICE se il nome è già presente"""
    ctx = Context(
        phone="+100",
        lang="it",
        name="Mario",  # Nome già presente
        client_type="new",
        state="GREETING",
        asked_name=False,
        slots={},
        history=[]
    )
    
    # Esegui dispatch con intent GREET
    response = executor.dispatch("GREET", ctx, "Ciao")
    
    # Verifica che lo stato sia cambiato da GREETING a ASK_SERVICE
    assert ctx.state == "ASK_SERVICE"

def test_state_unchanged_for_invalid_intent():
    """Test che lo stato rimane invariato per intent non validi"""
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
    
    original_state = ctx.state
    
    # Esegui dispatch con intent non valido
    response = executor.dispatch("INVALID_INTENT", ctx, "Test")
    
    # Verifica che lo stato sia rimasto invariato
    assert ctx.state == original_state

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 