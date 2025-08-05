#!/usr/bin/env python3
"""
Test per il short-circuit di risposte prevedibili
"""

import pytest
from sofia_lite.agents import state, orchestrator
from sofia_lite.agents.context import Context

@pytest.mark.xfail(reason="legacy behaviour removed")
def test_greet_short_circuit(monkeypatch):
    """Test che GREET in GREETING state usa short-circuit"""
    # Mock per evitare chiamate LLM
    def mock_plan(ctx, message, chat):
        return "GREET", "Intent Engine 2.0: GREET (confidence: 0.99)"
    
    def mock_validate(ctx, intent, confidence):
        return intent, ctx.state, ""
    
    def mock_dispatch(intent, ctx, message):
        return "Mock dispatch response"
    
    # Mock delle funzioni
    monkeypatch.setattr(orchestrator, "plan", mock_plan)
    monkeypatch.setattr(orchestrator, "validate", mock_validate)
    monkeypatch.setattr(orchestrator, "dispatch", mock_dispatch)
    
    # Crea context in GREETING state
    ctx = Context(
        phone="+test",
        lang="it",
        name=None,
        client_type="new",
        state="GREETING",
        asked_name=False,
        slots={},
        history=[]
    )
    
    # Mock get_or_create_context per restituire il nostro context
    def mock_get_context(phone):
        return ctx
    
    monkeypatch.setattr(orchestrator, "get_or_create_context", mock_get_context)
    
    # Esegui process_message
    orchestrator_instance = orchestrator.Orchestrator()
    result = orchestrator_instance.process_message("+test", "Ciao")
    
    # Verifica che la risposta contenga "come ti chiami" (ora tramite dispatch normale)
    assert "come ti chiami" in result["reply"].lower()
    assert result["intent"] == "GREET"

@pytest.mark.xfail(reason="legacy behaviour removed")
def test_ask_name_short_circuit(monkeypatch):
    """Test che ASK_NAME in GREETING state usa short-circuit"""
    # Mock per evitare chiamate LLM
    def mock_plan(ctx, message, chat):
        return "ASK_NAME", "Intent Engine 2.0: ASK_NAME (confidence: 0.99)"
    
    def mock_validate(ctx, intent, confidence):
        return intent, ctx.state, ""
    
    def mock_dispatch(intent, ctx, message):
        return "Mock dispatch response"
    
    # Mock delle funzioni
    monkeypatch.setattr(orchestrator, "plan", mock_plan)
    monkeypatch.setattr(orchestrator, "validate", mock_validate)
    monkeypatch.setattr(orchestrator, "dispatch", mock_dispatch)
    
    # Crea context in GREETING state
    ctx = Context(
        phone="+test",
        lang="it",
        name=None,
        client_type="new",
        state="GREETING",
        asked_name=False,
        slots={},
        history=[]
    )
    
    # Mock get_or_create_context per restituire il nostro context
    def mock_get_context(phone):
        return ctx
    
    monkeypatch.setattr(orchestrator, "get_or_create_context", mock_get_context)
    
    # Esegui process_message
    orchestrator_instance = orchestrator.Orchestrator()
    result = orchestrator_instance.process_message("+test", "Mi chiamo Mario")
    
    # Verifica che la risposta contenga informazioni sui servizi (ora tramite dispatch normale)
    assert "servizi" in result["reply"].lower() or "consulenza" in result["reply"].lower()
    assert result["intent"] == "ASK_NAME"

def test_no_short_circuit_for_other_states(monkeypatch):
    """Test che non c'è short-circuit per altri stati"""
    # Mock per evitare chiamate LLM
    def mock_plan(ctx, message, chat):
        return "GREET", "Intent Engine 2.0: GREET (confidence: 0.99)"
    
    def mock_validate(ctx, intent, confidence):
        return intent, ctx.state, ""
    
    def mock_dispatch(intent, ctx, message):
        return "Mock dispatch response"
    
    # Mock delle funzioni
    monkeypatch.setattr(orchestrator, "plan", mock_plan)
    monkeypatch.setattr(orchestrator, "validate", mock_validate)
    monkeypatch.setattr(orchestrator, "dispatch", mock_dispatch)
    
    # Crea context in ASK_NAME state (non GREETING)
    ctx = Context(
        phone="+test",
        lang="it",
        name=None,
        client_type="new",
        state="ASK_NAME",  # Non GREETING
        asked_name=False,
        slots={},
        history=[]
    )
    
    # Mock get_or_create_context per restituire il nostro context
    def mock_get_context(phone):
        return ctx
    
    monkeypatch.setattr(orchestrator, "get_or_create_context", mock_get_context)
    
    # Esegui process_message
    orchestrator_instance = orchestrator.Orchestrator()
    result = orchestrator_instance.process_message("+test", "Ciao")
    
    # Verifica che usi dispatch normale (non short-circuit)
    assert result["reply"] == "Mock dispatch response"

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 