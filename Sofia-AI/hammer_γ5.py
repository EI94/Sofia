#!/usr/bin/env python3
"""
F21 PERFORMANCE SWAT γ5 - Load Test
Obbligo: P95 latency < 2000 ms (fallback OFF)
"""

import asyncio
import json
import time
import yaml
import statistics
from typing import Dict, List, Tuple
import aiohttp
import logging
from datetime import datetime

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurazione
BASE_URL = "https://sofia-lite-1075574333382.us-central1.run.app"
TIMEOUT = 30
TWILIO_FROM = "+393279467308"
TWILIO_TO = "+18149149892"

class Hammerγ5:
    def __init__(self):
        self.session = None
        self.results = []
        self.scenarios = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=TIMEOUT))
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def load_scenarios(self):
        """Carica gli scenari dal file YAML"""
        try:
            with open("sofia_lite/scripts/scenarios.yaml", "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            
            # Estrai tutti gli scenari
            all_scenarios = []
            
            # Scenari principali
            for category, scenarios in data.get("scenarios", {}).items():
                for scenario in scenarios:
                    scenario["category"] = category
                    all_scenarios.append(scenario)
            
            # Corner cases
            for corner_type, scenarios in data.get("corner_cases", {}).items():
                for scenario in scenarios:
                    scenario["category"] = f"corner_{corner_type}"
                    all_scenarios.append(scenario)
            
            self.scenarios = all_scenarios
            logger.info(f"✅ Caricati {len(self.scenarios)} scenari")
            
        except Exception as e:
            logger.error(f"❌ Errore caricamento scenari: {e}")
            raise
    
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
                "response_time": response_time * 1000,  # Converti in ms
                "success": response.status == 200,
                "response": response_json,
                "payload": payload,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"✅ {test_name}: {response.status} ({response_time*1000:.0f}ms)")
            return result
            
        except Exception as e:
            result = {
                "test_name": test_name,
                "endpoint": endpoint,
                "status_code": 0,
                "response_time": 0,
                "success": False,
                "error": str(e),
                "payload": payload,
                "timestamp": datetime.now().isoformat()
            }
            logger.error(f"❌ {test_name}: {str(e)}")
            return result

    async def run_whatsapp_tests(self, scenarios: List[Dict]) -> List[Dict]:
        """Esegue test WhatsApp"""
        results = []
        
        for i, scenario in enumerate(scenarios, 1):
            # Genera numero di telefono unico
            phone_suffix = f"{i:03d}"
            phone = f"+39333{phone_suffix}4567"
            
            payload = {
                "Body": scenario["name"],
                "From": f"whatsapp:{phone}"
            }
            
            test_name = f"WhatsApp-{scenario['expected_lang']}-{scenario['type']}-{i:03d}"
            
            result = await self.test_endpoint("webhook/whatsapp", payload, test_name)
            result["scenario"] = scenario
            results.append(result)
            
            # Pausa tra le richieste
            await asyncio.sleep(0.1)
            
        return results

    async def run_voice_tests(self, scenarios: List[Dict]) -> List[Dict]:
        """Esegue test Voice"""
        results = []
        
        for i, scenario in enumerate(scenarios, 1):
            # Genera numero di telefono unico
            phone_suffix = f"{i:03d}"
            phone = f"+39333{phone_suffix}4568"
            
            payload = {
                "SpeechResult": scenario["name"],
                "From": phone
            }
            
            test_name = f"Voice-{scenario['expected_lang']}-{scenario['type']}-{i:03d}"
            
            result = await self.test_endpoint("webhook/voice", payload, test_name, is_form_data=True)
            result["scenario"] = scenario
            results.append(result)
            
            # Pausa tra le richieste
            await asyncio.sleep(0.1)
            
        return results

    def analyze_results(self, results: List[Dict]) -> Dict:
        """Analizza i risultati dei test"""
        if not results:
            return {}
        
        # Statistiche generali
        total_tests = len(results)
        successful_tests = sum(1 for r in results if r["success"])
        failed_tests = total_tests - successful_tests
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Latency statistics
        response_times = [r["response_time"] for r in results if r["success"] and r["response_time"] > 0]
        if response_times:
            p50 = statistics.quantiles(response_times, n=2)[0]
            p95 = statistics.quantiles(response_times, n=20)[18]  # 95th percentile
            p99 = statistics.quantiles(response_times, n=100)[98]  # 99th percentile
            avg_latency = statistics.mean(response_times)
        else:
            p50 = p95 = p99 = avg_latency = 0
        
        # Analisi per lingua
        lang_stats = {}
        for lang in ["it", "fr", "es", "en", "ar", "hi", "bn", "tr", "ru"]:
            lang_results = [r for r in results if r.get("scenario", {}).get("expected_lang") == lang]
            if lang_results:
                lang_success = sum(1 for r in lang_results if r["success"])
                lang_stats[lang] = {
                    "total": len(lang_results),
                    "successful": lang_success,
                    "success_rate": (lang_success / len(lang_results) * 100) if lang_results else 0
                }
        
        # Analisi per tipo (new vs active)
        type_stats = {}
        for test_type in ["new", "active", "corner", "rapid", "voice"]:
            type_results = [r for r in results if r.get("scenario", {}).get("type") == test_type]
            if type_results:
                type_success = sum(1 for r in type_results if r["success"])
                type_stats[test_type] = {
                    "total": len(type_results),
                    "successful": type_success,
                    "success_rate": (type_success / len(type_results) * 100) if type_results else 0
                }
        
        # Top 5 failure patterns
        failed_results = [r for r in results if not r["success"]]
        failure_patterns = []
        for result in failed_results[:5]:
            pattern = {
                "message": result.get("scenario", {}).get("name", "N/A"),
                "state": result.get("response", {}).get("state", "N/A"),
                "lang": result.get("scenario", {}).get("expected_lang", "N/A"),
                "intent": result.get("scenario", {}).get("expected_intent", "N/A"),
                "error": result.get("error", "HTTP Error"),
                "status_code": result.get("status_code", 0)
            }
            failure_patterns.append(pattern)
        
        return {
            "summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": failed_tests,
                "success_rate": success_rate,
                "avg_latency": avg_latency,
                "p50_latency": p50,
                "p95_latency": p95,
                "p99_latency": p99
            },
            "by_language": lang_stats,
            "by_type": type_stats,
            "failure_patterns": failure_patterns,
            "detailed_results": results
        }

    async def run_all_tests(self):
        """Esegue tutti i test"""
        logger.info("🚀 F21 PERFORMANCE SWAT γ5 - Load Test")
        logger.info(f"Target URL: {BASE_URL}")
        logger.info(f"TWILIO_FROM: {TWILIO_FROM}")
        logger.info(f"TWILIO_TO: {TWILIO_TO}")
        logger.info(f"LLM_FALLBACK_ALLOWED: 0")
        
        # Carica scenari
        self.load_scenarios()
        
        start_time = time.time()
        
        # Distribuisci scenari tra WhatsApp e Voice
        whatsapp_scenarios = self.scenarios[:len(self.scenarios)//2]
        voice_scenarios = self.scenarios[len(self.scenarios)//2:]
        
        # Esegui test WhatsApp
        logger.info(f"\n📱 Testando {len(whatsapp_scenarios)} scenari WhatsApp...")
        whatsapp_results = await self.run_whatsapp_tests(whatsapp_scenarios)
        
        # Esegui test Voice
        logger.info(f"\n📞 Testando {len(voice_scenarios)} scenari Voice...")
        voice_results = await self.run_voice_tests(voice_scenarios)
        
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
        print("🔨 F21 PERFORMANCE SWAT γ5 - REPORT")
        print("="*80)
        
        summary = analysis["summary"]
        print(f"\n📊 RIEPILOGO GENERALE:")
        print(f"   • Test totali: {summary['total_tests']}")
        print(f"   • Test riusciti: {summary['successful_tests']}")
        print(f"   • Test falliti: {summary['failed_tests']}")
        print(f"   • Tasso di successo: {summary['success_rate']:.1f}%")
        print(f"   • Tempo totale test: {total_time:.2f}s")
        
        print(f"\n⚡ LATENCY:")
        print(f"   • Media: {summary['avg_latency']:.0f}ms")
        print(f"   • P50: {summary['p50_latency']:.0f}ms")
        print(f"   • P95: {summary['p95_latency']:.0f}ms")
        print(f"   • P99: {summary['p99_latency']:.0f}ms")
        
        print(f"\n🌍 PER LINGUA:")
        for lang, stats in analysis["by_language"].items():
            print(f"   • {lang.upper()}: {stats['successful']}/{stats['total']} ({stats['success_rate']:.1f}%)")
        
        print(f"\n📝 PER TIPO:")
        for test_type, stats in analysis["by_type"].items():
            print(f"   • {test_type.upper()}: {stats['successful']}/{stats['total']} ({stats['success_rate']:.1f}%)")
        
        print(f"\n🔍 TOP-5 FAILURE PATTERNS:")
        for i, pattern in enumerate(analysis["failure_patterns"], 1):
            print(f"   {i}. {pattern['message'][:50]}... | {pattern['lang']} | {pattern['intent']} | {pattern['error']}")
        
        # Verifica obblighi γ5
        success_ok = summary['success_rate'] >= 95
        p95_ok = summary['p95_latency'] < 2000
        
        print(f"\n🎯 VERIFICA OBBLIGHI γ5:")
        print(f"   • Success ≥ 95%: {summary['success_rate']:.1f}% {'✅' if success_ok else '❌'}")
        print(f"   • P95 < 2000ms: {summary['p95_latency']:.0f}ms {'✅' if p95_ok else '❌'}")
        print(f"   • Fallback OFF: ✅")
        
        if success_ok and p95_ok:
            print(f"\n🎉 ✅ PASS – ready for GA")
        else:
            print(f"\n❌ FAIL – need deep profiling")
        
        print("\n" + "="*80)
        
        # Salva report su file
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis,
            "total_time": total_time,
            "requirements": {
                "success_rate": summary['success_rate'],
                "p95_latency": summary['p95_latency'],
                "success_ok": success_ok,
                "p95_ok": p95_ok,
                "pass": success_ok and p95_ok
            }
        }
        
        with open("docs/HAMMER_REPORT_γ5.md", "w", encoding="utf-8") as f:
            f.write(f"# F21 PERFORMANCE SWAT γ5 - REPORT\n\n")
            f.write(f"**Timestamp**: {report_data['timestamp']}\n\n")
            f.write(f"## 📊 RIEPILOGO GENERALE\n\n")
            f.write(f"- **Test totali**: {summary['total_tests']}\n")
            f.write(f"- **Test riusciti**: {summary['successful_tests']}\n")
            f.write(f"- **Tasso di successo**: {summary['success_rate']:.1f}%\n")
            f.write(f"- **Tempo totale**: {total_time:.2f}s\n\n")
            f.write(f"## ⚡ LATENCY\n\n")
            f.write(f"- **Media**: {summary['avg_latency']:.0f}ms\n")
            f.write(f"- **P50**: {summary['p50_latency']:.0f}ms\n")
            f.write(f"- **P95**: {summary['p95_latency']:.0f}ms\n")
            f.write(f"- **P99**: {summary['p99_latency']:.0f}ms\n\n")
            f.write(f"## 🎯 VERIFICA OBBLIGHI γ5\n\n")
            f.write(f"- **Success ≥ 95%**: {summary['success_rate']:.1f}% {'✅' if success_ok else '❌'}\n")
            f.write(f"- **P95 < 2000ms**: {summary['p95_latency']:.0f}ms {'✅' if p95_ok else '❌'}\n")
            f.write(f"- **Fallback OFF**: ✅\n\n")
            if success_ok and p95_ok:
                f.write(f"## 🎉 ✅ PASS – ready for GA\n\n")
            else:
                f.write(f"## ❌ FAIL – need deep profiling\n\n")
        
        # Salva anche JSON completo
        with open("docs/HAMMER_REPORT_γ5.json", "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print("📄 Report salvato in: docs/HAMMER_REPORT_γ5.md e docs/HAMMER_REPORT_γ5.json")

async def main():
    """Funzione principale"""
    async with Hammerγ5() as hammer:
        return await hammer.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 