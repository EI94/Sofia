"""
Sofia Lite - Orchestrator Unit Tests
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from sofia_lite.agents.orchestrator import Orchestrator
from sofia_lite.agents.context import Context
from sofia_lite.middleware.llm import classify
from sofia_lite.skills import dispatch

class TestOrchestrator:
    """Test suite for Orchestrator class"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.orchestrator = Orchestrator()
        self.test_phone = "+393001234567"
        self.test_ctx = Context(
            phone=self.test_phone,
            lang="it",
            state="GREETING",
            name="Test User"
        )
    
    @pytest.mark.e2e
    def test_process_message_new_user(self):
        """Test processing message for new user"""
        with patch('sofia_lite.middleware.memory.load_context', return_value=None), \
             patch('sofia_lite.middleware.memory.save_context') as mock_save, \
             patch('sofia_lite.middleware.language.detect', return_value="it"), \
             patch('sofia_lite.agents.prompt_builder.build_system_prompt', return_value="Test prompt"), \
             patch('sofia_lite.agents.planner.plan', return_value="GREET"), \
             patch('sofia_lite.agents.validator.validate', return_value=True), \
             patch('sofia_lite.agents.executor.dispatch', return_value="Ciao! Sono Sofia"):
            
            result = self.orchestrator.process_message(self.test_phone, "ciao")
            
            assert result["reply"] == "Ciao! Sono Sofia"
            assert result["intent"] == "GREET"
            assert result["phone"] == self.test_phone
            assert result["lang"] == "it"
            mock_save.assert_called_once()
    
    @pytest.mark.e2e
    def test_process_message_existing_user(self):
        """Test processing message for existing user"""
        with patch('sofia_lite.middleware.memory.load_context', return_value=self.test_ctx), \
             patch('sofia_lite.middleware.memory.save_context') as mock_save, \
             patch('sofia_lite.agents.prompt_builder.build_system_prompt', return_value="Test prompt"), \
             patch('sofia_lite.agents.planner.plan', return_value="ASK_NAME"), \
             patch('sofia_lite.agents.validator.validate', return_value=True), \
             patch('sofia_lite.agents.executor.dispatch', return_value="Come ti chiami?"):
            
            result = self.orchestrator.process_message(self.test_phone, "non ho capito")
            
            assert result["reply"] == "Come ti chiami?"
            assert result["intent"] == "ASK_NAME"
            assert result["state"] == "GREETING"  # Original state preserved
            mock_save.assert_called_once()
    
    @pytest.mark.e2e
    def test_process_message_invalid_intent(self):
        """Test processing message with invalid intent"""
        with patch('sofia_lite.middleware.memory.load_context', return_value=self.test_ctx), \
             patch('sofia_lite.middleware.memory.save_context') as mock_save, \
             patch('sofia_lite.agents.prompt_builder.build_system_prompt', return_value="Test prompt"), \
             patch('sofia_lite.agents.planner.plan', return_value="INVALID_INTENT"), \
             patch('sofia_lite.agents.validator.validate', return_value=False), \
             patch('sofia_lite.agents.executor.dispatch', return_value="Mi dispiace, puoi ripetere?"):
            
            result = self.orchestrator.process_message(self.test_phone, "messaggio strano")
            
            assert result["reply"] == "Mi dispiace, puoi ripetere?"
            assert result["intent"] == "clarify"  # Fallback to clarify
            mock_save.assert_called_once()
    
    @pytest.mark.e2e
    def test_process_voice(self):
        """Test processing voice transcript"""
        with patch.object(self.orchestrator, 'process_message') as mock_process:
            mock_process.return_value = {
                "reply": "Ciao! Come posso aiutarti?",
                "intent": "GREET",
                "state": "GREETING",
                "lang": "it"
            }
            
            result = self.orchestrator.process_voice(self.test_phone, "ciao")
            
            assert "twiml" in result
            assert "Polly.Bianca" in result["twiml"]
            assert result["reply"] == "Ciao! Come posso aiutarti?"
            mock_process.assert_called_once_with(self.test_phone, "ciao", "voice")
    
    def test_orchestrator_initialization(self):
        """Test orchestrator component initialization"""
        assert self.orchestrator is not None
    
    @pytest.mark.e2e
    def test_context_history_update(self):
        """Test that context history is updated correctly"""
        with patch('sofia_lite.middleware.memory.load_context', return_value=self.test_ctx), \
             patch('sofia_lite.middleware.memory.save_context') as mock_save, \
             patch('sofia_lite.agents.prompt_builder.build_system_prompt', return_value="Test prompt"), \
             patch('sofia_lite.agents.planner.plan', return_value="GREET"), \
             patch('sofia_lite.agents.validator.validate', return_value=True), \
             patch('sofia_lite.agents.executor.dispatch', return_value="Ciao!"):
            
            self.orchestrator.process_message(self.test_phone, "ciao")
            
            # Check that history was updated
            saved_ctx = mock_save.call_args[0][0]
            assert len(saved_ctx.history) == 2
            assert saved_ctx.history[0]["role"] == "user"
            assert saved_ctx.history[0]["content"] == "ciao"
            assert saved_ctx.history[1]["role"] == "assistant"
            assert saved_ctx.history[1]["content"] == "Ciao!"

if __name__ == "__main__":
    pytest.main([__file__]) 