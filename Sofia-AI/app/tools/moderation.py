from openai import OpenAI
from functools import lru_cache
from dotenv import load_dotenv
import os
import logging
from typing import Optional, Tuple, Dict, Any
from twilio.twiml.voice_response import VoiceResponse
from datetime import datetime, timedelta
from app.tools.journey_analytics import track_journey_event, EventType, JourneyStage, Channel as JourneyChannel, generate_session_id

logger = logging.getLogger(__name__)

load_dotenv()

# Inizializzazione client con timeout specifici
try:
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        timeout=10.0,  # Timeout di 10 secondi
        max_retries=2  # Massimo 2 retry
    )
    logger.info("✅ OpenAI client inizializzato per moderazione")
except Exception as e:
    logger.error(f"❌ Errore inizializzazione OpenAI client: {e}")
    client = None

# Solo categorie veramente problematiche, non semplice frustrazione
SERIOUS_ABUSE_CATEGORIES = {"hate", "violence"}

@lru_cache(maxsize=1024)
def _cached_moderation(text: str):
    """Moderazione cached con gestione errori robusta"""
    if not client:
        raise Exception("OpenAI client non disponibile")
    return client.moderations.create(model="text-moderation-latest", input=text)

def _keyword_moderation(text: str) -> bool:
    """Fallback moderazione basata su parole chiave per casi estremi"""
    text_lower = text.lower()
    
    # Solo parole veramente gravi
    extreme_hate_words = [
        "ammazzat", "crepa", "suicidat", "terrorist", "bomb", "kill yourself", 
        "murder", "shoot", "nazi", "fascist", "die"
    ]
    
    return any(word in text_lower for word in extreme_hate_words)

async def is_abusive(text: str) -> bool:
    """
    Moderazione ULTRA PERMISSIVA - blocca SOLO hate speech e violenza estrema,
    permette TUTTO il resto inclusi servizi immigrazione
    """
    if not text or not text.strip():
        return False
    
    # 🚨 WHITELIST SERVIZI IMMIGRAZIONE - MAI BLOCCARE
    immigration_services = [
        "protezione", "internazionale", "asilo", "rifugiato", "permesso", "soggiorno",
        "ricongiungimento", "familiare", "cittadinanza", "italiana", "questura",
        "prefettura", "ambasciata", "consolato", "nulla osta", "kit", "domanda",
        "ricorso", "tribunale", "tar", "commissione", "sanatoria", "decreto flussi",
        "corso", "lingua", "a2", "b1", "formazione", "codice fiscale", "tessera sanitaria",
        "residenza", "anagrafica", "idoneità", "alloggiativa", "traduzione", "apostille",
        "legalizzazione", "denuncia", "datore", "lavoro", "sfruttamento", "crediti",
        "separazione", "divorzio", "successione", "contratto", "locazione", "sinistro",
        "stradale", "spid", "cie", "firma", "digitale", "conversione", "stagionale",
        "subordinato", "art. 31", "t.u.", "immigrazione", "minori", "genitori",
        "studio", "immigrato", "consulenza", "appuntamento", "booking", "servizi",
        "aiuto", "assistenza", "pratiche", "documenti", "moduli", "istanze"
    ]
    
    text_lower = text.lower()
    
    # Se contiene servizi immigrazione, MAI bloccare
    if any(service in text_lower for service in immigration_services):
        logger.info(f"✅ Servizio immigrazione permesso: {text[:50]}...")
        return False
    
    # Se contiene parole comuni di conversazione, MAI bloccare
    conversation_words = [
        "ciao", "hello", "hola", "bonjour", "grazie", "thanks", "merci", "gracias",
        "prego", "you're welcome", "de rien", "de nada", "come", "how", "comment",
        "como", "cosa", "what", "que", "qu'est-ce", "aiuto", "help", "ayuda", "aide",
        "servizi", "services", "servicios", "services", "consulenza", "consultation",
        "consulta", "consultation", "appuntamento", "appointment", "rendez-vous", "cita",
        "online", "presenza", "person", "office", "ufficio", "studio", "milan", "milano"
    ]
    
    if any(word in text_lower for word in conversation_words):
        logger.info(f"✅ Parola conversazione permessa: {text[:50]}...")
        return False
    
    try:
        resp = _cached_moderation(text)
        flags = {k for k, v in resp.results[0].categories.model_dump().items() if v}
        
        # Blocca SOLO categorie estreme
        serious_flags = flags & SERIOUS_ABUSE_CATEGORIES
        
        # Se è solo harassment/sexual senza hate/violence, MAI bloccare
        if "harassment" in flags and not serious_flags:
            logger.info(f"✅ Harassment leggero permesso: {text[:50]}...")
            return False
        
        # Se è sexual senza hate/violence, MAI bloccare
        if "sexual" in flags and not serious_flags:
            logger.info(f"✅ Contenuto sexual leggero permesso: {text[:50]}...")
            return False
        
        # Blocca SOLO se è veramente grave
        if serious_flags:
            logger.warning(f"🚨 Contenuto moderato (AI): {serious_flags} per testo: {text[:50]}...")
            
        return bool(serious_flags)
        
    except Exception as e:
        logger.error(f"❌ Errore moderazione OpenAI: {e}")
        # Fallback alla moderazione keyword solo per casi estremi
        return _keyword_moderation(text)

# Cache per tracking violazioni per utente (in-memory per semplicità)
user_violations: Dict[str, Dict[str, Any]] = {}

# Configurazione moderazione Voice
VOICE_MODERATION_CONFIG = {
    "max_warnings": 2,  # Massimo 2 warning prima del ban
    "warning_timeout": 300,  # 5 minuti timeout dopo warning
    "violation_expiry": 3600,  # 1 ora per reset violazioni  
    "immediate_ban_categories": {"hate", "violence", "self-harm"},
    "warning_categories": {"harassment", "sexual"}
}


async def check_voice_content(speech_text: str, user_id: str, call_sid: str = "") -> Tuple[bool, str, VoiceResponse]:
    """
    Controllo moderazione completo per contenuto Voice con azioni graduate
    
    Args:
        speech_text: Testo trascritto dal parlato
        user_id: ID utente (numero telefono)
        call_sid: Call SID per tracking
        
    Returns:
        Tuple: (is_blocked, violation_reason, twiml_response)
    """
    
    if not speech_text or not speech_text.strip():
        return False, "", VoiceResponse()
    
    try:
        # 1. Controllo standard moderazione
        is_abuse = await is_abusive(speech_text)
        
        if not is_abuse:
            # Contenuto OK - pulisci warning se presenti
            if user_id in user_violations:
                user_violations[user_id]["last_clean_interaction"] = datetime.now()
            return False, "", VoiceResponse()
        
        # 2. Contenuto problematico - analisi dettagliata
        violation_details = await _analyze_voice_violation(speech_text, user_id)
        
        # 3. Gestione escalation graduata
        action = _determine_voice_moderation_action(user_id, violation_details)
        
        # 4. Genera TwiML response appropriata
        twiml_response = _create_voice_moderation_response(action, violation_details)
        
        # 5. Tracking per analytics
        await _track_voice_moderation_event(user_id, call_sid, violation_details, action)
        
        # 6. Aggiorna violazioni utente
        _update_user_violations(user_id, violation_details, action)
        
        logger.warning(f"🚨 Voice moderation: {action['type']} for user {user_id} - {violation_details['category']}")
        
        return action["block_interaction"], violation_details["category"], twiml_response
        
    except Exception as e:
        logger.error(f"❌ Errore moderazione Voice: {e}")
        return False, "", VoiceResponse()


async def _analyze_voice_violation(speech_text: str, user_id: str) -> Dict[str, Any]:
    """
    Analisi dettagliata violazione Voice con classificazione
    """
    try:
        # Usa moderazione OpenAI per classificazione dettagliata
        resp = _cached_moderation(speech_text)
        moderation_result = resp.results[0]
        
        # Identifica categoria principale violazione
        categories = moderation_result.categories.model_dump()
        violated_categories = [k for k, v in categories.items() if v]
        
        # Severity scores per prioritizzazione
        category_scores = moderation_result.category_scores.model_dump()
        max_score_category = max(category_scores.items(), key=lambda x: x[1])
        
        violation_details = {
            "text": speech_text[:100] + "..." if len(speech_text) > 100 else speech_text,
            "categories": violated_categories,
            "primary_category": max_score_category[0] if max_score_category[1] > 0.5 else "unknown",
            "confidence_score": max_score_category[1],
            "severity": "high" if max_score_category[1] > 0.8 else "medium" if max_score_category[1] > 0.5 else "low",
            "timestamp": datetime.now(),
            "user_history": user_violations.get(user_id, {})
        }
        
        return violation_details
        
    except Exception as e:
        logger.error(f"❌ Errore analisi violazione Voice: {e}")
        return {
            "text": speech_text[:100],
            "categories": ["unknown"],
            "primary_category": "unknown",
            "confidence_score": 0.7,
            "severity": "medium",
            "timestamp": datetime.now(),
            "user_history": {}
        }


def _determine_voice_moderation_action(user_id: str, violation_details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Determina azione moderazione basata su cronologia utente e severità
    """
    
    # Ottieni cronologia violazioni utente
    user_history = user_violations.get(user_id, {})
    previous_violations = user_history.get("violation_count", 0)
    last_warning = user_history.get("last_warning_time")
    
    primary_category = violation_details["primary_category"]
    severity = violation_details["severity"]
    
    # IMMEDIATE BAN per categorie gravi
    if primary_category in VOICE_MODERATION_CONFIG["immediate_ban_categories"] or severity == "high":
        return {
            "type": "immediate_ban",
            "message": "terminate_call_abuse", 
            "block_interaction": True,
            "escalation_level": 3
        }
    
    # WARNING SYSTEM graduato
    if previous_violations == 0:
        # Prima violazione - warning educato
        return {
            "type": "first_warning",
            "message": "polite_warning",
            "block_interaction": False,
            "escalation_level": 1
        }
    
    elif previous_violations == 1:
        # Seconda violazione - warning severo
        return {
            "type": "second_warning", 
            "message": "stern_warning",
            "block_interaction": False,
            "escalation_level": 2
        }
    
    else:
        # Terza violazione - ban temporaneo
        return {
            "type": "temporary_ban",
            "message": "terminate_call_repeated",
            "block_interaction": True,
            "escalation_level": 3
        }


def _create_voice_moderation_response(action: Dict[str, Any], violation_details: Dict[str, Any]) -> VoiceResponse:
    """
    Crea risposta TwiML appropriata per azione moderazione
    """
    
    response = VoiceResponse()
    
    message_templates = {
        "polite_warning": "Per favore, mantieni un linguaggio rispettoso. Sono qui per aiutarti con le pratiche di immigrazione.",
        "stern_warning": "Ti ricordo di mantenere un tono professionale. È il secondo avvertimento.",
        "terminate_call_abuse": "Il tuo linguaggio viola le nostre policy. La chiamata termina qui.",
        "terminate_call_repeated": "Hai superato il limite di avvertimenti. La chiamata termina qui. Riprova più tardi con un linguaggio appropriato."
    }
    
    message = message_templates.get(action["message"], "Per favore, mantieni un linguaggio appropriato.")
    
    # Aggiungi messaggio TTS
    response.say(message, language="it-IT", voice="alice")
    
    # Se non termina chiamata, permetti continuazione con warning
    if not action["block_interaction"]:
        # Breve pausa per enfatizzare il warning
        response.pause(length=1)
        
        # Gather per input successivo con warning
        from twilio.twiml.voice_response import Gather
        gather = Gather(
            input="speech",
            timeout=10,
            speech_timeout="auto",
            language="it-IT",
            action="/webhook/voice/process",
            method="POST"
        )
        gather.say("Ora, come posso aiutarti?")
        response.append(gather)
        
        # Fallback se non risponde
        response.say("Richiama quando vuoi. Ciao!")
    else:
        # Termina chiamata per violazioni gravi
        response.say("Ciao.")
        response.hangup()
    
    return response


async def _track_voice_moderation_event(user_id: str, call_sid: str, violation_details: Dict[str, Any], action: Dict[str, Any]):
    """
    Traccia evento moderazione per analytics
    """
    try:
        session_id = generate_session_id(user_id)
        
        await track_journey_event(
            user_id=user_id,
            event_type=EventType.MESSAGE_RECEIVED,  # Uso esistente, potrei aggiungere MODERATION_EVENT
            channel=JourneyChannel.VOICE,
            stage=JourneyStage.ENGAGEMENT,
            session_id=session_id,
            user_input=violation_details["text"],
            data={
                "moderation_violation": True,
                "violation_category": violation_details["primary_category"],
                "violation_severity": violation_details["severity"],
                "confidence_score": violation_details["confidence_score"],
                "action_taken": action["type"],
                "escalation_level": action["escalation_level"],
                "call_sid": call_sid,
                "block_interaction": action["block_interaction"],
                "violated_categories": violation_details["categories"]
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Errore tracking moderazione Voice: {e}")


def _update_user_violations(user_id: str, violation_details: Dict[str, Any], action: Dict[str, Any]):
    """
    Aggiorna cronologia violazioni utente
    """
    
    if user_id not in user_violations:
        user_violations[user_id] = {
            "violation_count": 0,
            "first_violation": datetime.now(),
            "violations_history": []
        }
    
    user_data = user_violations[user_id]
    
    # Aggiungi violazione corrente
    user_data["violation_count"] += 1
    user_data["last_violation"] = datetime.now()
    user_data["violations_history"].append({
        "timestamp": violation_details["timestamp"],
        "category": violation_details["primary_category"],
        "severity": violation_details["severity"],
        "action": action["type"]
    })
    
    # Tracking warning specifici
    if action["type"] in ["first_warning", "second_warning"]:
        user_data["last_warning_time"] = datetime.now()
    
    # Cleanup violazioni vecchie (oltre 1 ora)
    expiry_time = datetime.now() - timedelta(seconds=VOICE_MODERATION_CONFIG["violation_expiry"])
    user_data["violations_history"] = [
        v for v in user_data["violations_history"] 
        if v["timestamp"] > expiry_time
    ]
    
    # Reset count se violazioni sono tutte scadute
    if not user_data["violations_history"]:
        user_data["violation_count"] = 0
    else:
        user_data["violation_count"] = len(user_data["violations_history"])


def get_user_moderation_status(user_id: str) -> Dict[str, Any]:
    """
    Ottieni stato moderazione per utente
    
    Returns:
        Dict con violation_count, last_violation, is_banned, etc.
    """
    
    if user_id not in user_violations:
        return {
            "violation_count": 0,
            "is_banned": False,
            "last_violation": None,
            "ban_expires": None,
            "status": "clean"
        }
    
    user_data = user_violations[user_id]
    
    # Controlla se è attualmente bannato
    is_banned = False
    ban_expires = None
    
    if user_data.get("last_violation"):
        last_violation = user_data["last_violation"]
        warning_timeout = timedelta(seconds=VOICE_MODERATION_CONFIG["warning_timeout"])
        
        if datetime.now() - last_violation < warning_timeout and user_data["violation_count"] >= 3:
            is_banned = True
            ban_expires = last_violation + warning_timeout
    
    return {
        "violation_count": user_data["violation_count"],
        "is_banned": is_banned,
        "last_violation": user_data.get("last_violation"),
        "ban_expires": ban_expires,
        "status": "banned" if is_banned else "violations" if user_data["violation_count"] > 0 else "clean",
        "violations_history": user_data.get("violations_history", [])
    }


def clear_user_violations(user_id: str) -> bool:
    """
    Pulisce violazioni per utente (admin function)
    """
    if user_id in user_violations:
        del user_violations[user_id]
        logger.info(f"✅ Violazioni pulite per utente {user_id}")
        return True
    return False 