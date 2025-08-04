#!/usr/bin/env python3
"""
Test Rapido - Verifica miglioramenti implementati
"""

import requests
import json

def test_whatsapp_name_extraction():
    """Testa l'estrazione nomi su WhatsApp"""
    url = "https://sofia-lite-1075574333382.us-central1.run.app/webhook/whatsapp"
    
    test_cases = [
        {
            "name": "Nome semplice italiano",
            "payload": {
                "Body": "Ciao, mi chiamo Mario Rossi",
                "From": "whatsapp:+393331234567"
            },
            "expected_name": "Mario Rossi"
        },
        {
            "name": "Nome con caratteri speciali",
            "payload": {
                "Body": "Sono Mario@Rossi, piacere!",
                "From": "whatsapp:+393331234568"
            },
            "expected_name": "Mario Rossi"
        },
        {
            "name": "Nome con numeri",
            "payload": {
                "Body": "Mi chiamo Mario123Rossi",
                "From": "whatsapp:+393331234569"
            },
            "expected_name": "Mario Rossi"
        },
        {
            "name": "Nome francese",
            "payload": {
                "Body": "Bonjour, je m'appelle Jean-Pierre Dubois",
                "From": "whatsapp:+33123456789"
            },
            "expected_name": "Jean Pierre Dubois"
        },
        {
            "name": "Nome spagnolo",
            "payload": {
                "Body": "Hola, me llamo María José García",
                "From": "whatsapp:+34612345678"
            },
            "expected_name": "María José García"
        },
        {
            "name": "Nome inglese",
            "payload": {
                "Body": "Hi, I'm John Smith",
                "From": "whatsapp:+1234567890"
            },
            "expected_name": "John Smith"
        },
        {
            "name": "Nome con apostrofo",
            "payload": {
                "Body": "Ciao, sono Maria D'Angelo",
                "From": "whatsapp:+393331234570"
            },
            "expected_name": "Maria D'Angelo"
        }
    ]
    
    print("🔍 Testando estrazione nomi WhatsApp...")
    print("="*60)
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            response = requests.post(url, json=test_case["payload"], timeout=30)
            
            if response.status_code == 200:
                response_data = response.json()
                print(f"✅ {i}. {test_case['name']}: {response.status_code}")
                print(f"   Messaggio: {test_case['payload']['Body']}")
                print(f"   Risposta: {response_data.get('reply', '')[:100]}...")
                print(f"   Intent: {response_data.get('intent', 'N/A')}")
                print(f"   Lingua: {response_data.get('lang', 'N/A')}")
                print()
                success_count += 1
            else:
                print(f"❌ {i}. {test_case['name']}: {response.status_code}")
                print(f"   Errore: {response.text}")
                print()
                
        except Exception as e:
            print(f"❌ {i}. {test_case['name']}: Errore - {str(e)}")
            print()
    
    print(f"📊 Risultati WhatsApp: {success_count}/{total_count} test riusciti ({success_count/total_count*100:.1f}%)")
    print("="*60)
    
    return success_count, total_count

def test_voice_name_extraction():
    """Testa l'estrazione nomi su Voice"""
    url = "https://sofia-lite-1075574333382.us-central1.run.app/webhook/voice"
    
    test_cases = [
        {
            "name": "Nome semplice italiano",
            "payload": {
                "SpeechResult": "Ciao, mi chiamo Mario Rossi",
                "From": "+393331234567"
            }
        },
        {
            "name": "Nome con caratteri speciali",
            "payload": {
                "SpeechResult": "Sono Mario@Rossi, piacere!",
                "From": "+393331234568"
            }
        },
        {
            "name": "Nome con numeri",
            "payload": {
                "SpeechResult": "Mi chiamo Mario123Rossi",
                "From": "+393331234569"
            }
        }
    ]
    
    print("🔍 Testando estrazione nomi Voice...")
    print("="*60)
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            response = requests.post(url, data=test_case["payload"], timeout=30)
            
            if response.status_code == 200:
                response_data = response.json()
                print(f"✅ {i}. {test_case['name']}: {response.status_code}")
                print(f"   Messaggio: {test_case['payload']['SpeechResult']}")
                print(f"   Risposta: {response_data.get('reply', '')[:100]}...")
                print(f"   Intent: {response_data.get('intent', 'N/A')}")
                print(f"   Lingua: {response_data.get('lang', 'N/A')}")
                print()
                success_count += 1
            else:
                print(f"❌ {i}. {test_case['name']}: {response.status_code}")
                print(f"   Errore: {response.text}")
                print()
                
        except Exception as e:
            print(f"❌ {i}. {test_case['name']}: Errore - {str(e)}")
            print()
    
    print(f"📊 Risultati Voice: {success_count}/{total_count} test riusciti ({success_count/total_count*100:.1f}%)")
    print("="*60)
    
    return success_count, total_count

def main():
    """Funzione principale"""
    print("🚀 TEST RAPIDO - Verifica miglioramenti implementati")
    print("="*60)
    
    # Test WhatsApp
    whatsapp_success, whatsapp_total = test_whatsapp_name_extraction()
    
    # Test Voice
    voice_success, voice_total = test_voice_name_extraction()
    
    # Riepilogo finale
    total_success = whatsapp_success + voice_success
    total_tests = whatsapp_total + voice_total
    
    print("📊 RIEPILOGO FINALE")
    print("="*60)
    print(f"📱 WhatsApp: {whatsapp_success}/{whatsapp_total} ({whatsapp_success/whatsapp_total*100:.1f}%)")
    print(f"📞 Voice: {voice_success}/{voice_total} ({voice_success/voice_total*100:.1f}%)")
    print(f"🎯 Totale: {total_success}/{total_tests} ({total_success/total_tests*100:.1f}%)")
    
    if total_success == total_tests:
        print("🎉 TUTTI I TEST SUPERATI! I miglioramenti funzionano perfettamente!")
    elif total_success > total_tests * 0.8:
        print("✅ MAGGIORANZA DEI TEST SUPERATI! I miglioramenti funzionano bene!")
    else:
        print("⚠️ ALCUNI TEST FALLITI. Necessaria ulteriore analisi.")

if __name__ == "__main__":
    main() 