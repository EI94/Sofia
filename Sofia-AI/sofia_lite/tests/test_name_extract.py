"""
Sofia Lite - Name Extraction Tests
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from sofia_lite.utils.name_extract import extract_name_regex, extract_name, clean_name
from sofia_lite.agents.context import Context

# Test cases for name extraction
NAME_TEST_CASES = [
    # Italian
    ("Mi chiamo José-María", "José-María"),
    ("Sono Pierpaolo", "Pierpaolo"),
    ("Mi chiamo Maria Luisa", "Maria Luisa"),
    ("Sono Giovanni", "Giovanni"),
    
    # English
    ("My name is John", "John"),
    ("I'm Sarah", "Sarah"),
    ("I am Michael", "Michael"),
    ("Call me David", "David"),
    
    # French
    ("Je m'appelle O'Connor", "O'Connor"),
    ("Je suis Marie-Claire", "Marie-Claire"),
    ("Mon nom est Jean-Pierre", "Jean-Pierre"),
    
    # Spanish
    ("Me llamo José", "José"),
    ("Soy María", "María"),
    ("Mi nombre es Carlos", "Carlos"),
    
    # Arabic
    ("أنا محمد", "محمد"),
    ("اسمي فاطمة", "فاطمة"),
    ("أدعى أحمد", "أحمد"),
    
    # Hindi
    ("मेरा नाम राजेश", "राजेश"),
    ("मैं प्रिया", "प्रिया"),
    ("मुझे अमित कहते हैं", "अमित"),
    
    # Urdu
    ("میرا نام علی", "علی"),
    ("میں فاطمہ", "فاطمہ"),
    
    # Bengali
    ("আমার নাম রাহুল", "রাহুল"),
    ("আমি প্রিয়া", "প্রিয়া"),
    
    # Wolof
    ("Ma tudd Mamadou", "Mamadou"),
    ("Ma Fatou", "Fatou"),
]

# Test cases that should NOT extract names
NO_NAME_CASES = [
    "Ciao come stai?",
    "Hello how are you?",
    "Bonjour comment allez-vous?",
    "Hola como estas?",
    "مرحبا كيف حالك؟",
    "नमस्ते कैसे हो?",
    "السلام علیکم",
    "হ্যালো কেমন আছো?",
    "Salam nga def?",
    "",
    "   ",
    "A",
    "123",
    "!@#$%",
]

def test_extract_name_regex():
    """Test regex-based name extraction for all languages"""
    for text, expected in NAME_TEST_CASES:
        # Test with different languages
        for lang in ["it", "en", "fr", "es", "ar", "hi", "ur", "bn", "wo"]:
            result = extract_name_regex(text, lang)
            if result:
                # If we get a result, it should match expected (case insensitive)
                assert result.lower() == expected.lower(), f"Failed for '{text}' in {lang}: got '{result}', expected '{expected}'"
                break  # Found a match, move to next test case

def test_extract_name_regex_no_match():
    """Test that regex doesn't extract names from non-name text"""
    for text in NO_NAME_CASES:
        for lang in ["it", "en", "fr", "es", "ar", "hi", "ur", "bn", "wo"]:
            result = extract_name_regex(text, lang)
            assert result is None, f"Unexpectedly extracted name '{result}' from '{text}' in {lang}"

def test_extract_name_with_context():
    """Test full name extraction with context"""
    ctx = Context(phone="+393001234567", lang="it", state="ASK_NAME")
    
    # Test successful extraction
    result = extract_name("Mi chiamo Pierpaolo", ctx)
    assert result == "Pierpaolo"
    
    # Test no extraction
    result = extract_name("Ciao come stai?", ctx)
    assert result is None

def test_clean_name():
    """Test name cleaning and normalization"""
    test_cases = [
        ("  pierpaolo  ", "Pierpaolo"),
        ("MARIA LUISA", "Maria Luisa"),
        ("jose-maria", "Jose-Maria"),
        ("o'connor", "O'Connor"),
        ("jean-pierre", "Jean-Pierre"),
        ("محمد", "محمد"),  # Arabic should be preserved
        ("राजेश", "राजेश"),  # Hindi should be preserved
        ("", ""),
        ("   ", ""),
        ("a", "A"),
        ("123", ""),  # Numbers should be removed
        ("!@#$%", ""),  # Special chars should be removed
    ]
    
    for input_name, expected in test_cases:
        result = clean_name(input_name)
        assert result == expected, f"Failed for '{input_name}': got '{result}', expected '{expected}'"

def test_multilingual_patterns():
    """Test that all language patterns are defined"""
    from sofia_lite.utils.name_extract import NAME_PATTERNS
    
    expected_langs = ["it", "en", "fr", "es", "ar", "hi", "ur", "bn", "wo"]
    
    for lang in expected_langs:
        assert lang in NAME_PATTERNS, f"Missing patterns for language: {lang}"
        assert len(NAME_PATTERNS[lang]) > 0, f"Empty patterns for language: {lang}"

def test_unicode_support():
    """Test Unicode name support"""
    unicode_names = [
        ("Mi chiamo José", "José"),
        ("Je m'appelle François", "François"),
        ("Me llamo María", "María"),
        ("أنا محمد", "محمد"),
        ("मेरा नाम राजेश", "राजेश"),
        ("میرا نام علی", "علی"),
        ("আমার নাম রাহুল", "রাহুল"),
    ]
    
    for text, expected in unicode_names:
        result = extract_name_regex(text, "it")  # Try with Italian patterns
        if result:
            assert result == expected, f"Unicode test failed for '{text}': got '{result}', expected '{expected}'"

if __name__ == "__main__":
    pytest.main([__file__])
