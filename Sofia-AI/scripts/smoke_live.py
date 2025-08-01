#!/usr/bin/env python3
import os
import sys
import traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from sofia_lite.agents.orchestrator import Orchestrator

def test_smoke_live():
    print("🚀 Sofia Lite - Live Smoke Test")
    orchestrator = Orchestrator()
    test_phone = "+393001234567"
    test_message = "ciao"
    try:
        result = orchestrator.process_message(test_phone, test_message)
        reply = result["reply"]
        state = result["state"]
        print(f"Risposta: {reply}")
        print(f"Stato: {state}")
        if state == "ASK_NAME":
            print("OK: Stato ASK_NAME raggiunto")
            return True
        else:
            print(f"FAIL: Stato inatteso {state}")
            return False
    except Exception as e:
        print(f"Errore: {e}")
        traceback.print_exc()
        return False

def main():
    success = test_smoke_live()
    if success:
        print("Smoke test SUPERATO!")
        sys.exit(0)
    else:
        print("Smoke test FALLITO!")
        sys.exit(1)

if __name__ == "__main__":
    main()
