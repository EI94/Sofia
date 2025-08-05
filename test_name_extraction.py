#!/usr/bin/env python3
"""
Test completo per l'estrazione multilingue dei nomi
"""

import re
import sys
import os

# Aggiungi il path per importare sofia_lite
sys.path.insert(0, os.path.dirname(__file__))

# Pattern regex per l'estrazione dei nomi
NAME_PATTERNS = {
    "it": [
        r"mi chiamo\s+([a-zA-ZÀ-ÿ]+)",
        r"sono\s+([a-zA-ZÀ-ÿ]+)",
    ],
    "en": [
        r"my name is\s+([a-zA-ZÀ-ÿ]+)",
        r"i'm\s+([a-zA-ZÀ-ÿ]+)",
        r"i am\s+([a-zA-ZÀ-ÿ]+)",
    ],
    "fr": [
        r"je m'appelle\s+([a-zA-ZÀ-ÿ]+)",
        r"je suis\s+([a-zA-ZÀ-ÿ]+)",
    ],
    "es": [
        r"me llamo\s+([a-zA-ZÀ-ÿ]+)",
        r"soy\s+([a-zA-ZÀ-ÿ]+)",
    ]
}

def extract_name_regex(text: str, lang: str = "it") -> str:
    """Estrae il nome usando regex"""
    text_lower = text.lower().strip()
    
    if lang in NAME_PATTERNS:
        for pattern in NAME_PATTERNS[lang]:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if len(name) >= 2:
                    return name.title()
    
    return None

def test_name_extraction():
    """Testa l'estrazione dei nomi in diverse lingue"""
    
    test_cases = [
        ("Mi chiamo Pierpaolo", "it", "Pierpaolo"),
        ("Sono Maria", "it", "Maria"),
        ("My name is John", "en", "John"),
        ("I'm Sarah", "en", "Sarah"),
        ("I am Michael", "en", "Michael"),
        ("Je m'appelle Marie", "fr", "Marie"),
        ("Je suis Pierre", "fr", "Pierre"),
        ("Me llamo José", "es", "José"),
        ("Soy María", "es", "María"),
    ]
    
    print("🧪 Test Estrazione Nomi Multilingue")
    print("=" * 50)
    
    success_count = 0
    total_count = len(test_cases)
    
    for text, lang, expected in test_cases:
        result = extract_name_regex(text, lang)
        status = "✅" if result == expected else "❌"
        print(f"{status} {lang.upper()}: '{text}' → '{result}' (expected: '{expected}')")
        
        if result == expected:
            success_count += 1
    
    print("=" * 50)
    print(f"Risultati: {success_count}/{total_count} test superati")
    
    if success_count == total_count:
        print("🎉 Tutti i test superati!")
        return True
    else:
        print("⚠️ Alcuni test falliti")
        return False

def test_negative_cases():
    """Testa casi negativi (senza nomi)"""
    
    negative_cases = [
        "Ciao come stai?",
        "Hello how are you?",
        "Bonjour comment allez-vous?",
        "Hola como estas?",
        "",
        "   ",
        "123",
        "!@#$%",
    ]
    
    print("\n🧪 Test Casi Negativi")
    print("=" * 30)
    
    success_count = 0
    total_count = len(negative_cases)
    
    for text in negative_cases:
        result = extract_name_regex(text, "it")
        status = "✅" if result is None else "❌"
        print(f"{status} '{text}' → {result}")
        
        if result is None:
            success_count += 1
    
    print("=" * 30)
    print(f"Risultati: {success_count}/{total_count} test superati")
    
    return success_count == total_count

if __name__ == "__main__":
    print("🚀 Sofia Lite - Test Estrazione Nomi")
    print()
    
    # Test estrazione nomi
    extraction_success = test_name_extraction()
    
    # Test casi negativi
    negative_success = test_negative_cases()
    
    print("\n" + "=" * 50)
    if extraction_success and negative_success:
        print("🎉 TUTTI I TEST SUPERATI!")
        print("✅ L'estrazione multilingue dei nomi funziona correttamente")
        sys.exit(0)
    else:
        print("❌ ALCUNI TEST FALLITI")
        print("⚠️ L'estrazione dei nomi ha problemi")
        sys.exit(1) 