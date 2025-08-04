#!/usr/bin/env python3
"""
HAMMER ULTIMATE – JOURNEY AUDIT
Esegue test completo per validare tutte le 9 tappe del journey
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
import os

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurazione
BASE_URL = "https://sofia-lite-1075574333382.us-central1.run.app"
TIMEOUT = 30
WA_FROM = os.getenv("WA_FROM", "+18149149892")

class HammerUltimate:
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
    
    def load_journey_scenarios(self):
        """Carica scenari journey dal file YAML"""
        try:
            with open("hammer/scenarios_journey.yaml", "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            
            # Estrai tutti gli scenari
            all_scenarios = []
            
            for category, scenarios in data.get("scenarios", {}).items():
                if isinstance(scenarios, list):
                    for scenario in scenarios:
                        scenario["category"] = category
                        all_scenarios.append(scenario)
            
            self.scenarios = all_scenarios
            logger.info(f"✅ Caricati {len(self.scenarios)} scenari journey")
            
        except Exception as e:
            logger.error(f"❌ Errore caricamento scenari: {e}")
            raise
    
    async def test_journey_scenario(self, scenario: Dict) -> Dict:
        """Testa un singolo scenario journey completo"""
        
        scenario_id = scenario.get("scenario_id", "unknown")
        language = scenario.get("language", "unknown")
        channel = scenario.get("channel", "text")
        user_type = scenario.get("user_type", "new")
        journey = scenario.get("journey", [])
        
        logger.info(f"🎯 Testing scenario: {scenario_id} ({language}, {channel}, {user_type})")
        
        # Genera numero di telefono unico
        phone_suffix = scenario_id.replace("_", "").replace("-", "")[-6:]
        phone = f"+39333{phone_suffix}4567"
        
        result = {
            "scenario_id": scenario_id,
            "language": language,
            "channel": channel,
            "user_type": user_type,
            "phone": phone,
            "turns": [],
            "success": True,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "total_duration": 0
        }
        
        start_time = time.time()
        
        try:
            # Esegui ogni turn del journey
            for i, turn in enumerate(journey, 1):
                user_input = turn.get("user_input", "")
                expected_state = turn.get("expect_state", "")
                
                logger.info(f"  Turn {i}: {user_input[:50]}... → {expected_state}")
                
                # Testa il turn
                turn_result = await self.test_single_turn(
                    phone, user_input, channel, i, expected_state
                )
                
                result["turns"].append(turn_result)
                
                # Se il turn fallisce, interrompi il journey
                if not turn_result["success"]:
                    result["success"] = False
                    logger.warning(f"  ❌ Turn {i} failed: {turn_result['error']}")
                    break
                
                # Pausa tra i turn
                await asyncio.sleep(0.5)
            
            end_time = time.time()
            result["end_time"] = datetime.now().isoformat()
            result["total_duration"] = end_time - start_time
            
            if result["success"]:
                logger.info(f"✅ Scenario {scenario_id} completed successfully")
            else:
                logger.warning(f"❌ Scenario {scenario_id} failed")
            
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            logger.error(f"❌ Scenario {scenario_id} error: {e}")
        
        return result
    
    async def test_single_turn(self, phone: str, user_input: str, channel: str, turn_num: int, expected_state: str) -> Dict:
        """Testa un singolo turn del journey"""
        
        try:
            start_time = time.time()
            
            if channel == "text":
                # Test WhatsApp text
                payload = {
                    "Body": user_input,
                    "From": f"whatsapp:{phone}"
                }
                
                async with self.session.post(
                    f"{BASE_URL}/webhook/whatsapp",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    response_time = time.time() - start_time
                    response_text = await response.text()
                    
            elif channel == "voice_note":
                # Test WhatsApp voice note
                payload = {
                    "Body": user_input,
                    "From": f"whatsapp:{phone}",
                    "MediaUrl0": "https://example.com/sample.ogg",
                    "NumMedia": "1",
                    "MediaContentType0": "audio/ogg"
                }
                
                async with self.session.post(
                    f"{BASE_URL}/webhook/whatsapp",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    response_time = time.time() - start_time
                    response_text = await response.text()
                    
            elif channel == "voice_call":
                # Test Voice call
                payload = {
                    "SpeechResult": user_input,
                    "From": phone
                }
                
                async with self.session.post(
                    f"{BASE_URL}/webhook/voice",
                    data=payload
                ) as response:
                    response_time = time.time() - start_time
                    response_text = await response.text()
            
            # Parse response
            try:
                response_json = json.loads(response_text)
                sofia_reply = response_json.get("reply", "")
                actual_state = response_json.get("state", "UNKNOWN")
                lang_detected = response_json.get("lang", "unknown")
            except json.JSONDecodeError:
                response_json = {"raw_response": response_text}
                sofia_reply = response_text
                actual_state = "UNKNOWN"
                lang_detected = "unknown"
            
            # Valida stato
            success = actual_state == expected_state
            
            turn_result = {
                "turn": turn_num,
                "user_input": user_input,
                "expected_state": expected_state,
                "actual_state": actual_state,
                "sofia_reply": sofia_reply,
                "lang_detected": lang_detected,
                "response_time": response_time * 1000,
                "success": success,
                "status_code": response.status
            }
            
            if not success:
                turn_result["error"] = f"Expected '{expected_state}', got '{actual_state}'"
            
            return turn_result
            
        except Exception as e:
            return {
                "turn": turn_num,
                "user_input": user_input,
                "expected_state": expected_state,
                "actual_state": "ERROR",
                "error": str(e),
                "response_time": 0,
                "success": False,
                "status_code": 0
            }
    
    async def run_ultimate_test(self):
        """Esegue il test ultimate completo"""
        logger.info("🚀 HAMMER ULTIMATE – JOURNEY AUDIT")
        logger.info(f"Target URL: {BASE_URL}")
        logger.info(f"Scenarios: {len(self.scenarios)}")
        
        # Carica scenari
        self.load_journey_scenarios()
        
        start_time = time.time()
        
        # Esegui test per ogni scenario
        for i, scenario in enumerate(self.scenarios, 1):
            logger.info(f"\n📊 Progress: {i}/{len(self.scenarios)}")
            
            result = await self.test_journey_scenario(scenario)
            self.results.append(result)
            
            # Pausa tra scenari
            await asyncio.sleep(1)
        
        total_time = time.time() - start_time
        
        # Analizza risultati
        analysis = self.analyze_results()
        
        # Salva risultati
        self.save_results(analysis, total_time)
        
        return analysis
    
    def analyze_results(self) -> Dict:
        """Analizza i risultati dei test"""
        
        if not self.results:
            return {}
        
        # Statistiche generali
        total_scenarios = len(self.results)
        successful_scenarios = sum(1 for r in self.results if r["success"])
        failed_scenarios = total_scenarios - successful_scenarios
        success_rate = (successful_scenarios / total_scenarios * 100) if total_scenarios > 0 else 0
        
        # Analisi per lingua
        lang_stats = {}
        for lang in ["it", "fr", "es", "en", "ar", "hi", "bn", "tr", "ru"]:
            lang_results = [r for r in self.results if r.get("language") == lang]
            if lang_results:
                lang_success = sum(1 for r in lang_results if r["success"])
                lang_stats[lang] = {
                    "total": len(lang_results),
                    "successful": lang_success,
                    "success_rate": (lang_success / len(lang_results) * 100) if lang_results else 0
                }
        
        # Analisi per step (stato)
        step_stats = {}
        for step in ["GREETING", "ASK_NAME", "ASK_SERVICE", "PROPOSE_CONSULT", "ASK_CHANNEL", "ASK_SLOT", "ASK_PAYMENT", "CONFIRM_BOOKING", "ROUTE_ACTIVE"]:
            step_results = []
            for result in self.results:
                for turn in result.get("turns", []):
                    if turn.get("expected_state") == step:
                        step_results.append(turn)
            
            if step_results:
                step_success = sum(1 for r in step_results if r["success"])
                step_stats[step] = {
                    "total": len(step_results),
                    "successful": step_success,
                    "success_rate": (step_success / len(step_results) * 100) if step_results else 0
                }
        
        # Analisi per channel
        channel_stats = {}
        for channel in ["text", "voice_note", "voice_call"]:
            channel_results = [r for r in self.results if r.get("channel") == channel]
            if channel_results:
                channel_success = sum(1 for r in channel_results if r["success"])
                channel_stats[channel] = {
                    "total": len(channel_results),
                    "successful": channel_success,
                    "success_rate": (channel_success / len(channel_results) * 100) if channel_results else 0
                }
        
        # Top failures
        failed_results = [r for r in self.results if not r["success"]]
        top_failures = []
        for result in failed_results[:10]:
            failure = {
                "scenario_id": result.get("scenario_id"),
                "language": result.get("language"),
                "channel": result.get("channel"),
                "error": result.get("error", "Unknown error"),
                "failed_turn": None
            }
            
            # Trova il turn fallito
            for turn in result.get("turns", []):
                if not turn.get("success"):
                    failure["failed_turn"] = turn.get("turn")
                    failure["expected_state"] = turn.get("expected_state")
                    failure["actual_state"] = turn.get("actual_state")
                    break
            
            top_failures.append(failure)
        
        return {
            "summary": {
                "total_scenarios": total_scenarios,
                "successful_scenarios": successful_scenarios,
                "failed_scenarios": failed_scenarios,
                "success_rate": success_rate
            },
            "by_language": lang_stats,
            "by_step": step_stats,
            "by_channel": channel_stats,
            "top_failures": top_failures,
            "detailed_results": self.results
        }
    
    def save_results(self, analysis: Dict, total_time: float):
        """Salva i risultati su file"""
        
        # Salva risultati raw
        raw_data = {
            "timestamp": datetime.now().isoformat(),
            "total_time": total_time,
            "analysis": analysis,
            "results": self.results
        }
        
        with open("docs/HAMMER_RAW_JOURNEY.json", "w", encoding="utf-8") as f:
            json.dump(raw_data, f, indent=2, ensure_ascii=False)
        
        logger.info("📄 Risultati salvati in: docs/HAMMER_RAW_JOURNEY.json")
        
        # Stampa summary
        self.print_summary(analysis, total_time)
    
    def print_summary(self, analysis: Dict, total_time: float):
        """Stampa il summary dei risultati"""
        
        summary = analysis["summary"]
        
        print("\n" + "="*80)
        print("🔨 HAMMER ULTIMATE – JOURNEY AUDIT COMPLETATO")
        print("="*80)
        
        print(f"\n📊 RIEPILOGO GENERALE:")
        print(f"   • Scenari totali: {summary['total_scenarios']}")
        print(f"   • Scenari riusciti: {summary['successful_scenarios']}")
        print(f"   • Scenari falliti: {summary['failed_scenarios']}")
        print(f"   • Tasso di successo: {summary['success_rate']:.1f}%")
        print(f"   • Tempo totale: {total_time:.2f}s")
        
        print(f"\n🌍 PER LINGUA:")
        for lang, stats in analysis["by_language"].items():
            status = "✅" if stats['success_rate'] >= 95 else "❌"
            print(f"   • {lang.upper()}: {stats['success_rate']:.1f}% ({stats['successful']}/{stats['total']}) {status}")
        
        print(f"\n🎯 PER STEP:")
        for step, stats in analysis["by_step"].items():
            status = "✅" if stats['success_rate'] >= 95 else "❌"
            print(f"   • {step}: {stats['success_rate']:.1f}% ({stats['successful']}/{stats['total']}) {status}")
        
        print(f"\n📱 PER CANALE:")
        for channel, stats in analysis["by_channel"].items():
            status = "✅" if stats['success_rate'] >= 95 else "❌"
            print(f"   • {channel.upper()}: {stats['success_rate']:.1f}% ({stats['successful']}/{stats['total']}) {status}")
        
        # Verifica GO/NO-GO
        all_passed = True
        for lang_data in analysis["by_language"].values():
            if lang_data["success_rate"] < 95:
                all_passed = False
                break
        
        for step_data in analysis["by_step"].values():
            if step_data["success_rate"] < 95:
                all_passed = False
                break
        
        if all_passed:
            print(f"\n🎉 VERDETTO: **GO** ✅")
            print(f"   Tutte le lingue e tutti gli step hanno raggiunto ≥ 95%!")
        else:
            print(f"\n❌ VERDETTO: **NO-GO** ❌")
            print(f"   Alcune lingue o step non hanno raggiunto il 95% richiesto.")
        
        print("\n" + "="*80)

async def main():
    """Funzione principale"""
    async with HammerUltimate() as hammer:
        return await hammer.run_ultimate_test()

if __name__ == "__main__":
    asyncio.run(main()) 