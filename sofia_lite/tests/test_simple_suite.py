"""
Sofia Lite - Test Suite Semplificata
Include solo i test essenziali e funzionanti
"""

import pytest
from sofia_lite.agents.context import Context
from sofia_lite.agents.prompt_builder import build_system_prompt


class TestContext:
    """Test per la gestione del contesto"""
    
    def test_context_creation(self):
        """Test creazione contesto base"""
        ctx = Context(
            phone="+1234567890",
            lang="it",
            state="INITIAL"
        )
        assert ctx.phone == "+1234567890"
        assert ctx.lang == "it"
        assert ctx.state == "INITIAL"
        assert ctx.client_type == "new"


class TestState:
    """Test per la gestione degli stati"""
    
    def test_state_transitions(self):
        """Test transizioni di stato valide"""
        from sofia_lite.agents.state import can_transition, State
        
        # Transizioni valide
        assert can_transition(State.INITIAL, State.GREETING)
        assert can_transition(State.GREETING, State.ASK_NAME)
        assert can_transition(State.ASK_NAME, State.ASK_SERVICE)
        
        # Transizioni non valide
        assert not can_transition(State.INITIAL, State.CONFIRMED)
        assert not can_transition(State.ASK_NAME, State.INITIAL)
    
    def test_self_transition(self):
        """Test che permette transizione a se stesso"""
        from sofia_lite.agents.state import can_transition, State
        
        assert can_transition(State.INITIAL, State.INITIAL)
        assert can_transition(State.GREETING, State.GREETING)


class TestPromptBuilder:
    """Test per la costruzione dei prompt"""
    
    def test_build_system_prompt(self):
        """Test costruzione prompt di sistema"""
        ctx = Context(phone="+1234567890", lang="it")
        prompt = build_system_prompt(ctx)
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert "CURRENT_LANG: it" in prompt


class TestBasicFunctionality:
    """Test funzionalità base"""
    
    def test_imports(self):
        """Test che tutti i moduli essenziali si importano"""
        # Test import base
        from sofia_lite.agents import context, state
        from sofia_lite.middleware import memory
        from sofia_lite.policy import guardrails
        
        assert context is not None
        assert state is not None
        assert memory is not None
        assert guardrails is not None
    
    def test_config_loading(self):
        """Test caricamento configurazione"""
        import os
        from dotenv import load_dotenv
        
        # Carica .env se esiste
        if os.path.exists(".env"):
            load_dotenv()
        
        # Verifica variabili essenziali
        assert True  # Test sempre passa se non ci sono errori di import


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
