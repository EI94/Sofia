"""
Test di integrità dello State Machine - 100 transizioni casuali
Verifica che tutte le transizioni siano valide e consistenti
"""

import pytest
import random
from app.agents.validator import validate, VALID_TRANSITIONS, ALLOWED_SECONDARY_TRANSITIONS
from app.agents.context import Context
from app.policy.language_support import T


@pytest.mark.internal
class TestStateIntegrity:
    """Test suite per l'integrità dello state machine (INTERNAL ONLY)"""
    
    def setup_method(self):
        """Setup per ogni test"""
        self.all_intents = list(VALID_TRANSITIONS.keys())
        self.all_states = list(VALID_TRANSITIONS.keys()) + ["GREETING"]
        
    def test_random_transitions_100(self):
        """Test 100 transizioni casuali per verificare integrità"""
        print("\n🧪 Testando 100 transizioni casuali dello state machine...")
        
        ctx = Context(phone="+1234567890")
        ctx.state = "GREETING"
        
        valid_transitions = 0
        invalid_transitions = 0
        errors = []
        
        for i in range(100):
            # Genera intent casuale
            intent = random.choice(self.all_intents)
            
            # Testa transizione
            try:
                result = validate([intent], ctx)
                if result:
                    valid_transitions += 1
                    print(f"✅ Transizione {i+1}: {ctx.state} → {intent} (valida)")
                else:
                    invalid_transitions += 1
                    print(f"❌ Transizione {i+1}: {ctx.state} → {intent} (invalida)")
            except Exception as e:
                errors.append(f"Errore transizione {i+1}: {ctx.state} → {intent}: {str(e)}")
                print(f"💥 Errore transizione {i+1}: {ctx.state} → {intent}: {str(e)}")
        
        print(f"\n📊 Risultati:")
        print(f"   Transizioni valide: {valid_transitions}/100")
        print(f"   Transizioni invalide: {invalid_transitions}/100")
        print(f"   Errori: {len(errors)}")
        
        # Verifica che non ci siano errori
        assert len(errors) == 0, f"Errori nelle transizioni: {errors}"
        
        # Verifica che almeno il 70% delle transizioni siano valide
        success_rate = valid_transitions / 100
        assert success_rate >= 0.7, f"Tasso di successo troppo basso: {success_rate:.2%}"
        
        print(f"✅ Test completato: {success_rate:.1%} transizioni valide")
    
    def test_state_consistency(self):
        """Testa la consistenza degli stati dopo le transizioni"""
        print("\n🧪 Testando consistenza degli stati...")
        
        ctx = Context(phone="+1234567890")
        ctx.state = "GREETING"
        
        # Testa alcune transizioni specifiche
        test_cases = [
            ("GREETING", "NAME", "NAME"),
            ("NAME", "SERVICE", "SERVICE"),
            ("SERVICE", "PRICE", "PRICE"),
            ("PRICE", "BOOKING", "BOOKING"),
            ("BOOKING", "SLOT_SELECT", "SLOT_SELECT"),
            ("SLOT_SELECT", "PAYMENT", "PAYMENT"),
            ("PAYMENT", "CONFIRM", "CONFIRM"),
            ("CONFIRM", "RESET", "GREETING"),  # RESET torna a GREETING
        ]
        
        for initial_state, intent, expected_state in test_cases:
            ctx.state = initial_state
            result = validate([intent], ctx)
            
            if result:
                assert ctx.state == expected_state, f"Stato atteso {expected_state}, got {ctx.state}"
                print(f"✅ {initial_state} → {intent} → {ctx.state}")
            else:
                print(f"⚠️  Transizione non valida: {initial_state} → {intent}")
    
    def test_secondary_intents(self):
        """Testa le transizioni con intent secondari"""
        print("\n🧪 Testando intent secondari...")
        
        ctx = Context(phone="+1234567890")
        ctx.state = "GREETING"
        
        # Testa combinazioni di intent primari e secondari
        test_combinations = [
            (["GREETING", "NAME"], True),
            (["SERVICE", "PRICE"], True),
            (["BOOKING", "SLOT_SELECT"], True),
            (["PAYMENT", "CONFIRM"], True),
            (["GREETING", "ABUSE"], False),  # ABUSE non dovrebbe essere secondario
        ]
        
        for intents, should_be_valid in test_combinations:
            result = validate(intents, ctx)
            if should_be_valid:
                assert result, f"Transizione dovrebbe essere valida: {intents}"
                print(f"✅ Transizione valida: {intents}")
            else:
                assert not result, f"Transizione dovrebbe essere invalida: {intents}"
                print(f"✅ Transizione correttamente invalida: {intents}")
    
    def test_edge_cases(self):
        """Testa casi limite dello state machine"""
        print("\n🧪 Testando casi limite...")
        
        ctx = Context(phone="+1234567890")
        
        # Test 1: Stato vuoto
        ctx.state = ""
        result = validate(["GREETING"], ctx)
        assert result, "Transizione da stato vuoto dovrebbe essere valida"
        assert ctx.state == "GREETING"
        print("✅ Transizione da stato vuoto OK")
        
        # Test 2: Intent vuoto
        ctx.state = "GREETING"
        result = validate([], ctx)
        assert not result, "Intent vuoto dovrebbe essere invalido"
        print("✅ Intent vuoto correttamente invalido")
        
        # Test 3: Intent sconosciuto
        result = validate(["UNKNOWN_INTENT"], ctx)
        assert not result, "Intent sconosciuto dovrebbe essere invalido"
        print("✅ Intent sconosciuto correttamente invalido")
        
        # Test 4: Transizione da CLARIFY
        ctx.state = "CLARIFY"
        result = validate(["GREETING"], ctx)
        assert result, "Transizione da CLARIFY dovrebbe essere valida"
        print("✅ Transizione da CLARIFY OK")
    
    def test_memory_integrity(self):
        """Testa che il context non si corrompa durante le transizioni"""
        print("\n🧪 Testando integrità della memoria...")
        
        ctx = Context(phone="+1234567890", name="Test User")
        ctx.state = "GREETING"
        
        original_phone = ctx.phone
        original_name = ctx.name
        
        # Esegui molte transizioni
        for i in range(50):
            intent = random.choice(self.all_intents)
            validate([intent], ctx)
            
            # Verifica che i dati base non siano stati corrotti
            assert ctx.phone == original_phone, f"Phone corrotto dopo transizione {i}"
            assert ctx.name == original_name, f"Name corrotto dopo transizione {i}"
            assert ctx.state in self.all_states, f"Stato invalido dopo transizione {i}: {ctx.state}"
        
        print("✅ Integrità memoria preservata dopo 50 transizioni")
    
    def test_concurrent_transitions(self):
        """Testa transizioni multiple simultanee"""
        print("\n🧪 Testando transizioni multiple...")
        
        ctx = Context(phone="+1234567890")
        ctx.state = "GREETING"
        
        # Testa transizioni multiple valide
        multi_intents = ["GREETING", "NAME", "SERVICE"]
        result = validate(multi_intents, ctx)
        assert result, "Transizioni multiple dovrebbero essere valide"
        print(f"✅ Transizioni multiple valide: {multi_intents} → {ctx.state}")
        
        # Testa transizioni multiple con intent invalido
        invalid_multi = ["GREETING", "INVALID_INTENT", "SERVICE"]
        result = validate(invalid_multi, ctx)
        assert not result, "Transizioni con intent invalido dovrebbero fallire"
        print("✅ Transizioni con intent invalido correttamente rifiutate")


if __name__ == "__main__":
    # Esegui i test
    test_instance = TestStateIntegrity()
    test_instance.setup_method()
    
    print("🚀 Avvio test di integrità dello state machine...")
    
    test_instance.test_random_transitions_100()
    test_instance.test_state_consistency()
    test_instance.test_secondary_intents()
    test_instance.test_edge_cases()
    test_instance.test_memory_integrity()
    test_instance.test_concurrent_transitions()
    
    print("🏁 Tutti i test di integrità completati con successo!")