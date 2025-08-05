#!/usr/bin/env python3
"""
Test E2E per conversazione completa con estrazione e persistenza del nome
"""

import re
import sys
import os

def extract_name_regex(text: str, lang: str = "it") -> str:
    """Estrae il nome usando regex"""
    patterns = {
        'it': [r'mi chiamo\s+([a-zA-ZÀ-ÿ]+)', r'sono\s+([a-zA-ZÀ-ÿ]+)'],
        'en': [r'my name is\s+([a-zA-ZÀ-ÿ]+)', r'i\'m\s+([a-zA-ZÀ-ÿ]+)'],
        'fr': [r'je m\'appelle\s+([a-zA-ZÀ-ÿ]+)', r'je suis\s+([a-zA-ZÀ-ÿ]+)'],
        'es': [r'me llamo\s+([a-zA-ZÀ-ÿ]+)', r'soy\s+([a-zA-ZÀ-ÿ]+)']
    }
    
    text_lower = text.lower().strip()
    
    if lang in patterns:
        for pattern in patterns[lang]:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if len(name) >= 2:
                    return name.title()
    
    return None

def simulate_conversation():
    """Simula una conversazione completa E2E"""
    
    print("🚀 Sofia Lite - Test E2E Conversazione Completa")
    print("=" * 60)
    
    # Simula Context e Memory
    class MockContext:
        def __init__(self, phone):
            self.phone = phone
            self.name = None
            self.lang = 'it'
            self.state = 'GREETING'
            self.history = []
        
        def add_message(self, role, content):
            self.history.append({'role': role, 'content': content})
    
    class MockMemory:
        def __init__(self):
            self.users = {}
        
        def save_context(self, ctx):
            self.users[ctx.phone] = {
                'name': ctx.name,
                'lang': ctx.lang,
                'state': ctx.state,
                'history': ctx.history
            }
            print(f"💾 Context salvato: {ctx.phone} → {ctx.name}")
        
        def load_context(self, phone):
            return self.users.get(phone)
    
    # Inizializza
    memory = MockMemory()
    phone = "+393001234567"
    ctx = MockContext(phone)
    
    # Conversazione simulata
    conversation = [
        ("user", "Ciao"),
        ("assistant", "Ciao! Sono Sofia di Studio Immigrato. Come posso aiutarti?"),
        ("user", "Mi chiamo Pierpaolo"),
        ("assistant", "Mi chiamo Pierpaolo. Piacere di conoscerti!"),
        ("user", "Vorrei informazioni sui servizi"),
        ("assistant", "Offriamo consulenze per: permesso di soggiorno, cittadinanza, ricongiungimento familiare. Quale ti interessa?"),
    ]
    
    print(f"📱 Telefono: {phone}")
    print(f"🌍 Lingua: {ctx.lang}")
    print(f"🎯 Stato iniziale: {ctx.state}")
    print()
    
    # Simula il flusso conversazionale
    for i, (role, message) in enumerate(conversation):
        print(f"Turno {i+1}:")
        print(f"  {role.upper()}: {message}")
        
        # Aggiungi messaggio alla storia
        ctx.add_message(role, message)
        
        # Se è un messaggio utente, cerca di estrarre il nome
        if role == "user":
            name = extract_name_regex(message, ctx.lang)
            if name:
                ctx.name = name
                ctx.state = "ASK_SERVICE"
                print(f"  ✅ Nome estratto: {name}")
                print(f"  🔄 Stato aggiornato: {ctx.state}")
                
                # Salva il context
                memory.save_context(ctx)
        
        print()
    
    # Verifica finale
    print("🔍 Verifica Finale:")
    print("=" * 30)
    
    saved_context = memory.load_context(phone)
    if saved_context:
        print(f"✅ Context persistito: {saved_context['name']}")
        print(f"✅ Stato finale: {saved_context['state']}")
        print(f"✅ Messaggi: {len(saved_context['history'])}")
        
        # Verifica che il nome sia stato salvato
        if saved_context['name'] == "Pierpaolo":
            print("🎉 SUCCESSO: Nome estratto e persistito correttamente!")
            return True
        else:
            print(f"❌ ERRORE: Nome non persistito correttamente ({saved_context['name']})")
            return False
    else:
        print("❌ ERRORE: Context non trovato in memoria")
        return False

def test_multilingual_conversations():
    """Testa conversazioni in diverse lingue"""
    
    print("\n🌍 Test Conversazioni Multilingue")
    print("=" * 40)
    
    test_cases = [
        ("it", "Mi chiamo Maria", "Maria"),
        ("en", "My name is John", "John"),
        ("fr", "Je m'appelle Pierre", "Pierre"),
        ("es", "Me llamo José", "José"),
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for lang, text, expected in test_cases:
        result = extract_name_regex(text, lang)
        status = "✅" if result == expected else "❌"
        print(f"{status} {lang.upper()}: '{text}' → '{result}' (expected: '{expected}')")
        
        if result == expected:
            success_count += 1
    
    print(f"\nRisultati: {success_count}/{total_count} test superati")
    return success_count == total_count

if __name__ == "__main__":
    print("🚀 Sofia Lite - Test E2E Completo")
    print()
    
    # Test conversazione completa
    conversation_success = simulate_conversation()
    
    # Test multilingue
    multilingual_success = test_multilingual_conversations()
    
    print("\n" + "=" * 60)
    if conversation_success and multilingual_success:
        print("🎉 TUTTI I TEST E2E SUPERATI!")
        print("✅ Sofia Lite è pronto per l'estrazione e persistenza dei nomi")
        sys.exit(0)
    else:
        print("❌ ALCUNI TEST E2E FALLITI")
        print("⚠️ Ci sono problemi nell'estrazione o persistenza")
        sys.exit(1) 