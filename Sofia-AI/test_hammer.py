#!/usr/bin/env python3
"""
Test Hammer - Test completo per verificare tutti i miglioramenti implementati
"""

import asyncio
import json
import time
from typing import Dict, List, Tuple
import aiohttp
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurazione
BASE_URL = "https://sofia-lite-1075574333382.us-central1.run.app"
TIMEOUT = 30

class TestHammer:
    def __init__(self):
        self.session = None
        self.results = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=TIMEOUT))
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_endpoint(self, endpoint: str, payload: Dict, test_name: str, is_form_data: bool = False) -> Dict:
        """Testa un endpoint specifico"""
        try:
            start_time = time.time()
            
            if is_form_data:
                # Per Voice endpoint che usa form data
                data = aiohttp.FormData()
                for key, value in payload.items():
                    data.add_field(key, str(value))
                
                async with self.session.post(
                    f"{BASE_URL}/{endpoint}",
                    data=data
                ) as response:
                    response_time = time.time() - start_time
                    response_text = await response.text()
            else:
                # Per WhatsApp endpoint che usa JSON
                async with self.session.post(
                    f"{BASE_URL}/{endpoint}",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    response_time = time.time() - start_time
                    response_text = await response.text()
                
                try:
                    response_json = json.loads(response_text)
                except json.JSONDecodeError:
                    response_json = {"raw_response": response_text}
                
                result = {
                    "test_name": test_name,
                    "endpoint": endpoint,
                    "status_code": response.status,
                    "response_time": response_time,
                    "success": response.status == 200,
                    "response": response_json,
                    "payload": payload
                }
                
                logger.info(f"✅ {test_name}: {response.status} ({response_time:.2f}s)")
                return result
                
        except Exception as e:
            result = {
                "test_name": test_name,
                "endpoint": endpoint,
                "status_code": 0,
                "response_time": 0,
                "success": False,
                "error": str(e),
                "payload": payload
            }
            logger.error(f"❌ {test_name}: {str(e)}")
            return result

    async def run_whatsapp_tests(self) -> List[Dict]:
        """Testa tutti i casi WhatsApp"""
        tests = [
            # Test 1: Nome semplice italiano
            {
                "name": "WhatsApp - Nome semplice italiano",
                "payload": {
                    "Body": "Ciao, mi chiamo Mario Rossi",
                    "From": "whatsapp:+393331234567"
                }
            },
            
            # Test 2: Nome con caratteri speciali
            {
                "name": "WhatsApp - Nome con caratteri speciali",
                "payload": {
                    "Body": "Sono Mario@Rossi, piacere!",
                    "From": "whatsapp:+393331234568"
                }
            },
            
            # Test 3: Nome con numeri
            {
                "name": "WhatsApp - Nome con numeri",
                "payload": {
                    "Body": "Mi chiamo Mario123Rossi",
                    "From": "whatsapp:+393331234569"
                }
            },
            
            # Test 4: Nome francese
            {
                "name": "WhatsApp - Nome francese",
                "payload": {
                    "Body": "Bonjour, je m'appelle Jean-Pierre Dubois",
                    "From": "whatsapp:+33123456789"
                }
            },
            
            # Test 5: Nome spagnolo
            {
                "name": "WhatsApp - Nome spagnolo",
                "payload": {
                    "Body": "Hola, me llamo María José García",
                    "From": "whatsapp:+34612345678"
                }
            },
            
            # Test 6: Nome inglese
            {
                "name": "WhatsApp - Nome inglese",
                "payload": {
                    "Body": "Hi, I'm John Smith",
                    "From": "whatsapp:+1234567890"
                }
            },
            
            # Test 7: Nome arabo
            {
                "name": "WhatsApp - Nome arabo",
                "payload": {
                    "Body": "مرحبا، اسمي أحمد محمد",
                    "From": "whatsapp:+966501234567"
                }
            },
            
            # Test 8: Nome hindi
            {
                "name": "WhatsApp - Nome hindi",
                "payload": {
                    "Body": "नमस्ते, मेरा नाम राजेश कुमार है",
                    "From": "whatsapp:+919876543210"
                }
            },
            
            # Test 9: Nome bengalese
            {
                "name": "WhatsApp - Nome bengalese",
                "payload": {
                    "Body": "হ্যালো, আমার নাম রাহুল দাস",
                    "From": "whatsapp:+8801712345678"
                }
            },
            
            # Test 10: Nome con apostrofo
            {
                "name": "WhatsApp - Nome con apostrofo",
                "payload": {
                    "Body": "Ciao, sono Maria D'Angelo",
                    "From": "whatsapp:+393331234570"
                }
            }
        ]
        
        results = []
        for test in tests:
            result = await self.test_endpoint("webhook/whatsapp", test["payload"], test["name"])
            if result is not None:
                results.append(result)
            await asyncio.sleep(0.5)  # Pausa tra le richieste
            
        return results

    async def run_voice_tests(self) -> List[Dict]:
        """Testa tutti i casi Voice"""
        tests = [
            # Test 1: Nome semplice italiano
            {
                "name": "Voice - Nome semplice italiano",
                "payload": {
                    "SpeechResult": "Ciao, mi chiamo Mario Rossi",
                    "From": "+393331234567"
                }
            },
            
            # Test 2: Nome con caratteri speciali
            {
                "name": "Voice - Nome con caratteri speciali",
                "payload": {
                    "SpeechResult": "Sono Mario@Rossi, piacere!",
                    "From": "+393331234568"
                }
            },
            
            # Test 3: Nome con numeri
            {
                "name": "Voice - Nome con numeri",
                "payload": {
                    "SpeechResult": "Mi chiamo Mario123Rossi",
                    "From": "+393331234569"
                }
            },
            
            # Test 4: Nome francese
            {
                "name": "Voice - Nome francese",
                "payload": {
                    "SpeechResult": "Bonjour, je m'appelle Jean-Pierre Dubois",
                    "From": "+33123456789"
                }
            },
            
            # Test 5: Nome spagnolo
            {
                "name": "Voice - Nome spagnolo",
                "payload": {
                    "SpeechResult": "Hola, me llamo María José García",
                    "From": "+34612345678"
                }
            },
            
            # Test 6: Nome inglese
            {
                "name": "Voice - Nome inglese",
                "payload": {
                    "SpeechResult": "Hi, I'm John Smith",
                    "From": "+1234567890"
                }
            },
            
            # Test 7: Nome arabo
            {
                "name": "Voice - Nome arabo",
                "payload": {
                    "SpeechResult": "مرحبا، اسمي أحمد محمد",
                    "From": "+966501234567"
                }
            },
            
            # Test 8: Nome hindi
            {
                "name": "Voice - Nome hindi",
                "payload": {
                    "SpeechResult": "नमस्ते, मेरा नाम राजेश कुमार है",
                    "From": "+919876543210"
                }
            },
            
            # Test 9: Nome bengalese
            {
                "name": "Voice - Nome bengalese",
                "payload": {
                    "SpeechResult": "হ্যালো, আমার নাম রাহুল দাস",
                    "From": "+8801712345678"
                }
            },
            
            # Test 10: Nome con apostrofo
            {
                "name": "Voice - Nome con apostrofo",
                "payload": {
                    "SpeechResult": "Ciao, sono Maria D'Angelo",
                    "From": "+393331234570"
                }
            }
        ]
        
        results = []
        for test in tests:
            result = await self.test_endpoint("webhook/voice", test["payload"], test["name"], is_form_data=True)
            if result is not None:
                results.append(result)
            await asyncio.sleep(0.5)  # Pausa tra le richieste
            
        return results

    def analyze_results(self, results: List[Dict]) -> Dict:
        """Analizza i risultati dei test"""
        total_tests = len(results)
        successful_tests = sum(1 for r in results if r["success"])
        failed_tests = total_tests - successful_tests
        
        avg_response_time = sum(r["response_time"] for r in results if r["success"]) / successful_tests if successful_tests > 0 else 0
        
        # Analisi per endpoint
        whatsapp_results = [r for r in results if "whatsapp" in r["test_name"].lower()]
        voice_results = [r for r in results if "voice" in r["test_name"].lower()]
        
        whatsapp_success = sum(1 for r in whatsapp_results if r["success"])
        voice_success = sum(1 for r in voice_results if r["success"])
        
        # Analisi dei nomi estratti
        extracted_names = []
        for r in results:
            if r["success"] and "response" in r and isinstance(r["response"], dict):
                if "extracted_name" in r["response"]:
                    extracted_names.append(r["response"]["extracted_name"])
                elif "name" in r["response"]:
                    extracted_names.append(r["response"]["name"])
        
        return {
            "summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": failed_tests,
                "success_rate": (successful_tests / total_tests * 100) if total_tests > 0 else 0,
                "avg_response_time": avg_response_time
            },
            "by_endpoint": {
                "whatsapp": {
                    "total": len(whatsapp_results),
                    "successful": whatsapp_success,
                    "success_rate": (whatsapp_success / len(whatsapp_results) * 100) if whatsapp_results else 0
                },
                "voice": {
                    "total": len(voice_results),
                    "successful": voice_success,
                    "success_rate": (voice_success / len(voice_results) * 100) if voice_results else 0
                }
            },
            "extracted_names": extracted_names,
            "detailed_results": results
        }

    async def run_all_tests(self):
        """Esegue tutti i test"""
        logger.info("🚀 Avvio Test Hammer - Verifica miglioramenti implementati")
        logger.info(f"Target URL: {BASE_URL}")
        
        start_time = time.time()
        
        # Esegui test WhatsApp
        logger.info("\n📱 Testando endpoint WhatsApp...")
        whatsapp_results = await self.run_whatsapp_tests()
        
        # Esegui test Voice
        logger.info("\n📞 Testando endpoint Voice...")
        voice_results = await self.run_voice_tests()
        
        # Combina risultati
        all_results = whatsapp_results + voice_results
        
        # Analizza risultati
        analysis = self.analyze_results(all_results)
        
        total_time = time.time() - start_time
        
        # Stampa report
        self.print_report(analysis, total_time)
        
        return analysis

    def print_report(self, analysis: Dict, total_time: float):
        """Stampa il report dei test"""
        print("\n" + "="*80)
        print("🔨 TEST HAMMER - REPORT COMPLETO")
        print("="*80)
        
        summary = analysis["summary"]
        print(f"\n📊 RIEPILOGO GENERALE:")
        print(f"   • Test totali: {summary['total_tests']}")
        print(f"   • Test riusciti: {summary['successful_tests']}")
        print(f"   • Test falliti: {summary['failed_tests']}")
        print(f"   • Tasso di successo: {summary['success_rate']:.1f}%")
        print(f"   • Tempo medio di risposta: {summary['avg_response_time']:.2f}s")
        print(f"   • Tempo totale test: {total_time:.2f}s")
        
        print(f"\n📱 WHATSAPP:")
        whatsapp_stats = analysis["by_endpoint"]["whatsapp"]
        print(f"   • Test totali: {whatsapp_stats['total']}")
        print(f"   • Test riusciti: {whatsapp_stats['successful']}")
        print(f"   • Tasso di successo: {whatsapp_stats['success_rate']:.1f}%")
        
        print(f"\n📞 VOICE:")
        voice_stats = analysis["by_endpoint"]["voice"]
        print(f"   • Test totali: {voice_stats['total']}")
        print(f"   • Test riusciti: {voice_stats['successful']}")
        print(f"   • Tasso di successo: {voice_stats['success_rate']:.1f}%")
        
        print(f"\n👤 NOMI ESTRATTI ({len(analysis['extracted_names'])}):")
        for i, name in enumerate(analysis['extracted_names'], 1):
            print(f"   {i}. {name}")
        
        print(f"\n🔍 DETTAGLI ERRORI:")
        failed_tests = [r for r in analysis["detailed_results"] if not r["success"]]
        if failed_tests:
            for test in failed_tests:
                print(f"   ❌ {test['test_name']}: {test.get('error', 'Unknown error')}")
        else:
            print("   ✅ Nessun errore rilevato!")
        
        print("\n" + "="*80)
        
        # Salva report su file
        with open("test_hammer_report.json", "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print("📄 Report salvato in: test_hammer_report.json")

async def main():
    """Funzione principale"""
    async with TestHammer() as hammer:
        await hammer.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 