#!/usr/bin/env python3
"""
HAMMER ULTIMATE – JOURNEY AUDIT VALIDATION ENGINE
Valida che Sofia percorra tutte le 9 tappe correttamente
"""

import json
import sys
import yaml
from typing import Dict, List, Any
from collections import defaultdict
import statistics

def load_journey_scenarios(scenarios_file: str) -> Dict[str, Any]:
    """Carica gli scenari journey dal file YAML"""
    try:
        with open(scenarios_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Errore caricamento scenari: {e}")
        sys.exit(1)

def load_hammer_results(results_file: str) -> Dict[str, Any]:
    """Carica i risultati Hammer dal file JSON"""
    try:
        with open(results_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Errore caricamento risultati: {e}")
        sys.exit(1)

def validate_journey_path(scenario: Dict, hammer_result: Dict) -> Dict[str, Any]:
    """Valida che il journey path segua la sequenza attesa"""
    
    validation = {
        "scenario_id": scenario.get("scenario_id", "unknown"),
        "language": scenario.get("language", "unknown"),
        "user_type": scenario.get("user_type", "unknown"),
        "channel": scenario.get("channel", "unknown"),
        "success": True,
        "mismatches": [],
        "expected_states": [],
        "actual_states": [],
        "details": []
    }
    
    # Estrai journey atteso
    expected_journey = scenario.get("journey", [])
    if not expected_journey:
        validation["success"] = False
        validation["mismatches"].append("No journey defined in scenario")
        return validation
    
    # Estrai risultati Hammer
    hammer_turns = hammer_result.get("turns", [])
    if not hammer_turns:
        validation["success"] = False
        validation["mismatches"].append("No turns found in Hammer result")
        return validation
    
    # Valida ogni turn
    for i, expected_turn in enumerate(expected_journey):
        expected_state = expected_turn.get("expect_state")
        validation["expected_states"].append(expected_state)
        
        if i >= len(hammer_turns):
            validation["success"] = False
            validation["mismatches"].append(f"Turn {i+1}: Missing in Hammer result")
            validation["actual_states"].append("MISSING")
            continue
        
        hammer_turn = hammer_turns[i]
        actual_state = hammer_turn.get("state", "UNKNOWN")
        validation["actual_states"].append(actual_state)
        
        if actual_state != expected_state:
            validation["success"] = False
            mismatch = {
                "turn": i + 1,
                "expected": expected_state,
                "actual": actual_state,
                "user_input": expected_turn.get("user_input", ""),
                "sofia_reply": hammer_turn.get("reply", ""),
                "lang_detected": hammer_turn.get("lang_detected", "unknown")
            }
            validation["mismatches"].append(mismatch)
            
            detail = f"Turn {i+1}: Expected '{expected_state}', got '{actual_state}'"
            validation["details"].append(detail)
    
    return validation

def analyze_results(validations: List[Dict]) -> Dict[str, Any]:
    """Analizza i risultati delle validazioni"""
    
    analysis = {
        "total_scenarios": len(validations),
        "successful_scenarios": sum(1 for v in validations if v["success"]),
        "failed_scenarios": sum(1 for v in validations if not v["success"]),
        "overall_success_rate": 0,
        "by_language": defaultdict(lambda: {"total": 0, "successful": 0, "failed": 0}),
        "by_step": defaultdict(lambda: {"total": 0, "successful": 0, "failed": 0}),
        "by_user_type": defaultdict(lambda: {"total": 0, "successful": 0, "failed": 0}),
        "by_channel": defaultdict(lambda: {"total": 0, "successful": 0, "failed": 0}),
        "failures": []
    }
    
    if validations:
        analysis["overall_success_rate"] = (analysis["successful_scenarios"] / analysis["total_scenarios"]) * 100
    
    # Analisi per lingua
    for validation in validations:
        lang = validation["language"]
        analysis["by_language"][lang]["total"] += 1
        if validation["success"]:
            analysis["by_language"][lang]["successful"] += 1
        else:
            analysis["by_language"][lang]["failed"] += 1
            analysis["failures"].append(validation)
    
    # Calcola success rate per lingua
    for lang in analysis["by_language"]:
        total = analysis["by_language"][lang]["total"]
        successful = analysis["by_language"][lang]["successful"]
        analysis["by_language"][lang]["success_rate"] = (successful / total * 100) if total > 0 else 0
    
    # Analisi per step (stato)
    for validation in validations:
        for i, expected_state in enumerate(validation["expected_states"]):
            analysis["by_step"][expected_state]["total"] += 1
            if i < len(validation["actual_states"]):
                actual_state = validation["actual_states"][i]
                if actual_state == expected_state:
                    analysis["by_step"][expected_state]["successful"] += 1
                else:
                    analysis["by_step"][expected_state]["failed"] += 1
    
    # Calcola success rate per step
    for step in analysis["by_step"]:
        total = analysis["by_step"][step]["total"]
        successful = analysis["by_step"][step]["successful"]
        analysis["by_step"][step]["success_rate"] = (successful / total * 100) if total > 0 else 0
    
    # Analisi per user type
    for validation in validations:
        user_type = validation["user_type"]
        analysis["by_user_type"][user_type]["total"] += 1
        if validation["success"]:
            analysis["by_user_type"][user_type]["successful"] += 1
        else:
            analysis["by_user_type"][user_type]["failed"] += 1
    
    # Analisi per channel
    for validation in validations:
        channel = validation["channel"]
        analysis["by_channel"][channel]["total"] += 1
        if validation["success"]:
            analysis["by_channel"][channel]["successful"] += 1
        else:
            analysis["by_channel"][channel]["failed"] += 1
    
    return analysis

def generate_report(analysis: Dict, output_file: str = None):
    """Genera il report finale"""
    
    report_lines = []
    report_lines.append("# HAMMER ULTIMATE – JOURNEY AUDIT REPORT")
    report_lines.append("")
    report_lines.append(f"**Timestamp**: {analysis.get('timestamp', 'N/A')}")
    report_lines.append(f"**Total Scenarios**: {analysis['total_scenarios']}")
    report_lines.append(f"**Successful**: {analysis['successful_scenarios']}")
    report_lines.append(f"**Failed**: {analysis['failed_scenarios']}")
    report_lines.append(f"**Overall Success Rate**: {analysis['overall_success_rate']:.1f}%")
    report_lines.append("")
    
    # Matrix lingua × step
    report_lines.append("## 📊 MATRIX LINGUA × STEP")
    report_lines.append("")
    
    # Header
    steps = ["GREETING", "ASK_NAME", "ASK_SERVICE", "PROPOSE_CONSULT", "ASK_CHANNEL", "ASK_SLOT", "ASK_PAYMENT", "CONFIRM_BOOKING", "ROUTE_ACTIVE"]
    header = "| Lingua | " + " | ".join(steps) + " |"
    report_lines.append(header)
    report_lines.append("|" + "---|" * (len(steps) + 1))
    
    # Rows per lingua
    for lang in sorted(analysis["by_language"].keys()):
        row = f"| {lang.upper()} |"
        for step in steps:
            if step in analysis["by_step"]:
                success_rate = analysis["by_step"][step]["success_rate"]
                status = "✅" if success_rate >= 95 else "❌"
                row += f" {success_rate:.0f}% {status} |"
            else:
                row += " N/A |"
        report_lines.append(row)
    
    report_lines.append("")
    
    # Summary per lingua
    report_lines.append("## 🌍 SUCCESS RATE PER LINGUA")
    report_lines.append("")
    for lang in sorted(analysis["by_language"].keys()):
        lang_data = analysis["by_language"][lang]
        success_rate = lang_data["success_rate"]
        status = "✅ PASS" if success_rate >= 95 else "❌ FAIL"
        report_lines.append(f"- **{lang.upper()}**: {success_rate:.1f}% ({lang_data['successful']}/{lang_data['total']}) {status}")
    
    report_lines.append("")
    
    # Summary per step
    report_lines.append("## 🎯 SUCCESS RATE PER STEP")
    report_lines.append("")
    for step in steps:
        if step in analysis["by_step"]:
            step_data = analysis["by_step"][step]
            success_rate = step_data["success_rate"]
            status = "✅ PASS" if success_rate >= 95 else "❌ FAIL"
            report_lines.append(f"- **{step}**: {success_rate:.1f}% ({step_data['successful']}/{step_data['total']}) {status}")
    
    report_lines.append("")
    
    # FAILURES
    if analysis["failures"]:
        report_lines.append("## ❌ FAILURES DETTAGLIATE")
        report_lines.append("")
        report_lines.append("| Scenario ID | Lingua | Mismatch | Dettagli |")
        report_lines.append("|-------------|--------|----------|----------|")
        
        for failure in analysis["failures"][:20]:  # Mostra solo i primi 20
            scenario_id = failure["scenario_id"]
            language = failure["language"]
            
            if failure["mismatches"]:
                mismatch = failure["mismatches"][0]
                details = f"Turn {mismatch['turn']}: Expected '{mismatch['expected']}', got '{mismatch['actual']}'"
                report_lines.append(f"| {scenario_id} | {language} | {mismatch['expected']} → {mismatch['actual']} | {details} |")
    
    report_lines.append("")
    
    # VERDETTO FINALE
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
        report_lines.append("## 🎉 VERDETTO FINALE: **GO** ✅")
        report_lines.append("")
        report_lines.append("Tutte le lingue e tutti gli step hanno raggiunto ≥ 95% di successo!")
    else:
        report_lines.append("## ❌ VERDETTO FINALE: **NO-GO** ❌")
        report_lines.append("")
        report_lines.append("Alcune lingue o step non hanno raggiunto il 95% di successo richiesto.")
    
    report_content = "\n".join(report_lines)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"📄 Report salvato in: {output_file}")
    
    return report_content

def main():
    """Funzione principale"""
    if len(sys.argv) != 2:
        print("❌ Uso: python journey_assert.py <hammer_results.json>")
        sys.exit(1)
    
    hammer_results_file = sys.argv[1]
    scenarios_file = "hammer/scenarios_journey.yaml"
    
    print("🔍 HAMMER ULTIMATE – JOURNEY AUDIT VALIDATION")
    print(f"📁 Hammer results: {hammer_results_file}")
    print(f"📁 Scenarios: {scenarios_file}")
    
    # Carica dati
    scenarios = load_journey_scenarios(scenarios_file)
    hammer_results = load_hammer_results(hammer_results_file)
    
    print(f"✅ Caricati {len(scenarios.get('scenarios', {}))} scenari")
    print(f"✅ Caricati {len(hammer_results.get('results', []))} risultati Hammer")
    
    # Estrai tutti gli scenari
    all_scenarios = []
    for category, category_scenarios in scenarios.get("scenarios", {}).items():
        if isinstance(category_scenarios, list):
            all_scenarios.extend(category_scenarios)
    
    print(f"📊 Totale scenari da validare: {len(all_scenarios)}")
    
    # Valida ogni scenario
    validations = []
    for scenario in all_scenarios:
        scenario_id = scenario.get("scenario_id")
        
        # Trova risultato corrispondente
        matching_result = None
        for result in hammer_results.get("results", []):
            if result.get("scenario_id") == scenario_id:
                matching_result = result
                break
        
        if matching_result:
            validation = validate_journey_path(scenario, matching_result)
            validations.append(validation)
        else:
            print(f"⚠️ Scenario {scenario_id} non trovato nei risultati Hammer")
    
    # Analizza risultati
    analysis = analyze_results(validations)
    analysis["timestamp"] = hammer_results.get("timestamp", "N/A")
    
    # Genera report
    report_content = generate_report(analysis, "docs/HAMMER_JOURNEY_REPORT.md")
    
    # Stampa summary
    print(f"\n📊 RISULTATI VALIDAZIONE:")
    print(f"   • Scenari totali: {analysis['total_scenarios']}")
    print(f"   • Successi: {analysis['successful_scenarios']}")
    print(f"   • Fallimenti: {analysis['failed_scenarios']}")
    print(f"   • Success rate: {analysis['overall_success_rate']:.1f}%")
    
    # Verdetto
    all_passed = True
    for lang_data in analysis["by_language"].values():
        if lang_data["success_rate"] < 95:
            all_passed = False
            break
    
    if all_passed:
        print(f"\n🎉 VERDETTO: **GO** ✅")
    else:
        print(f"\n❌ VERDETTO: **NO-GO** ❌")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main()) 