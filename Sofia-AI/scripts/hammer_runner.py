#!/usr/bin/env python3
"""
Sofia Lite - Hammer Production Test Runner
Direct Webhook Testing with TEST_WEBHOOK=true
"""

import os
import sys
import yaml
import time
import json
import logging
import requests
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import argparse

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

class HammerRunner:
    def __init__(self):
        self.cloud_run_url = os.getenv("CLOUD_RUN_URL", "https://sofia-lite-jtcm2gle4a-uc.a.run.app")
        self.test_webhook = os.getenv("TEST_WEBHOOK", "true")
        self.results = []
        self.start_time = time.time()
        
        # Validate environment
        self._validate_env()
        
    def _validate_env(self):
        """Validate required environment variables"""
        required_vars = [
            "OPENAI_API_KEY",
            "TWILIO_ACCOUNT_SID", 
            "TWILIO_AUTH_TOKEN",
            "FIREBASE_CRED_JSON",
            "GCP_PROJECT_ID"
        ]
        
        missing = []
        for var in required_vars:
            if not os.getenv(var):
                missing.append(var)
        
        if missing:
            log.error(f"❌ MISSING ENV VARS: {missing}")
            sys.exit(1)
            
        log.info("✅ Environment validation passed")
    
    def _load_scenarios(self, scenarios_file: str) -> List[Dict]:
        """Load scenarios from YAML file"""
        scenarios_path = Path(__file__).parent / scenarios_file
        with open(scenarios_path, 'r', encoding='utf-8') as f:
            scenarios = yaml.safe_load(f)
        
        log.info(f"📋 Loaded {len(scenarios)} scenarios from {scenarios_path}")
        return scenarios
    
    def _clean_firestore_user(self, phone: str):
        """Clean Firestore document for test isolation"""
        try:
            import firebase_admin
            from firebase_admin import credentials, firestore
            
            # Initialize Firebase if not already done
            if not firebase_admin._apps:
                cred_json = os.getenv("FIREBASE_CRED_JSON")
                cred = credentials.Certificate(json.loads(cred_json))
                firebase_admin.initialize_app(cred)
            
            db = firestore.client()
            doc_ref = db.collection('users').document(phone)
            doc_ref.delete()
            log.info(f"🧹 Cleaned Firestore user: {phone}")
            
        except Exception as e:
            log.warning(f"⚠️ Error cleaning Firestore {phone}: {e}")
    
    def _send_webhook_request(self, scenario: Dict, step: Dict) -> Dict:
        """Send webhook request to Sofia Lite"""
        try:
            # Prepare Twilio-like payload
            payload = {
                "From": scenario["from"],
                "To": scenario["to"],
                "Body": step["user"],
                "NumMedia": "0"
            }
            
            # Send POST request to webhook
            url = f"{self.cloud_run_url}/webhook/whatsapp"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            
            start_time = time.time()
            response = requests.post(url, data=payload, headers=headers, timeout=30)
            latency = (time.time() - start_time) * 1000  # Convert to ms
            
            if response.status_code == 200:
                response_data = response.json()
                return {
                    "success": True,
                    "latency": latency,
                    "response": response_data,
                    "reply": response_data.get("reply", "")
                }
            else:
                return {
                    "success": False,
                    "latency": latency,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "latency": 0,
                "error": str(e)
            }
    
    def _validate_journey_compliance(self, scenario: Dict, responses: List[Dict]) -> Dict:
        """Validate if responses follow expected user journey"""
        journey_pass = True
        fail_reason = None
        
        # Check if all steps got responses
        if len(responses) != len(scenario["steps"]):
            journey_pass = False
            fail_reason = f"Expected {len(scenario['steps'])} responses, got {len(responses)}"
            return {"journey_pass": journey_pass, "fail_reason": fail_reason}
        
        # Check each step
        for i, (step, response) in enumerate(zip(scenario["steps"], responses)):
            if not response["success"]:
                journey_pass = False
                fail_reason = f"Step {i+1} failed: {response.get('error', 'Unknown error')}"
                break
            
            # Check if response contains expected content
            reply = response["reply"].lower()
            expected_intent = step["expect_intent"]
            
            # Simple content validation based on intent
            if expected_intent == "GREET":
                if not any(word in reply for word in ["ciao", "salve", "buongiorno", "hello", "hi", "bonjour", "hola"]):
                    journey_pass = False
                    fail_reason = f"Step {i+1}: Expected greeting, got: {reply[:50]}"
                    break
            elif expected_intent == "ASK_NAME":
                if not any(word in reply for word in ["nome", "name", "chiami", "appelle", "llamo"]):
                    journey_pass = False
                    fail_reason = f"Step {i+1}: Expected name request, got: {reply[:50]}"
                    break
            elif expected_intent == "ASK_SERVICE":
                if not any(word in reply for word in ["servizi", "services", "offriamo", "offer", "aiuto", "help"]):
                    journey_pass = False
                    fail_reason = f"Step {i+1}: Expected service inquiry, got: {reply[:50]}"
                    break
            elif expected_intent == "CLARIFY":
                if not any(word in reply for word in ["non ho capito", "didn't understand", "non comprendo", "clarify"]):
                    journey_pass = False
                    fail_reason = f"Step {i+1}: Expected clarification, got: {reply[:50]}"
                    break
        
        return {"journey_pass": journey_pass, "fail_reason": fail_reason}
    
    def _run_scenario(self, scenario: Dict) -> Dict:
        """Run a single scenario"""
        log.info(f"🚀 Running scenario: {scenario['id']} ({scenario['type']} - {scenario['lang']})")
        
        # Clean Firestore for test isolation
        phone = scenario["to"]
        self._clean_firestore_user(phone)
        
        responses = []
        total_latency = 0
        
        # Run each step
        for i, step in enumerate(scenario["steps"]):
            log.info(f"  📝 Step {i+1}: {step['user'][:30]}...")
            
            response = self._send_webhook_request(scenario, step)
            responses.append(response)
            total_latency += response["latency"]
            
            # Small delay between steps
            time.sleep(1)
        
        # Validate journey compliance
        journey_validation = self._validate_journey_compliance(scenario, responses)
        
        # Calculate metrics
        avg_latency = total_latency / len(responses) if responses else 0
        success_count = sum(1 for r in responses if r["success"])
        success_rate = success_count / len(responses) if responses else 0
        
        result = {
            "scenario_id": scenario["id"],
            "type": scenario["type"],
            "lang": scenario["lang"],
            "steps_count": len(scenario["steps"]),
            "success_count": success_count,
            "success_rate": success_rate,
            "avg_latency": avg_latency,
            "total_latency": total_latency,
            "journey_pass": journey_validation["journey_pass"],
            "fail_reason": journey_validation["fail_reason"],
            "responses": responses
        }
        
        status = "✅ PASS" if result["journey_pass"] else "❌ FAIL"
        log.info(f"  {status} - Success: {success_count}/{len(responses)}, Avg Latency: {avg_latency:.0f}ms")
        
        return result
    
    def run_all_scenarios(self, scenarios_file: str, report_file: str):
        """Run all scenarios and generate report"""
        scenarios = self._load_scenarios(scenarios_file)
        
        log.info(f"🎯 Starting Hammer Production Test - {len(scenarios)} scenarios")
        log.info(f"🌐 Target: {self.cloud_run_url}")
        log.info(f"🔧 Test Webhook: {self.test_webhook}")
        
        # Run scenarios
        for scenario in scenarios:
            result = self._run_scenario(scenario)
            self.results.append(result)
            
            # Progress update every 10 scenarios
            if len(self.results) % 10 == 0:
                passed = sum(1 for r in self.results if r["journey_pass"])
                log.info(f"📊 Progress: {len(self.results)}/{len(scenarios)} - Passed: {passed}")
        
        # Generate report
        self._generate_report(report_file)
    
    def _generate_report(self, report_file: str):
        """Generate comprehensive test report"""
        total_scenarios = len(self.results)
        passed_scenarios = sum(1 for r in self.results if r["journey_pass"])
        failed_scenarios = total_scenarios - passed_scenarios
        success_rate = (passed_scenarios / total_scenarios) * 100 if total_scenarios > 0 else 0
        
        # Calculate latencies
        latencies = [r["avg_latency"] for r in self.results if r["avg_latency"] > 0]
        p95_latency = sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        
        # Success rate by type
        new_scenarios = [r for r in self.results if r["type"] == "new"]
        active_scenarios = [r for r in self.results if r["type"] == "active"]
        
        new_success_rate = (sum(1 for r in new_scenarios if r["journey_pass"]) / len(new_scenarios) * 100) if new_scenarios else 0
        active_success_rate = (sum(1 for r in active_scenarios if r["journey_pass"]) / len(active_scenarios) * 100) if active_scenarios else 0
        
        # Success rate by language
        lang_stats = {}
        for result in self.results:
            lang = result["lang"]
            if lang not in lang_stats:
                lang_stats[lang] = {"total": 0, "passed": 0}
            lang_stats[lang]["total"] += 1
            if result["journey_pass"]:
                lang_stats[lang]["passed"] += 1
        
        lang_success_rates = {}
        for lang, stats in lang_stats.items():
            lang_success_rates[lang] = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
        
        # Top failures
        failures = [r for r in self.results if not r["journey_pass"]]
        top_failures = sorted(failures, key=lambda x: x["scenario_id"])[:10]
        
        # Generate report
        report_content = f"""# Sofia Lite - Hammer Production Test Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Target:** {self.cloud_run_url}
**Test Webhook:** {self.test_webhook}

## 📊 Overall Results

- **Total Scenarios:** {total_scenarios}
- **Passed:** {passed_scenarios}
- **Failed:** {failed_scenarios}
- **Success Rate:** {success_rate:.1f}%
- **Average Latency:** {avg_latency:.0f}ms
- **P95 Latency:** {p95_latency:.0f}ms

## 📈 Success Rates by Type

- **New Users:** {new_success_rate:.1f}% ({len(new_scenarios)} scenarios)
- **Active Users:** {active_success_rate:.1f}% ({len(active_scenarios)} scenarios)

## 🌍 Success Rates by Language

"""
        
        for lang, rate in sorted(lang_success_rates.items()):
            report_content += f"- **{lang.upper()}:** {rate:.1f}%\n"
        
        report_content += f"""
## ❌ Top 10 Failures

"""
        
        for failure in top_failures:
            report_content += f"- **{failure['scenario_id']}** ({failure['type']} - {failure['lang']}): {failure['fail_reason']}\n"
        
        report_content += f"""
## 🎯 Target Compliance

- **Success Rate Target:** ≥ 95%
- **P95 Latency Target:** < 1500ms
- **Current Status:** {'✅ PASSED' if success_rate >= 95 and p95_latency < 1500 else '❌ FAILED'}

## 📋 Detailed Results

| Scenario ID | Type | Lang | Steps | Success | Avg Latency | Journey Pass |
|-------------|------|------|-------|---------|-------------|--------------|
"""
        
        for result in self.results:
            report_content += f"| {result['scenario_id']} | {result['type']} | {result['lang']} | {result['steps_count']} | {result['success_count']}/{result['steps_count']} | {result['avg_latency']:.0f}ms | {'✅' if result['journey_pass'] else '❌'} |\n"
        
        # Save report
        report_path = Path(__file__).parent.parent / report_file
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        log.info(f"📄 Report saved to: {report_path}")
        
        # Print summary
        log.info(f"\n🎯 HAMMER PRODUCTION TEST COMPLETE")
        log.info(f"📊 Success Rate: {success_rate:.1f}% ({passed_scenarios}/{total_scenarios})")
        log.info(f"⏱️  P95 Latency: {p95_latency:.0f}ms")
        log.info(f"🎯 Target Status: {'✅ PASSED' if success_rate >= 95 and p95_latency < 1500 else '❌ FAILED'}")

def main():
    parser = argparse.ArgumentParser(description="Sofia Lite Hammer Production Test Runner")
    parser.add_argument("--scenarios", default="scenarios_full.yaml", help="Scenarios YAML file")
    parser.add_argument("--report", default="docs/HAMMER_PROD_REPORT.md", help="Report output file")
    
    args = parser.parse_args()
    
    runner = HammerRunner()
    runner.run_all_scenarios(args.scenarios, args.report)

if __name__ == "__main__":
    main() 