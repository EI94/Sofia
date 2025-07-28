import pytest
from app.agents.context import Context
from app.skills import greet_user, ask_name, ask_service, propose_consult, clarify

def test_greet_user_skill():
    """Test greet_user skill"""
    ctx = Context(phone="+1234567890", lang="it")
    
    result = greet_user.run(ctx, "Ciao!")
    
    assert "Ciao! Sono Sofia" in result
    assert "Studio Immigrato" in result

def test_ask_name_skill():
    """Test ask_name skill"""
    ctx = Context(phone="+1234567890", lang="it")
    
    result = ask_name.run(ctx, "Ciao come stai")
    
    assert "Piacere! Come ti chiami?" in result
    assert "Come ti chiami" in result
    
    # Test with name extraction
    ctx2 = Context(phone="+1234567890", lang="it")
    result2 = ask_name.run(ctx2, "Mario")
    assert "servizio" in result2.lower()  # Should go to ask_service
    
    # Test with existing name
    ctx3 = Context(phone="+1234567890", lang="it", name="Giovanni")
    result3 = ask_name.run(ctx3, "Test")
    assert "servizio" in result3.lower()  # Should skip to ask_service

def test_ask_service_skill():
    """Test ask_service skill"""
    ctx = Context(phone="+1234567890", lang="it")
    
    result = ask_service.run(ctx, "Test")
    
    assert "servizio" in result.lower()
    assert "immigrazione" in result.lower()

def test_propose_consult_skill():
    """Test propose_consult skill"""
    ctx = Context(phone="+1234567890", lang="it")
    
    result = propose_consult.run(ctx, "Test")
    
    assert "consulenza" in result.lower()
    # Now returns ask_channel message, not propose_consult
    assert "slot" in result.lower()

def test_clarify_skill():
    """Test clarify skill"""
    ctx = Context(phone="+1234567890", lang="it")
    
    result = clarify.run(ctx, "Test")
    
    assert "non ho capito" in result.lower()
    assert "ripetere" in result.lower()

def test_skills_multilingual():
    """Test skills in different languages"""
    languages = ["en", "fr", "es"]
    
    for lang in languages:
        ctx = Context(phone="+1234567890", lang=lang)
        
        # Test that skills return appropriate language
        result = greet_user.run(ctx, "Test")
        assert result != "Message not found: greet_intro"
        
        result = ask_name.run(ctx, "Test")
        assert result != "Message not found: ask_name" 