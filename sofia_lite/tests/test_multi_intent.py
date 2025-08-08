"""
Sofia Lite - Multi-Intent Classification Tests
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from sofia_lite.agents.context import Context
from sofia_lite.agents.planner import classify_intents, next_state, plan
from sofia_lite.agents.state import State


def test_classify_intents_single():
    """Test classificazione intent singoli"""

    test_cases = [
        ("Ciao", ["GREET"]),
        ("Mi chiamo Pierpaolo", ["ASK_NAME"]),
        ("Ho bisogno del permesso di soggiorno", ["REQUEST_SERVICE"]),
        ("Quanto costa?", ["ASK_COST"]),
        ("Domani alle 15:00", ["ASK_SLOT"]),
        ("Come posso pagare?", ["ASK_PAYMENT"]),
        ("Sì, va bene", ["CONFIRM"]),
        ("Non capisco", ["CLARIFY"]),
    ]

    for text, expected in test_cases:
        result = classify_intents(text)
        assert (
            expected[0] in result
        ), f"Failed for '{text}': expected {expected[0]}, got {result}"


def test_classify_intents_multi():
    """Test classificazione multi-intent con priorità"""

    test_cases = [
        # "Ciao ho bisogno permesso" → first intent REQUEST_SERVICE
        ("Ciao ho bisogno del permesso di soggiorno", ["REQUEST_SERVICE", "GREET"]),
        (
            "Salve quanto costa la cittadinanza?",
            ["REQUEST_SERVICE", "ASK_COST", "GREET"],
        ),
        (
            "Mi chiamo Maria e vorrei sapere i costi",
            ["ASK_NAME", "ASK_COST", "REQUEST_SERVICE"],
        ),
        ("Ciao domani alle 15:00 va bene?", ["ASK_SLOT", "GREET", "CONFIRM"]),
        ("Ho bisogno di aiuto per il ricongiungimento familiare", ["REQUEST_SERVICE"]),
    ]

    for text, expected in test_cases:
        result = classify_intents(text)
        # Verifica che il primo intent sia quello con priorità più alta
        assert (
            result[0] == expected[0]
        ), f"Failed for '{text}': expected first intent {expected[0]}, got {result[0]}"

        # Verifica che tutti gli intent attesi siano presenti
        for intent in expected:
            assert (
                intent in result
            ), f"Failed for '{text}': expected {intent} in {result}"


def test_priority_order():
    """Test che l'ordine di priorità sia rispettato"""

    # Test con tutti gli intent possibili
    complex_text = "Ciao mi chiamo Pierpaolo, ho bisogno del permesso di soggiorno, quanto costa e domani alle 15:00 va bene?"

    result = classify_intents(complex_text)

    # Verifica che REQUEST_SERVICE sia il primo (priorità massima)
    assert (
        result[0] == "REQUEST_SERVICE"
    ), f"REQUEST_SERVICE should be first, got {result[0]}"

    # Verifica che GREET non sia il primo (priorità bassa)
    if "GREET" in result:
        greet_index = result.index("GREET")
        assert greet_index > 0, f"GREET should not be first, got index {greet_index}"


def test_next_state_mapping():
    """Test mapping intent → state"""

    test_cases = [
        (State.GREETING, "REQUEST_SERVICE", State.ASK_SERVICE),
        (State.GREETING, "ASK_COST", State.PROPOSE_CONSULT),
        (State.ASK_NAME, "REQUEST_SERVICE", State.ASK_SERVICE),
        (State.ASK_SERVICE, "ASK_COST", State.PROPOSE_CONSULT),
    ]

    for current_state, intent, expected_state in test_cases:
        result = next_state(current_state, intent)
        assert (
            result == expected_state
        ), f"Failed for {current_state} + {intent}: expected {expected_state}, got {result}"


def test_plan_with_multi_intent():
    """Test funzione plan con multi-intent"""

    # Mock context
    ctx = Context(phone="+393001234567", lang="it", state=State.GREETING)

    # Mock LLM (non verrà chiamato perché regex dovrebbe trovare l'intent)
    def mock_llm(*args, **kwargs):
        return '{"intent": "UNKNOWN", "reason": "fallback"}'

    # Test con multi-intent
    text = "Ciao ho bisogno del permesso di soggiorno"
    intent, reason = plan(ctx, text, mock_llm)

    # Dovrebbe trovare REQUEST_SERVICE tramite regex
    assert intent == "REQUEST_SERVICE", f"Expected REQUEST_SERVICE, got {intent}"
    assert (
        "Multi-intent detected" in reason
    ), f"Expected multi-intent reason, got {reason}"


def test_edge_cases():
    """Test casi limite"""

    # Test testo vuoto
    result = classify_intents("")
    assert result == [], f"Empty text should return empty list, got {result}"

    # Test testo senza intent riconosciuti
    result = classify_intents("xyz 123 !@#")
    assert result == [], f"Text without intents should return empty list, got {result}"

    # Test testo molto lungo
    long_text = "Ciao " * 100 + "ho bisogno del permesso di soggiorno"
    result = classify_intents(long_text)
    assert (
        "REQUEST_SERVICE" in result
    ), f"Long text should still detect REQUEST_SERVICE, got {result}"


def test_case_insensitive():
    """Test che la classificazione sia case-insensitive"""

    test_cases = [
        ("CIAO", ["GREET"]),
        ("Mi Chiamo", ["ASK_NAME"]),
        ("HO BISOGNO", ["REQUEST_SERVICE"]),
        ("QUANTO COSTA", ["ASK_COST"]),
    ]

    for text, expected in test_cases:
        result = classify_intents(text)
        assert (
            expected[0] in result
        ), f"Failed for '{text}': expected {expected[0]}, got {result}"


if __name__ == "__main__":
    pytest.main([__file__])
