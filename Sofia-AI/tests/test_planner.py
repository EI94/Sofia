import pytest
from unittest.mock import Mock, patch
from app.agents.planner import plan, INTENTS
from app.agents.context import Context

class MockLLM:
    def chat_completion(self, messages, model="gpt-4o-mini"):
        # Mock response based on user message
        user_msg = ""
        for msg in messages:
            if msg["role"] == "user":
                user_msg = msg["content"]
                break
        
        # Extract user message from the prompt
        if "User: \"" in user_msg:
            user_msg = user_msg.split("User: \"")[-1].split("\"")[0]
        

        
        if "ciao" in user_msg.lower():
            return '{"intent": "GREET", "reason": "greeting detected"}'
        elif "mi chiamo" in user_msg.lower() or "pierpaolo" in user_msg.lower():
            return '{"intent": "ASK_NAME", "reason": "name mentioned"}'
        elif "consulenza" in user_msg.lower() or "voglio una consulenza" in user_msg.lower():
            return '{"intent": "PROPOSE_CONSULT", "reason": "consultation requested"}'
        else:
            return '{"intent": "UNKNOWN", "reason": "no specific intent"}'

def test_planner_greeting():
    """Test planner with greeting intent"""
    ctx = Context(phone="+1234567890")
    llm = MockLLM()
    
    intent, reason = plan(ctx, "Ciao!", llm)
    
    assert intent == "GREET"
    assert "greeting" in reason.lower()

def test_planner_name_request():
    """Test planner with name intent"""
    ctx = Context(phone="+1234567890")
    llm = MockLLM()
    
    intent, reason = plan(ctx, "Mi chiamo Pierpaolo", llm)
    
    assert intent == "ASK_NAME"
    assert "name" in reason.lower()

def test_planner_consultation():
    """Test planner with consultation intent"""
    ctx = Context(phone="+1234567890")
    llm = MockLLM()
    
    intent, reason = plan(ctx, "Voglio una consulenza", llm)
    
    assert intent == "PROPOSE_CONSULT"
    assert "consultation" in reason.lower()

def test_planner_unknown():
    """Test planner with unknown intent"""
    ctx = Context(phone="+1234567890")
    llm = MockLLM()
    
    intent, reason = plan(ctx, "Random text", llm)
    
    assert intent == "UNKNOWN"
    assert "no specific" in reason.lower()

def test_planner_json_error():
    """Test planner with invalid JSON response"""
    ctx = Context(phone="+1234567890")
    
    class BadLLM:
        def chat_completion(self, messages, model="gpt-4o-mini"):
            return "invalid json"
    
    llm = BadLLM()
    
    intent, reason = plan(ctx, "Test", llm)
    
    assert intent == "UNKNOWN"
    assert "error" in reason.lower() 