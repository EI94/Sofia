#!/usr/bin/env python3
"""
Hammer Send Module - Twilio Messaging Service Integration
Supporta template WhatsApp e rate limiting
"""

import os
import json
import time
import requests
import argparse
from datetime import datetime, timedelta
from typing import Dict, Optional

class TwilioSender:
    def __init__(self, msid: str = None):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.messaging_service_sid = msid or os.getenv("TWILIO_MSID", "MGbb4ee25182f8fc4de2015ffcf98fb79d")
        self.template = os.getenv("TWILIO_TEMPLATE", "hello_sandbox")
        self.last_send_time = 0
        
        if not self.account_sid or not self.auth_token:
            raise ValueError("TWILIO_ACCOUNT_SID e TWILIO_AUTH_TOKEN sono richiesti")
    
    def _rate_limit(self):
        """Rate limiter: max 1 msg/s"""
        now = time.time()
        time_since_last = now - self.last_send_time
        if time_since_last < 1.1:
            time.sleep(1.1 - time_since_last)
        self.last_send_time = time.time()
    
    def send_message(self, to: str, body: str, first_of_thread: bool = False) -> Dict:
        """Invia messaggio via Twilio Messaging Service"""
        self._rate_limit()
        
        url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Messages.json"
        
        # Usa sempre Body per ora, template non configurato
        data = {
            "MessagingServiceSid": self.messaging_service_sid,
            "To": to,
            "Body": body
        }
        
        response = requests.post(url, data=data, auth=(self.account_sid, self.auth_token))
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Twilio error {response.status_code}: {response.text}")
    
    def send_test_message(self, to: str) -> Dict:
        """Invia messaggio di test"""
        return self.send_message(to, "Ciao! Test Sofia GO-LIVE", first_of_thread=True)

def main():
    parser = argparse.ArgumentParser(description="Twilio Messaging Service Sender")
    parser.add_argument("--to", required=True, help="Numero destinatario")
    parser.add_argument("--body", required=True, help="Corpo del messaggio")
    parser.add_argument("--msid", help="Messaging Service SID")
    parser.add_argument("--first", action="store_true", help="Primo messaggio del thread")
    parser.add_argument("--test", action="store_true", help="Invia messaggio di test")
    
    args = parser.parse_args()
    
    try:
        sender = TwilioSender(args.msid)
        
        if args.test:
            result = sender.send_test_message(args.to)
        else:
            result = sender.send_message(args.to, args.body, args.first)
        
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main() 