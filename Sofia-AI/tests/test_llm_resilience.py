#!/usr/bin/env python3
"""
Test per la resilienza del LLM con circuit breaker
"""

import pytest
import asyncio
import time
from sofia_lite.middleware import llm

def test_cb_opens_after_three_timeouts(monkeypatch):
    """Test che il circuit breaker si apre dopo 3 timeout"""
    # Mock _raw_chat per simulare timeout
    def boom(sys_prompt, user_prompt): 
        raise Exception("Mock timeout")
    
    monkeypatch.setattr(llm, "_raw_chat", boom)
    
    # Reset circuit breaker
    llm._CIRCUIT["fail"] = 0
    llm._CIRCUIT["open_until"] = 0
    
    # Simula 3 fallimenti
    for _ in range(3):
        result = llm.chat("System prompt", "User message")
        # Il fallback restituisce una risposta valida, non un errore
        assert isinstance(result, str) and len(result) > 0
    
    # Verifica che il circuit breaker sia aperto
    assert llm._CIRCUIT["open_until"] > time.time()

def test_cb_resets_after_success(monkeypatch):
    """Test che il circuit breaker si resetta dopo un successo"""
    # Reset circuit breaker (chiuso)
    llm._CIRCUIT["fail"] = 2
    llm._CIRCUIT["open_until"] = 0  # Chiuso
    
    # Mock _raw_chat per simulare successo
    def success(sys_prompt, user_prompt):
        return "Success response"
    
    monkeypatch.setattr(llm, "_raw_chat", success)
    
    # Esegui chiamata di successo
    result = llm.chat("System prompt", "User message")
    
    # Verifica che il circuit breaker sia resettato
    assert llm._CIRCUIT["fail"] == 0
    assert result == "Success response"

def test_fallback_returns_valid_response():
    """Test che il fallback restituisce una risposta valida"""
    # Forza circuit breaker aperto
    llm._CIRCUIT["open_until"] = time.time() + 60
    
    # Test fallback
    result = llm.chat("System prompt", "Ciao")
    
    # Verifica che restituisca una risposta valida
    assert isinstance(result, str)
    assert len(result) > 0
    assert "mi dispiace" in result.lower() or "ciao" in result.lower()

def test_cb_closes_after_timeout():
    """Test che il circuit breaker si chiude dopo il timeout"""
    # Imposta circuit breaker aperto
    llm._CIRCUIT["open_until"] = time.time() - 1  # Scaduto
    
    # Mock _raw_chat per simulare successo
    def success(sys_prompt, user_prompt):
        return "Success response"
    
    import sofia_lite.middleware.llm as llm_module
    llm_module._raw_chat = success
    
    # Esegui chiamata
    result = llm.chat("System prompt", "User message")
    
    # Verifica che il circuit breaker sia chiuso e funzioni
    assert result == "Success response"

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 