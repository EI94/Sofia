"""
Sofia Lite - Guardrails Tests
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from sofia_lite.policy.guardrails import (
    is_abusive, is_threatening, is_spam, is_sexual_inappropriate, 
    is_inappropriate, abuse_reply, warning_reply, get_abuse_type
)
from sofia_lite.agents.executor import dispatch
from sofia_lite.agents.context import Context

def test_abusive_content_detection():
    """Test rilevamento contenuti abusivi"""
    
    test_cases = [
        # Italiano
        ("vaffa", True),
        ("porco dio", True),
        ("stronzo", True),
        ("cazzo", True),
        ("merda", True),
        
        # Inglese
        ("fuck you", True),
        ("shit", True),
        ("bitch", True),
        ("cunt", True),
        
        # Francese
        ("merde", True),
        ("putain", True),
        ("connard", True),
        
        # Spagnolo
        ("puta", True),
        ("coño", True),
        ("cabrón", True),
        
        # Test negativi
        ("ciao come stai?", False),
        ("hello how are you?", False),
        ("bonjour comment allez-vous?", False),
        ("hola como estas?", False),
        ("", False),
        ("   ", False),
    ]
    
    for text, expected in test_cases:
        result = is_abusive(text)
        assert result == expected, f"Failed for '{text}': expected {expected}, got {result}"

def test_threatening_content_detection():
    """Test rilevamento minacce e violenza"""
    
    test_cases = [
        ("ti ammazzo", True),
        ("kill you", True),
        ("te tue", True),
        ("te mato", True),
        ("violence", True),
        ("violenza", True),
        
        # Test negativi
        ("ciao come stai?", False),
        ("hello how are you?", False),
    ]
    
    for text, expected in test_cases:
        result = is_threatening(text)
        assert result == expected, f"Failed for '{text}': expected {expected}, got {result}"

def test_spam_content_detection():
    """Test rilevamento spam"""
    
    test_cases = [
        ("compra ora", True),
        ("buy now", True),
        ("achetez maintenant", True),
        ("comprar ahora", True),
        ("click here", True),
        ("clicca qui", True),
        ("www.example.com", True),
        ("http://example.com", True),
        ("prezzo speciale", True),
        
        # Test negativi
        ("ciao come stai?", False),
        ("hello how are you?", False),
    ]
    
    for text, expected in test_cases:
        result = is_spam(text)
        assert result == expected, f"Failed for '{text}': expected {expected}, got {result}"

def test_sexual_inappropriate_detection():
    """Test rilevamento contenuti sessuali inappropriati"""
    
    test_cases = [
        ("porno", True),
        ("porn", True),
        ("pornographie", True),
        ("pornografía", True),
        ("sexy", True),
        ("nudo", True),
        ("nude", True),
        ("sex", True),
        ("sesso", True),
        
        # Test negativi
        ("ciao come stai?", False),
        ("hello how are you?", False),
    ]
    
    for text, expected in test_cases:
        result = is_sexual_inappropriate(text)
        assert result == expected, f"Failed for '{text}': expected {expected}, got {result}"

def test_multilingual_abuse_replies():
    """Test risposte multilingue per abusi"""
    
    test_languages = ["it", "en", "fr", "es", "ar", "hi", "ur", "bn", "wo"]
    
    for lang in test_languages:
        abuse_msg = abuse_reply(lang)
        warning_msg = warning_reply(lang)
        
        # Verifica che i messaggi non siano vuoti
        assert len(abuse_msg) > 0, f"Empty abuse message for {lang}"
        assert len(warning_msg) > 0, f"Empty warning message for {lang}"
        
        # Verifica che i messaggi siano diversi
        assert abuse_msg != warning_msg, f"Same message for abuse and warning in {lang}"

def test_abuse_type_detection():
    """Test rilevamento tipo di abuso"""
    
    test_cases = [
        ("vaffa", "abusive"),
        ("ti ammazzo", "threatening"),
        ("compra ora", "spam"),
        ("porno", "sexual"),
        ("ciao come stai?", "none"),
    ]
    
    for text, expected in test_cases:
        result = get_abuse_type(text)
        assert result == expected, f"Failed for '{text}': expected {expected}, got {result}"

def test_executor_guardrails_integration():
    """Test integrazione guardrails con executor"""
    
    # Mock context
    ctx = Context(phone="+393001234567", lang="it", state="GREETING")
    ctx.slots = {}
    
    # Mock skill module
    class MockSkill:
        @staticmethod
        def run(ctx, text):
            return "Normal response"
    
    # Test primo abuso - dovrebbe dare warning
    result1 = dispatch("GREET", ctx, "vaffa")
    assert "Attenzione" in result1, f"Expected warning, got: {result1}"
    assert ctx.slots.get("abuse_count") == 1, f"Expected abuse_count=1, got: {ctx.slots.get('abuse_count')}"
    
    # Test secondo abuso - dovrebbe chiudere conversazione
    result2 = dispatch("GREET", ctx, "porco dio")
    assert "policy" in result2.lower(), f"Expected abuse close, got: {result2}"
    
    # Test messaggio normale - dovrebbe passare
    ctx.slots = {}  # Reset
    result3 = dispatch("GREET", ctx, "ciao")
    assert result3 == "Normal response", f"Expected normal response, got: {result3}"

def test_case_insensitive_detection():
    """Test che il rilevamento sia case-insensitive"""
    
    test_cases = [
        ("VAFFA", True),
        ("FUCK", True),
        ("MERDE", True),
        ("PUTA", True),
        ("Vaffa", True),
        ("Fuck", True),
    ]
    
    for text, expected in test_cases:
        result = is_abusive(text)
        assert result == expected, f"Failed for '{text}': expected {expected}, got {result}"

def test_edge_cases():
    """Test casi limite"""
    
    # Test testo vuoto
    assert not is_inappropriate(""), "Empty text should not be inappropriate"
    assert not is_inappropriate("   "), "Whitespace should not be inappropriate"
    
    # Test testo molto lungo
    long_text = "ciao " * 100 + "vaffa"
    assert is_inappropriate(long_text), "Long text with abuse should be inappropriate"
    
    # Test testo con caratteri speciali
    special_text = "v@ff@"
    assert not is_inappropriate(special_text), "Text with special chars should not be inappropriate"

if __name__ == "__main__":
    pytest.main([__file__]) 