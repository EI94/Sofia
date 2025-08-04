"""
Test for multilingual language detection and intent classification
"""

import pytest
from sofia_lite.middleware.language import heuristic_lang, detect_lang_with_heuristics
from sofia_lite.agents.planner import classify_intent
from sofia_lite.agents.context import Context

def test_heuristic_lang_detection():
    """Test heuristic language detection based on first word"""
    
    # Test Italian greetings
    assert heuristic_lang("Ciao Sofia") == "it"
    assert heuristic_lang("Salve") == "it"
    assert heuristic_lang("Buongiorno") == "it"
    
    # Test English greetings
    assert heuristic_lang("Hello there") == "en"
    assert heuristic_lang("Hi Sofia") == "en"
    assert heuristic_lang("Good morning") == "en"
    
    # Test French greetings
    assert heuristic_lang("Bonjour Sofia") == "fr"
    assert heuristic_lang("Salut") == "fr"
    assert heuristic_lang("Bonsoir") == "fr"
    
    # Test Spanish greetings
    assert heuristic_lang("Hola Sofia") == "es"
    assert heuristic_lang("Buenos días") == "es"
    assert heuristic_lang("Buenas tardes") == "es"
    
    # Test non-greeting text
    assert heuristic_lang("Mi chiamo Mario") is None
    assert heuristic_lang("What services do you offer?") is None

def test_lang_intent_classification():
    """Test intent classification with language detection"""
    
    # Create test context
    ctx = Context(phone="+1234567890", state="GREETING", name=None)
    
    # Test Italian greeting
    intent, confidence = classify_intent("Ciao", "it", ctx)
    assert intent == "GREET"
    assert confidence > 0.5
    
    # Test English greeting
    intent, confidence = classify_intent("Hello", "en", ctx)
    assert intent == "GREET"
    assert confidence > 0.5
    
    # Test French greeting
    intent, confidence = classify_intent("Bonjour", "fr", ctx)
    assert intent == "GREET"
    assert confidence > 0.5
    
    # Test Spanish greeting
    intent, confidence = classify_intent("Hola", "es", ctx)
    assert intent == "GREET"
    assert confidence > 0.5

def test_name_extraction_intent():
    """Test intent classification for name extraction"""
    
    ctx = Context(phone="+1234567890", state="GREETING", name=None)
    
    # Test Italian name
    intent, confidence = classify_intent("Mi chiamo Mario Rossi", "it", ctx)
    assert intent == "ASK_NAME"
    assert confidence > 0.5
    
    # Test English name
    intent, confidence = classify_intent("My name is John Smith", "en", ctx)
    assert intent == "ASK_NAME"
    assert confidence > 0.5
    
    # Test French name
    intent, confidence = classify_intent("Je m'appelle Pierre Dubois", "fr", ctx)
    assert intent == "ASK_NAME"
    assert confidence > 0.5
    
    # Test Spanish name
    intent, confidence = classify_intent("Me llamo Carlos García", "es", ctx)
    assert intent == "ASK_NAME"
    assert confidence > 0.5 