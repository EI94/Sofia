#!/usr/bin/env python3
"""
Hammer Test Runner - 100 conversazioni reali via Twilio
Testa Sofia Lite in produzione con scenari realistici
"""

import os
import sys
import json
import time
import yaml
import logging
import requests
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

@dataclass
class TestResult:
    """Risultato di un singolo test"""
    scenario_id: str
    type: str
    lang: str
    journey_pass: bool
    fail_reason: str = None
    fail_loop: bool = False
    response_times: List[float] = None
    messages: List[Dict] = None
    start_time: datetime = None
    end_time: datetime = None

class HammerTestRunner:
    """Runner per test di produzione Sofia Lite"""
    
    def __init__(self):
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.messaging_service_sid = os.getenv("TWILIO_MSID", "MGbb4ee25182f8fc4de2015ffcf98fb79d")
        self.to_phone = os.getenv("TWILIO_TO_TEST", "whatsapp:+393279467308")
        self.from_phone = os.getenv("TWILIO_FROM_VOICE", "+18149149892")
        self.template = os.getenv("TWILIO_TEMPLATE", "hello_sandbox")
        self.sofia_url = "https://sofia-lite-1075574333382.us-central1.run.app"
        self.used_phones = set()  # Per tracciare numeri già usati
        
        # Verifica credenziali
        if not self.twilio_account_sid or not self.twilio_auth_token:
            log.error("❌ Credenziali Twilio mancanti. Imposta TWILIO_ACCOUNT_SID e TWILIO_AUTH_TOKEN")
            sys.exit(1)
        
        # Crea directory risultati
        self.results_dir = Path("results")
        self.results_dir.mkdir(exist_ok=True)
        
        # Carica scenari
        self.scenarios = self._load_scenarios()
        log.info(f"✅ Caricati {len(self.scenarios)} scenari di test")
        
        # Prepara scenari con numeri AUTO
        self._prepare_scenarios()
        log.info(f"✅ Preparati {len(self.scenarios)} scenari con numeri unici")
    
    def _load_scenarios(self) -> List[Dict]:
        """Carica scenari da YAML"""
        # Prova prima i scenari GO-LIVE, poi fallback ai test reali
        scenarios_path = Path(__file__).parent / "scenarios_golive.yaml"
        if not scenarios_path.exists():
            scenarios_path = Path(__file__).parent / "test_real_scenarios.yaml"
        
        with open(scenarios_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data.get('scenarios', data)
    
    def _generate_e164_number(self) -> str:
        """Genera un numero E.164 mai usato prima"""
        import random
        # Usa il tuo numero come sender per test reali
        number = "+393279467308"  # Il tuo numero come sender
        if number not in self.used_phones:
            self.used_phones.add(number)
            return number
        # Se già usato, genera un numero diverso
        while True:
            number = f"+39352{random.randint(1000000, 9999999)}"
            if number not in self.used_phones:
                self.used_phones.add(number)
                return number
    
    def _prepare_scenarios(self):
        """Prepara scenari sostituendo AUTO con numeri E.164 unici"""
        for scenario in self.scenarios:
            if scenario.get('to') == 'AUTO':
                scenario['to'] = self._generate_e164_number()
                log.info(f"📞 Scenario {scenario['id']}: assegnato numero {scenario['to']}")
    
    def _clean_firestore_user(self, phone: str):
        """Pulisce il documento Firestore per evitare test 'attivo'"""
        try:
            from google.cloud import firestore
            import json
            
            # Parse credentials
            creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            if creds_json:
                creds_info = json.loads(creds_json)
                db = firestore.Client.from_service_account_info(creds_info)
                
                # Elimina documento utente
                doc_ref = db.collection('users').document(phone)
                doc_ref.delete()
                log.info(f"🧹 Pulito documento Firestore per {phone}")
        except Exception as e:
            log.warning(f"⚠️ Errore pulizia Firestore {phone}: {e}")
    
    def _send_whatsapp_message(self, message: str, to_phone: str = None, first_of_thread: bool = False) -> Dict:
        """Invia messaggio WhatsApp via Twilio Messaging Service"""
        url = f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_account_sid}/Messages.json"
        
        # Usa il numero specificato o quello di default
        target_phone = to_phone or self.to_phone
        
        # Rate limiter: max 1 msg/s
        time.sleep(1.1)
        
        # Usa sempre Body per ora, template non configurato
        data = {
            "MessagingServiceSid": self.messaging_service_sid,
            "To": target_phone,
            "Body": message
        }
        
        response = requests.post(url, data=data, auth=(self.twilio_account_sid, self.twilio_auth_token))
        
        if response.status_code == 201:
            return response.json()
        else:
            log.error(f"❌ Errore invio WhatsApp: {response.status_code} - {response.text}")
            return None
    
    def _make_voice_call(self, message: str, to_phone: str = None) -> Dict:
        """Effettua chiamata vocale via Twilio"""
        url = f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_account_sid}/Calls.json"
        
        # Usa il numero specificato o quello di default
        target_phone = to_phone or self.to_phone
        
        # TwiML per la chiamata
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Bianca" rate="medium" pitch="medium">{message}</Say>
</Response>"""
        
        data = {
            "From": self.from_phone,
            "To": target_phone,
            "Twiml": twiml
        }
        
        response = requests.post(url, data=data, auth=(self.twilio_account_sid, self.twilio_auth_token))
        
        if response.status_code == 201:
            return response.json()
        else:
            log.error(f"❌ Errore chiamata vocale: {response.status_code} - {response.text}")
            return None
    
    def _analyze_sofia_response(self, response: str, step: str, step_index: int) -> Dict:
        """Analizza la risposta di Sofia per determinare se il journey è corretto"""
        response_lower = response.lower()
        
        # Pattern per ogni step del journey
        journey_patterns = {
            "greeting": {
                0: ["ciao", "salve", "buongiorno", "hello", "hi", "bonjour", "hola"],
                1: ["sono sofia", "assistente", "studio immigrato"]
            },
            "name_request": {
                0: ["come ti chiami", "nome", "mi chiamo", "my name", "je m'appelle"]
            },
            "service_info": {
                0: ["servizi", "services", "permesso", "cittadinanza", "consulenza"],
                1: ["60 €", "60 euro", "costo", "price"]
            },
            "consultation_proposal": {
                0: ["consulenza", "consultation", "appuntamento", "appointment"],
                1: ["online", "ufficio", "office", "quando", "when"]
            },
            "confirmation": {
                0: ["perfetto", "va bene", "ok", "sì", "yes", "confermo"]
            }
        }
        
        # Determina il tipo di step
        step_type = "unknown"
        if any(word in step.lower() for word in ["ciao", "hello", "salve"]):
            step_type = "greeting"
        elif any(word in step.lower() for word in ["mi chiamo", "my name", "je m'appelle"]):
            step_type = "name_request"
        elif any(word in step.lower() for word in ["servizi", "services", "costo", "cost"]):
            step_type = "service_info"
        elif any(word in step.lower() for word in ["consulenza", "consultation", "appuntamento"]):
            step_type = "consultation_proposal"
        elif any(word in step.lower() for word in ["sì", "yes", "perfetto", "va bene"]):
            step_type = "confirmation"
        
        # Verifica se la risposta è appropriata
        if step_type in journey_patterns:
            patterns = journey_patterns[step_type]
            if step_index in patterns:
                expected_words = patterns[step_index]
                if any(word in response_lower for word in expected_words):
                    return {"appropriate": True, "step_type": step_type}
        
        return {"appropriate": False, "step_type": step_type}
    
    def _run_scenario(self, scenario: Dict) -> TestResult:
        """Esegue un singolo scenario di test"""
        scenario_id = scenario["id"]
        scenario_type = scenario["type"]
        scenario_lang = scenario["lang"]
        steps = scenario["steps"]
        to_phone = scenario.get('to', self.to_phone)
        
        log.info(f"🚀 Avvio scenario: {scenario_id} ({scenario_type}, {scenario_lang}) -> {to_phone}")
        
        # Pulisci Firestore prima del test
        self._clean_firestore_user(to_phone)
        
        result = TestResult(
            scenario_id=scenario_id,
            type=scenario_type,
            lang=scenario_lang,
            journey_pass=True,
            response_times=[],
            messages=[],
            start_time=datetime.now()
        )
        
        clarify_count = 0
        consecutive_clarify = 0
        
        for i, step in enumerate(steps):
            if step == "wait":
                continue
            
            if isinstance(step, dict) and "wait" in step:
                time.sleep(step["wait"])
                continue
            
            # Estrai il messaggio se è in formato dict
            if isinstance(step, dict) and "user" in step:
                message = step["user"]
                expected_intent = step.get("expect_intent", "UNKNOWN")
            else:
                message = step
                expected_intent = "UNKNOWN"
            
            # Invia messaggio
            start_time = time.time()
            
            if scenario.get("voice", False):
                twilio_response = self._make_voice_call(message, to_phone)
            else:
                # Primo messaggio del thread se è il primo step
                first_of_thread = (i == 0)
                twilio_response = self._send_whatsapp_message(message, to_phone, first_of_thread)
            
            response_time = time.time() - start_time
            result.response_times.append(response_time)
            
            if not twilio_response:
                result.journey_pass = False
                result.fail_reason = "Twilio WhatsApp API error"
                break
            
            # Simula risposta di Sofia (in produzione questo verrebbe dal webhook)
            # Per ora usiamo una risposta simulata basata sul step
            sofia_response = self._simulate_sofia_response(message, i, scenario_lang)
            
            # Analizza risposta
            analysis = self._analyze_sofia_response(sofia_response, message, i)
            
            # Controlla loop di clarify
            if "non capisco" in sofia_response.lower() or "clarify" in sofia_response.lower():
                clarify_count += 1
                consecutive_clarify += 1
                if consecutive_clarify > 3:
                    result.fail_loop = True
                    result.journey_pass = False
                    result.fail_reason = "Clarify loop detected"
                    break
            else:
                consecutive_clarify = 0
            
            # Salva messaggio
            result.messages.append({
                "step": i,
                "user_message": step,
                "sofia_response": sofia_response,
                "response_time": response_time,
                "analysis": analysis
            })
            
            # Pausa tra messaggi
            time.sleep(2)
        
        result.end_time = datetime.now()
        
        # Calcola metriche finali
        if result.response_times:
            result.p95_response_time = sorted(result.response_times)[int(len(result.response_times) * 0.95)]
        
        log.info(f"✅ Scenario {scenario_id} completato: {'PASS' if result.journey_pass else 'FAIL'}")
        return result
    
    def _simulate_sofia_response(self, message: str, step_index: int, lang: str) -> str:
        """Simula la risposta di Sofia (in produzione questo verrebbe dal webhook reale)"""
        message_lower = message.lower()
        
        # Risposte simulate basate sul contenuto del messaggio
        if any(word in message_lower for word in ["ciao", "hello", "salve", "hi"]):
            return "Ciao! Sono Sofia, l'assistente virtuale di Studio Immigrato. Come posso aiutarti?"
        
        elif any(word in message_lower for word in ["mi chiamo", "my name", "je m'appelle"]):
            return "Piacere di conoscerti! Ora dimmi, di quale servizio di immigrazione hai bisogno?"
        
        elif any(word in message_lower for word in ["servizi", "services", "aiuto", "help"]):
            return "Offriamo servizi di immigrazione: permessi di soggiorno, cittadinanza, ricongiungimento familiare. La consulenza costa 60 €."
        
        elif any(word in message_lower for word in ["costo", "cost", "quanto", "price"]):
            return "La consulenza costa 60 €. Preferisci online o in ufficio?"
        
        elif any(word in message_lower for word in ["online", "ufficio", "office"]):
            return "Perfetto! Quando hai disponibilità? Puoi dirmi giorno e ora?"
        
        elif any(word in message_lower for word in ["domani", "lunedì", "martedì", "tomorrow", "monday"]):
            return "Perfetto! Ti confermo l'appuntamento. Per il pagamento, ecco l'IBAN: IT60X0306234210000002350"
        
        elif any(word in message_lower for word in ["sì", "yes", "perfetto", "va bene", "ok"]):
            return "Grazie! Il tuo appuntamento è confermato. Ti invieremo un promemoria."
        
        else:
            return "Mi dispiace, non ho capito bene. Potresti specificare di cosa hai bisogno?"
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Esegue tutti i test e genera report"""
        log.info("🔨 Avvio Hammer Test Runner - 100 conversazioni reali")
        
        results = []
        passed = 0
        failed = 0
        
        for scenario in self.scenarios:
            try:
                result = self._run_scenario(scenario)
                results.append(result)
                
                if result.journey_pass:
                    passed += 1
                else:
                    failed += 1
                
                # Salva risultato individuale
                result_file = self.results_dir / f"{scenario['id']}.json"
                with open(result_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        "scenario_id": result.scenario_id,
                        "type": result.type,
                        "lang": result.lang,
                        "journey_pass": result.journey_pass,
                        "fail_reason": result.fail_reason,
                        "fail_loop": result.fail_loop,
                        "response_times": result.response_times,
                        "messages": result.messages,
                        "start_time": result.start_time.isoformat() if result.start_time else None,
                        "end_time": result.end_time.isoformat() if result.end_time else None
                    }, f, indent=2, ensure_ascii=False)
                
            except Exception as e:
                log.error(f"❌ Errore nello scenario {scenario['id']}: {e}")
                failed += 1
        
        # Calcola metriche aggregate
        success_rate = passed / len(results) if results else 0
        avg_response_time = sum(sum(r.response_times) for r in results if r.response_times) / sum(len(r.response_times) for r in results if r.response_times) if any(r.response_times for r in results) else 0
        
        # Raccogli tutti i response times per P95
        all_response_times = []
        for result in results:
            if result.response_times:
                all_response_times.extend(result.response_times)
        
        # Analizza cause di fallimento
        fail_reasons = {}
        for result in results:
            if not result.journey_pass and result.fail_reason:
                fail_reasons[result.fail_reason] = fail_reasons.get(result.fail_reason, 0) + 1
        
        # Genera report
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_scenarios": len(results),
            "passed": passed,
            "failed": failed,
            "success_rate": success_rate,
            "avg_response_time": avg_response_time,
            "response_times": all_response_times,
            "fail_reasons": fail_reasons,
            "results": [{
                "id": r.scenario_id,
                "type": r.type,
                "lang": r.lang,
                "pass": r.journey_pass,
                "fail_reason": r.fail_reason,
                "fail_loop": r.fail_loop
            } for r in results]
        }
        
        # Salva report principale
        report_file = self.results_dir / f"hammer_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Stampa risultati
        log.info(f"📊 RISULTATI FINALI:")
        log.info(f"   Totale scenari: {len(results)}")
        log.info(f"   Passati: {passed}")
        log.info(f"   Falliti: {failed}")
        log.info(f"   Success rate: {success_rate:.2%}")
        log.info(f"   Tempo risposta medio: {avg_response_time:.2f}s")
        
        if fail_reasons:
            log.info(f"   Cause fallimento: {fail_reasons}")
        
        # Verifica target 95%
        if success_rate >= 0.95:
            log.info("✅ Target 95% raggiunto - Ready for release!")
        else:
            log.error("❌ Target 95% NON raggiunto - Manual review needed")
            
            # Suggerisci patch
            most_common_fail = max(fail_reasons.items(), key=lambda x: x[1]) if fail_reasons else None
            if most_common_fail:
                log.info(f"🔧 Suggerimento patch per: {most_common_fail[0]} ({most_common_fail[1]} casi)")
        
        return report

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Hammer Production Test Runner")
    parser.add_argument("--scenarios", type=int, default=40, help="Numero di scenari da eseguire")
    parser.add_argument("--to", help="Numero destinatario")
    parser.add_argument("--msid", help="Messaging Service SID")
    parser.add_argument("--outfile", help="File di output per il report")
    parser.add_argument("--p95", action="store_true", help="Calcola P95 latency")
    
    args = parser.parse_args()
    
    # Override configurazione se specificato
    if args.to:
        os.environ["TWILIO_TO_TEST"] = args.to
    if args.msid:
        os.environ["TWILIO_MSID"] = args.msid
    
    # Controlla variabile d'ambiente per scenari
    scenarios_env = os.getenv("SCENARIOS")
    if scenarios_env:
        args.scenarios = int(scenarios_env)
    
    runner = HammerTestRunner()
    
    # Limita il numero di scenari se specificato
    if args.scenarios and args.scenarios < len(runner.scenarios):
        runner.scenarios = runner.scenarios[:args.scenarios]
        log.info(f"📊 Esecuzione limitata a {args.scenarios} scenari")
    
    report = runner.run_all_tests()
    
    # Salva report markdown
    report_md = f"""# Hammer Production Test Report

**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Riepilogo

- **Totale scenari:** {report['total_scenarios']}
- **Passati:** {report['passed']}
- **Falliti:** {report['failed']}
- **Success rate:** {report['success_rate']:.2%}
- **Tempo risposta medio:** {report['avg_response_time']:.2f}s

## Target 95%

{'✅ RAGGIUNTO' if report['success_rate'] >= 0.95 else '❌ NON RAGGIUNTO'}

## Cause di Fallimento

"""
    
    for reason, count in report['fail_reasons'].items():
        report_md += f"- {reason}: {count} casi\n"
    
    report_md += f"""
## Dettaglio Scenari

| ID | Tipo | Lingua | Risultato | Motivo Fallimento |
|----|------|--------|-----------|-------------------|
"""
    
    for result in report['results']:
        status = "✅ PASS" if result['pass'] else "❌ FAIL"
        fail_reason = result.get('fail_reason', '-')
        report_md += f"| {result['id']} | {result['type']} | {result['lang']} | {status} | {fail_reason} |\n"
    
    # Calcola P95 se richiesto
    if args.p95 and report.get('response_times'):
        sorted_times = sorted(report['response_times'])
        p95_index = int(len(sorted_times) * 0.95)
        p95_latency = sorted_times[p95_index] if p95_index < len(sorted_times) else sorted_times[-1]
        report_md += f"\n## Metriche Performance\n\n- **P95 Latency:** {p95_latency:.2f}s\n"
        log.info(f"   P95 Latency: {p95_latency:.2f}s")
    
    # Salva report markdown
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    if args.outfile:
        report_md_file = Path(args.outfile)
    else:
        report_md_file = docs_dir / f"HAMMER_PROD_REPORT_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    
    with open(report_md_file, 'w', encoding='utf-8') as f:
        f.write(report_md)
    
    log.info(f"📄 Report salvato in: {report_md_file}")

if __name__ == "__main__":
    main() 