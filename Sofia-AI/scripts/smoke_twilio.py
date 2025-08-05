#!/usr/bin/env python3
"""
Sofia Twilio Smoke Test
Testa l'integrazione Twilio in produzione
"""

import os
import time
import json
import requests
import logging
from datetime import datetime
from typing import Dict, Optional

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

class TwilioSmokeTest:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.messaging_service_sid = os.getenv("TWILIO_MSID", "MGbb4ee25182f8fc4de2015ffcf98fb79d")
        self.to_phone = os.getenv("TWILIO_TO_TEST", "whatsapp:+393279467308")
        self.sofia_url = "https://sofia-lite-1075574333382.us-central1.run.app"
        
        if not self.account_sid or not self.auth_token:
            raise ValueError("TWILIO_ACCOUNT_SID e TWILIO_AUTH_TOKEN sono richiesti")
    
    def send_whatsapp_message(self, message: str) -> Optional[Dict]:
        """Invia messaggio WhatsApp via Twilio Messaging Service"""
        url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Messages.json"
        
        data = {
            "MessagingServiceSid": self.messaging_service_sid,
            "To": self.to_phone,
            "Body": message
        }
        
        try:
            response = requests.post(url, data=data, auth=(self.account_sid, self.auth_token), timeout=30)
            
            if response.status_code == 201:
                return response.json()
            else:
                log.error(f"❌ Errore Twilio: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            log.error(f"❌ Errore invio: {e}")
            return None
    
    def poll_webhook_response(self, message_sid: str, timeout: int = 15) -> Optional[Dict]:
        """Poll webhook response per verificare la risposta di Sofia"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Simula webhook call per verificare lo stato
                webhook_url = f"{self.sofia_url}/webhook/whatsapp"
                payload = {
                    "Body": "Ciao!",
                    "From": "whatsapp:+393331234567",
                    "MessageSid": message_sid
                }
                
                response = requests.post(webhook_url, json=payload, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("state") == "ASK_NAME":
                        return result
                
                time.sleep(1)
                
            except Exception as e:
                log.warning(f"⚠️ Errore polling: {e}")
                time.sleep(1)
        
        return None
    
    def run_smoke_test(self) -> bool:
        """Esegue il test smoke completo"""
        log.info("🚀 Avvio Smoke Test Twilio")
        
        # Step 1: Invia messaggio WhatsApp
        log.info("📤 Invio messaggio WhatsApp...")
        twilio_result = self.send_whatsapp_message("Ciao!")
        
        if not twilio_result:
            log.error("❌ FAIL: Errore invio WhatsApp")
            return False
        
        message_sid = twilio_result.get("sid")
        log.info(f"✅ Messaggio inviato: {message_sid}")
        
        # Step 2: Poll webhook response
        log.info("📥 Poll webhook response...")
        webhook_result = self.poll_webhook_response(message_sid)
        
        if not webhook_result:
            log.error("❌ FAIL: Timeout webhook response")
            return False
        
        # Step 3: Verifica stato
        state = webhook_result.get("state")
        if state == "ASK_NAME":
            log.info("✅ SUCCESS: Sofia risponde correttamente con stato ASK_NAME")
            return True
        else:
            log.error(f"❌ FAIL: Stato inaspettato {state}, atteso ASK_NAME")
            return False

def main():
    try:
        smoke_test = TwilioSmokeTest()
        success = smoke_test.run_smoke_test()
        
        if success:
            log.info("🎉 SMOKE TEST PASSED")
            exit(0)
        else:
            log.error("💥 SMOKE TEST FAILED")
            exit(1)
            
    except Exception as e:
        log.error(f"💥 SMOKE TEST ERROR: {e}")
        exit(1)

if __name__ == "__main__":
    main() 