import pytest
from unittest.mock import Mock, patch
from app.agents.context import Context
from app.agents.planner import plan
from app.agents.validator import validate
from app.agents.executor import dispatch

class MockLLM:
    def chat_completion(self, messages, model="gpt-4o-mini"):
        user_msg = messages[1]["content"] if len(messages) > 1 else ""
        
        if "ciao" in user_msg.lower() or "hello" in user_msg.lower():
            return '{"intent": "GREET", "reason": "greeting"}'
        elif "pierpaolo" in user_msg.lower():
            return '{"intent": "ASK_NAME", "reason": "name provided"}'
        elif "consulenza" in user_msg.lower():
            return '{"intent": "PROPOSE_CONSULT", "reason": "consultation"}'
        else:
            return '{"intent": "CLARIFY", "reason": "unclear"}'

def test_happy_path_new_user():
    """Test complete happy path for new user"""
    ctx = Context(phone="+1234567890")
    llm = MockLLM()
    
    # Step 1: Greeting → forced to ASK_NAME (smart name handling)
    intent, reason = plan(ctx, "Ciao!", llm)
    intent = validate(ctx, intent)
    reply = dispatch(intent, ctx, "Ciao!")
    
    assert intent == "ASK_NAME"  # Smart validator forces ASK_NAME
    assert "Piacere! Come ti chiami?" in reply
    assert ctx.state == "ASK_NAME"
    
    # Step 2: Name (extracted automatically)
    intent, reason = plan(ctx, "Mi chiamo Pierpaolo", llm)
    intent = validate(ctx, intent)
    reply = dispatch(intent, ctx, "Mi chiamo Pierpaolo")
    
    assert intent == "ASK_NAME"
    assert "servizio" in reply.lower()  # Goes directly to ask_service
    assert ctx.state == "ASK_SERVICE"  # Name extracted, state updated

def test_edge_case_abusive_language():
    """Test edge case with abusive language"""
    from app.policy.guardrails import is_abusive, close_message
    
    # Test abusive detection
    assert is_abusive("fuck you") == True
    assert is_abusive("merda") == True
    assert is_abusive("hello") == False
    
    # Test close message
    close_msg = close_message("it")
    assert "politica" in close_msg.lower()

def test_edge_case_invalid_state():
    """Test edge case with invalid state transition"""
    ctx = Context(phone="+1234567890", state="GREETING")
    llm = MockLLM()
    
    # Try invalid transition
    intent, reason = plan(ctx, "Random text", llm)
    intent = validate(ctx, intent)
    reply = dispatch(intent, ctx, "Random text")
    
    assert intent == "CLARIFY"
    assert "non ho capito" in reply.lower()

def test_edge_case_memory_persistence():
    """Test that context is properly updated"""
    ctx = Context(phone="+1234567890")
    llm = MockLLM()
    
    # Initial state
    assert ctx.state == "GREETING"
    assert ctx.intent is None
    
    # Process message
    intent, reason = plan(ctx, "Ciao!", llm)
    intent = validate(ctx, intent)
    reply = dispatch(intent, ctx, "Ciao!")
    
    # Check state was updated (smart name handling)
    assert ctx.state == "ASK_NAME"
    # Intent is not set by executor anymore
    # assert ctx.intent == "GREET"

def test_multilingual_support():
    """Test multilingual support"""
    languages = ["it", "en", "fr", "es"]
    
    for lang in languages:
        ctx = Context(phone="+1234567890", lang=lang)
        llm = MockLLM()
        
        # Test greeting in different languages
        intent, reason = plan(ctx, "Hello", llm)
        intent = validate(ctx, intent)
        reply = dispatch(intent, ctx, "Hello")
        
        # Should work in all languages (smart name handling)
        assert intent == "ASK_NAME"  # Smart validator forces ASK_NAME
        assert reply != "Message not found: greet_intro" 