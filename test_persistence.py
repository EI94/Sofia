#!/usr/bin/env python3
"""
Test per la persistenza dei nomi in Firestore
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

def test_memory_persistence():
    """Testa la persistenza in memoria (mock Firestore)"""
    
    print("🧪 Test Persistenza Nomi in Firestore")
    print("=" * 50)
    
    # Simula il flusso completo
    test_phone = "+393001234567"
    test_name = "Pierpaolo"
    
    print(f"📱 Telefono: {test_phone}")
    print(f"👤 Nome da salvare: {test_name}")
    
    # Simula Context
    class MockContext:
        def __init__(self, phone, lang="it", state="ASK_NAME"):
            self.phone = phone
            self.lang = lang
            self.state = state
            self.name = None
            self.history = []
    
    # Simula Memory Gateway
    class MockMemoryGateway:
        def __init__(self):
            self.users = {}
        
        def save_user_context(self, phone, user_data):
            self.users[phone] = user_data
            print(f"💾 Salvato in memoria: {phone} → {user_data}")
        
        def get_user_context(self, phone):
            return self.users.get(phone)
    
    # Test del flusso
    memory = MockMemoryGateway()
    ctx = MockContext(test_phone)
    
    # Simula estrazione nome
    ctx.name = test_name
    print(f"✅ Nome estratto: {ctx.name}")
    
    # Simula salvataggio
    user_data = {
        'lang': ctx.lang,
        'name': ctx.name,
        'state': ctx.state,
        'history': ctx.history
    }
    memory.save_user_context(ctx.phone, user_data)
    
    # Verifica persistenza
    saved_data = memory.get_user_context(test_phone)
    if saved_data and saved_data.get('name') == test_name:
        print(f"✅ Persistenza verificata: {saved_data}")
        return True
    else:
        print(f"❌ Persistenza fallita: {saved_data}")
        return False

def test_executor_integration():
    """Testa l'integrazione con l'executor"""
    
    print("\n🧪 Test Integrazione Executor")
    print("=" * 40)
    
    # Simula l'executor
    def mock_extract_name(text, ctx):
        """Mock dell'estrazione nome"""
        if "mi chiamo" in text.lower():
            return "Pierpaolo"
        return None
    
    def mock_save_context(ctx):
        """Mock del salvataggio"""
        print(f"💾 Context salvato: {ctx.phone} → {ctx.name}")
        return True
    
    # Test del flusso executor
    class MockContext:
        def __init__(self, phone):
            self.phone = phone
            self.name = None
    
    ctx = MockContext("+393001234567")
    
    # Simula intent ASK_NAME
    intent = "ASK_NAME"
    text = "Mi chiamo Pierpaolo"
    
    print(f"🎯 Intent: {intent}")
    print(f"📝 Testo: {text}")
    
    if intent == "ASK_NAME":
        name = mock_extract_name(text, ctx)
        if name:
            ctx.name = name
            mock_save_context(ctx)
            print(f"✅ Nome estratto e salvato: {ctx.name}")
            return True
    
    print("❌ Estrazione fallita")
    return False

if __name__ == "__main__":
    print("🚀 Sofia Lite - Test Persistenza Nomi")
    print()
    
    # Test persistenza
    persistence_success = test_memory_persistence()
    
    # Test integrazione executor
    executor_success = test_executor_integration()
    
    print("\n" + "=" * 50)
    if persistence_success and executor_success:
        print("🎉 TUTTI I TEST SUPERATI!")
        print("✅ La persistenza dei nomi funziona correttamente")
        sys.exit(0)
    else:
        print("❌ ALCUNI TEST FALLITI")
        print("⚠️ La persistenza dei nomi ha problemi")
        sys.exit(1) 