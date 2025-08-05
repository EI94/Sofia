#!/usr/bin/env python3
"""
Sofia Lite - End-to-End Test Runner
Tests complete user journeys with Firestore emulator.
"""

import os
import sys
import time
import logging
from typing import List, Dict, Any
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sofia_lite.agents.state import State
from sofia_lite.agents.context import Context
from sofia_lite.handlers.common import handle_incoming

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Supported languages for testing
SUPPORTED_LANGS = ["it", "en", "fr", "es", "ar", "hi", "ur", "bn"]

class Scenario:
    """Represents a complete user journey scenario."""
    
    def __init__(self, lang: str, client_type: str = "new"):
        self.lang = lang
        self.client_type = client_type
        self.phone = f"+39300{lang}123456"
        self.messages = []
        self.responses = []
        self.final_state = None
        self.success = False
        
    def run_workflow(self) -> bool:
        """Execute the complete workflow for this scenario."""
        try:
            logger.info(f"🚀 Starting {self.lang} scenario for {self.client_type} client")
            
            # Step 1: Greeting
            self._send_message("ciao" if self.lang == "it" else "hello")
            if not self._check_response_contains("Sofia"):
                return False
            
            # Step 2: Provide name
            self._send_message("Mi chiamo Pierpaolo" if self.lang == "it" else "My name is Pierpaolo")
            if not self._check_response_contains("Piacere"):
                return False
            
            # Step 3: Request service
            self._send_message("Ho bisogno del permesso di soggiorno" if self.lang == "it" else "I need a residence permit")
            if not self._check_response_contains("60"):
                return False
            
            # Step 4: Confirm consultation
            self._send_message("Sì, va bene" if self.lang == "it" else "Yes, that's fine")
            if not self._check_response_contains("online") or not self._check_response_contains("presenza"):
                return False
            
            # Step 5: Choose online
            self._send_message("Online" if self.lang == "it" else "Online")
            if not self._check_response_contains("IBAN"):
                return False
            
            # Step 6: Confirm payment
            self._send_message("Perfetto, confermo" if self.lang == "it" else "Perfect, I confirm")
            
            # Check final state
            self.final_state = self._get_current_state()
            self.success = self.final_state == State.CONFIRMED
            
            logger.info(f"✅ {self.lang} scenario completed: {self.final_state}")
            return self.success
            
        except Exception as e:
            logger.error(f"❌ {self.lang} scenario failed: {e}")
            return False
    
    def _send_message(self, message: str) -> Dict[str, Any]:
        """Send a message and get response."""
        self.messages.append(message)
        
        try:
            # Use common handler
            result = handle_incoming(self.phone, message, "whatsapp")
            self.responses.append(result["reply"])
            
            logger.info(f"📤 {self.lang}: {message}")
            logger.info(f"📥 {self.lang}: {result['reply'][:50]}...")
            
            return result
        except Exception as e:
            logger.error(f"❌ Error sending message: {e}")
            return {"reply": "", "state": "ERROR"}
    
    def _check_response_contains(self, text: str) -> bool:
        """Check if last response contains specific text."""
        if not self.responses:
            return False
        return text.lower() in self.responses[-1].lower()
    
    def _get_current_state(self) -> State:
        """Get current conversation state."""
        try:
            from sofia_lite.middleware.memory import load_context
            ctx = load_context(self.phone)
            if ctx:
                return State(ctx.state) if hasattr(State, ctx.state) else State.ASK_CLARIFICATION
        except Exception as e:
            logger.warning(f"Could not get current state: {e}")
        
        return State.ASK_CLARIFICATION

def run_language_scenarios() -> Dict[str, bool]:
    """Run scenarios for all supported languages."""
    results = {}
    
    logger.info("🌍 Running E2E scenarios for all supported languages")
    logger.info("=" * 60)
    
    for lang in SUPPORTED_LANGS:
        logger.info(f"\n🧪 Testing language: {lang}")
        
        # Test new client scenario
        scenario = Scenario(lang, "new")
        success = scenario.run_workflow()
        results[lang] = success
        
        if success:
            logger.info(f"✅ {lang}: PASSED (final state: {scenario.final_state})")
        else:
            logger.error(f"❌ {lang}: FAILED (final state: {scenario.final_state})")
        
        # Small delay between tests
        time.sleep(1)
    
    return results

def run_edge_case_scenarios() -> Dict[str, bool]:
    """Run edge case scenarios."""
    results = {}
    
    logger.info("\n🔍 Running edge case scenarios")
    logger.info("=" * 60)
    
    # Test 1: Abusive content
    logger.info("\n🧪 Test: Abusive content")
    scenario = Scenario("it", "new")
    scenario._send_message("vaffanculo")
    results["abuse"] = "policy" in scenario.responses[-1].lower()
    logger.info(f"{'✅' if results['abuse'] else '❌'} Abuse handling: {'PASSED' if results['abuse'] else 'FAILED'}")
    
    # Test 2: Unknown language
    logger.info("\n🧪 Test: Unknown language")
    scenario = Scenario("xx", "new")
    scenario._send_message("xyz")
    results["unknown_lang"] = "language" in scenario.responses[-1].lower() or "lingua" in scenario.responses[-1].lower()
    logger.info(f"{'✅' if results['unknown_lang'] else '❌'} Unknown language: {'PASSED' if results['unknown_lang'] else 'FAILED'}")
    
    # Test 3: Very long message
    logger.info("\n🧪 Test: Very long message")
    long_message = "ciao " * 100
    scenario = Scenario("it", "new")
    scenario._send_message(long_message)
    results["long_message"] = len(scenario.responses[-1]) > 0
    logger.info(f"{'✅' if results['long_message'] else '❌'} Long message: {'PASSED' if results['long_message'] else 'FAILED'}")
    
    return results

def run_performance_tests() -> Dict[str, float]:
    """Run performance tests."""
    results = {}
    
    logger.info("\n⚡ Running performance tests")
    logger.info("=" * 60)
    
    # Test response time
    start_time = time.time()
    scenario = Scenario("it", "new")
    scenario._send_message("ciao")
    response_time = time.time() - start_time
    results["response_time"] = response_time
    
    logger.info(f"⏱️ Response time: {response_time:.2f}s")
    
    # Test memory usage
    import psutil
    process = psutil.Process()
    memory_usage = process.memory_info().rss / 1024 / 1024  # MB
    results["memory_usage"] = memory_usage
    
    logger.info(f"💾 Memory usage: {memory_usage:.2f} MB")
    
    return results

def generate_report(lang_results: Dict[str, bool], edge_results: Dict[str, bool], perf_results: Dict[str, float]) -> str:
    """Generate test report."""
    report = []
    report.append("# Sofia Lite - E2E Test Report")
    report.append("")
    report.append(f"**Test Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Language results
    report.append("## Language Scenarios")
    passed_langs = sum(1 for success in lang_results.values() if success)
    total_langs = len(lang_results)
    
    report.append(f"**Results:** {passed_langs}/{total_langs} languages passed")
    report.append("")
    
    for lang, success in lang_results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        report.append(f"- {lang.upper()}: {status}")
    
    report.append("")
    
    # Edge case results
    report.append("## Edge Cases")
    passed_edge = sum(1 for success in edge_results.values() if success)
    total_edge = len(edge_results)
    
    report.append(f"**Results:** {passed_edge}/{total_edge} edge cases passed")
    report.append("")
    
    for test, success in edge_results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        report.append(f"- {test}: {status}")
    
    report.append("")
    
    # Performance results
    report.append("## Performance")
    report.append(f"- Response Time: {perf_results.get('response_time', 0):.2f}s")
    report.append(f"- Memory Usage: {perf_results.get('memory_usage', 0):.2f} MB")
    
    # Overall status
    overall_success = passed_langs == total_langs and passed_edge == total_edge
    report.append("")
    report.append(f"## Overall Status: {'✅ PASSED' if overall_success else '❌ FAILED'}")
    
    return "\n".join(report)

def main():
    """Main test runner."""
    logger.info("🚀 Sofia Lite - E2E Test Runner")
    logger.info("=" * 60)
    
    # Check if Firestore emulator is running
    emulator_host = os.getenv("FIRESTORE_EMULATOR_HOST")
    if not emulator_host:
        logger.warning("⚠️ FIRESTORE_EMULATOR_HOST not set. Tests may fail.")
    else:
        logger.info(f"✅ Firestore emulator detected: {emulator_host}")
    
    try:
        # Run language scenarios
        lang_results = run_language_scenarios()
        
        # Run edge case scenarios
        edge_results = run_edge_case_scenarios()
        
        # Run performance tests
        perf_results = run_performance_tests()
        
        # Generate report
        report = generate_report(lang_results, edge_results, perf_results)
        
        # Save report
        report_path = "e2e_test_report.md"
        with open(report_path, "w") as f:
            f.write(report)
        
        logger.info(f"📄 Report saved to: {report_path}")
        
        # Print summary
        passed_langs = sum(1 for success in lang_results.values() if success)
        total_langs = len(lang_results)
        passed_edge = sum(1 for success in edge_results.values() if success)
        total_edge = len(edge_results)
        
        logger.info("\n" + "=" * 60)
        logger.info("📊 TEST SUMMARY")
        logger.info(f"Languages: {passed_langs}/{total_langs} passed")
        logger.info(f"Edge Cases: {passed_edge}/{total_edge} passed")
        logger.info(f"Response Time: {perf_results.get('response_time', 0):.2f}s")
        logger.info("=" * 60)
        
        # Exit with appropriate code
        overall_success = passed_langs == total_langs and passed_edge == total_edge
        if overall_success:
            logger.info("🎉 ALL TESTS PASSED!")
            sys.exit(0)
        else:
            logger.error("❌ SOME TESTS FAILED!")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"❌ Test runner failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 