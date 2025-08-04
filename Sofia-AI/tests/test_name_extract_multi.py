"""
Test for multilingual name extraction
"""

import pytest
from sofia_lite.utils.name_extract import extract_name_regex, clean_name
from sofia_lite.agents.context import Context

def test_italian_name_extraction():
    """Test Italian name extraction patterns"""
    
    # Test "mi chiamo" pattern
    name = extract_name_regex("Mi chiamo Mario Rossi", "it")
    assert name == "Mario Rossi"
    
    # Test "sono" pattern
    name = extract_name_regex("Sono Mario", "it")
    assert name == "Mario"
    
    # Test "il mio nome è" pattern
    name = extract_name_regex("Il mio nome è Mario Rossi", "it")
    assert name == "Mario Rossi"
    
    # Test with special characters
    name = extract_name_regex("Mi chiamo Mario-Rossi", "it")
    assert name == "Mario-Rossi"

def test_english_name_extraction():
    """Test English name extraction patterns"""
    
    # Test "my name is" pattern
    name = extract_name_regex("My name is John Smith", "en")
    assert name == "John Smith"
    
    # Test "i am" pattern
    name = extract_name_regex("I am John", "en")
    assert name == "John"
    
    # Test "i'm" pattern
    name = extract_name_regex("I'm John Smith", "en")
    assert name == "John Smith"
    
    # Test "i'm called" pattern
    name = extract_name_regex("I'm called John", "en")
    assert name == "John"

def test_french_name_extraction():
    """Test French name extraction patterns"""
    
    # Test "je m'appelle" pattern
    name = extract_name_regex("Je m'appelle Pierre Dubois", "fr")
    assert name == "Pierre Dubois"
    
    # Test "je suis" pattern
    name = extract_name_regex("Je suis Pierre", "fr")
    assert name == "Pierre"
    
    # Test "mon nom est" pattern
    name = extract_name_regex("Mon nom est Pierre Dubois", "fr")
    assert name == "Pierre Dubois"
    
    # Test with accents
    name = extract_name_regex("Je m'appelle François", "fr")
    assert name == "François"

def test_spanish_name_extraction():
    """Test Spanish name extraction patterns"""
    
    # Test "me llamo" pattern
    name = extract_name_regex("Me llamo Carlos García", "es")
    assert name == "Carlos García"
    
    # Test "soy" pattern
    name = extract_name_regex("Soy Carlos", "es")
    assert name == "Carlos"
    
    # Test "mi nombre es" pattern
    name = extract_name_regex("Mi nombre es Carlos García", "es")
    assert name == "Carlos García"
    
    # Test with ñ
    name = extract_name_regex("Me llamo Peña", "es")
    assert name == "Peña"

def test_name_cleaning():
    """Test name cleaning and normalization"""
    
    # Test basic cleaning
    assert clean_name("  Mario   Rossi  ") == "Mario Rossi"
    
    # Test special characters
    assert clean_name("Mario-Rossi") == "Mario-Rossi"
    assert clean_name("Mario O'Connor") == "Mario O'Connor"
    
    # Test Unicode characters
    assert clean_name("François") == "François"
    assert clean_name("Carlos García") == "Carlos García"
    
    # Test removal of invalid characters
    assert clean_name("Mario 123 Rossi") == "Mario Rossi"
    assert clean_name("Mario@Rossi") == "Mario Rossi"

def test_no_name_extraction():
    """Test cases where no name should be extracted"""
    
    # Test non-name text
    assert extract_name_regex("Ciao, come stai?", "it") is None
    assert extract_name_regex("Hello, how are you?", "en") is None
    
    # Test incomplete patterns
    assert extract_name_regex("Mi chiamo", "it") is None
    assert extract_name_regex("My name is", "en") is None
    
    # Test wrong language
    assert extract_name_regex("Mi chiamo Mario", "en") is None
    assert extract_name_regex("My name is John", "it") is None 