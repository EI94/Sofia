#!/usr/bin/env python3
"""
Test locale per verificare il flusso di Sofia
"""

import sys
import os
sys.path.append('sofia_lite')

from sofia_lite.agents.context import Context
from sofia_lite.agents.orchestrator import Orchestrator
from sofia_lite.middleware.memory import save_context

def test_conversation():
    """Test una conversazione semplice"""
    
    # Crea un nuovo contesto
    ctx = Context(phone="+393521110999", lang="it", state="GREETING")
    
    # Salva il contesto
    save_context(ctx)
    
    # Crea l'orchestrator
    orchestrator = Orchestrator()
    
    # Test 1: "Ciao"
    print("=== TEST 1: 'Ciao' ===")
    response1 = orchestrator.process_message("+393521110999", "Ciao")
    print(f"Response: {response1['reply']}")
    print(f"Intent: {response1['intent']}")
    print(f"State: {response1['state']}")
    print()
    
    # Test 2: "Mi chiamo Mario"
    print("=== TEST 2: 'Mi chiamo Mario' ===")
    response2 = orchestrator.process_message("+393521110999", "Mi chiamo Mario")
    print(f"Response: {response2['reply']}")
    print(f"Intent: {response2['intent']}")
    print(f"State: {response2['state']}")
    print()
    
    # Test 3: "Voglio un permesso"
    print("=== TEST 3: 'Voglio un permesso' ===")
    response3 = orchestrator.process_message("+393521110999", "Voglio un permesso")
    print(f"Response: {response3['reply']}")
    print(f"Intent: {response3['intent']}")
    print(f"State: {response3['state']}")
    print()

if __name__ == "__main__":
    test_conversation() 