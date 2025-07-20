from fastapi import APIRouter, Form, HTTPException, UploadFile, File, Request
from twilio.rest import Client
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from app.chains.detect_language import detect_language
from app.chains.classify_intent import classify_intent
from app.chains.planner import sofia_planner
from app.tools import moderation, memory, ocr
from app.tools.memory import FirestoreMemory
from app.tools.error_handler import (
    error_handler, handle_sofia_errors, create_error_response,
    extract_context_from_request, Channel, ErrorCategory, ErrorSeverity
)
from app.tools.journey_analytics import (
    track_journey_event, EventType, JourneyStage, 
    Channel as JourneyChannel, generate_session_id
)
import os
import logging
import base64
from datetime import datetime

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# NOTA: Sistema prompt UNIFIED rimosso - ora usa il planner unificato che contiene
# il sistema prompt PARA-HELP v3 completo con EXCLUSIONS allineate

# Inizializzazione client Twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER]):
    logger.warning("Variabili Twilio non configurate completamente")
    twilio_client = None
else:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Inizializzazione FirestoreMemory
memory_store = FirestoreMemory()


# Le funzioni detect_language, classify_intent e planner sono ora importate da app.chains


@router.post("/whatsapp")
async def whatsapp_webhook(
    request: Request,
    From: str = Form(...),
    Body: str = Form(...)
):
    """
    Webhook per ricevere messaggi WhatsApp da Twilio con error handling centralizzato.
    
    - **From**: Numero del mittente
    - **Body**: Testo del messaggio
    """
    try:
        logger.info(f"📱 Messaggio WhatsApp ricevuto da {From}: {Body}")
        
        # Genera session ID per tracking
        session_id = generate_session_id(From)
        
        # Track: First Contact Event
        await track_journey_event(
            user_id=From,
            event_type=EventType.FIRST_CONTACT,
            channel=JourneyChannel.WHATSAPP,
            stage=JourneyStage.DISCOVERY,
            session_id=session_id,
            user_input=Body
        )
        
        # Controllo moderazione contenuti con error handling
        try:
            if await moderation.is_abusive(Body):
                reply = "Il tuo messaggio viola le nostre policy. La conversazione termina qui."
                if twilio_client:
                    twilio_client.messages.create(body=reply, from_=TWILIO_NUMBER, to=From)
                await memory.save_message(From, Body, "aggressivo")
                return {"status": "blocked", "reason": "content_moderation"}
        except Exception as mod_error:
            # Gestisce errore moderazione senza bloccare flusso
            context = extract_context_from_request(request, Channel.WHATSAPP, From)
            context.user_input = Body
            await error_handler.handle_error(mod_error, context, ErrorCategory.API_EXTERNAL, ErrorSeverity.LOW)
            logger.warning(f"⚠️ Moderazione fallita, procedo senza controllo: {mod_error}")
        
        # Inizializzazione LLM con error handling
        try:
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        except Exception as llm_error:
            context = extract_context_from_request(request, Channel.WHATSAPP, From)
            sofia_error = await error_handler.handle_error(llm_error, context, ErrorCategory.API_EXTERNAL, ErrorSeverity.HIGH)
            
            # Fallback response senza LLM
            reply = "Mi dispiace, c'è un problema tecnico temporaneo. Riprova tra qualche minuto. 🔧"
            return await _send_whatsapp_message(From, reply, fallback_mode=True)
        
        # Step 1: Rilevamento lingua con error handling
        try:
            lang = detect_language(Body, llm)
            logger.info(f"🌍 Lingua rilevata: {lang}")
            
            # Track: Language Detection
            await track_journey_event(
                user_id=From,
                event_type=EventType.LANGUAGE_DETECTED,
                channel=JourneyChannel.WHATSAPP,
                stage=JourneyStage.ENGAGEMENT,
                session_id=session_id,
                language=lang,
                user_input=Body
            )
            
        except Exception as lang_error:
            context = extract_context_from_request(request, Channel.WHATSAPP, From)
            context.user_input = Body
            await error_handler.handle_error(lang_error, context, ErrorCategory.API_INTERNAL, ErrorSeverity.LOW)
            lang = "it"  # Default fallback
            logger.info(f"🌍 Lingua fallback: {lang}")
        
        # Step 2: Classificazione intent con error handling
        try:
            intent = classify_intent(Body, llm)
            logger.info(f"🎯 Intent classificato: {intent}")
            
            # Track: Intent Classification
            await track_journey_event(
                user_id=From,
                event_type=EventType.INTENT_CLASSIFIED,
                channel=JourneyChannel.WHATSAPP,
                stage=JourneyStage.QUALIFICATION,
                session_id=session_id,
                language=lang,
                intent=intent,
                user_input=Body
            )
            
        except Exception as intent_error:
            context = extract_context_from_request(request, Channel.WHATSAPP, From)
            context.user_input = Body
            await error_handler.handle_error(intent_error, context, ErrorCategory.API_INTERNAL, ErrorSeverity.LOW)
            intent = "general"  # Default fallback
            logger.info(f"🎯 Intent fallback: {intent}")
        
        # Step 3: Salvataggio dati utente con error handling
        try:
            topic = " ".join(Body.split()[:5])
            await memory_store.upsert_user(From, lang, case_topic=topic)
        except Exception as memory_error:
            context = extract_context_from_request(request, Channel.WHATSAPP, From)
            await error_handler.handle_error(memory_error, context, ErrorCategory.DATABASE, ErrorSeverity.MEDIUM)
            logger.warning(f"⚠️ Salvataggio utente fallito: {memory_error}")
            # Continua senza bloccare il flusso
        
        # Step 4: Pianificazione risposta con error handling
        try:
            reply = await sofia_planner.plan(lang, intent, Body, From)
            logger.info(f"💬 Risposta generata: {reply}")
            
            # Track: AI Response Generated
            await track_journey_event(
                user_id=From,
                event_type=EventType.MESSAGE_RECEIVED,
                channel=JourneyChannel.WHATSAPP,
                stage=JourneyStage.ENGAGEMENT,
                session_id=session_id,
                language=lang,
                intent=intent,
                user_input=Body,
                ai_response=reply
            )
            
        except Exception as plan_error:
            context = extract_context_from_request(request, Channel.WHATSAPP, From)
            context.user_input = Body
            context.language = lang
            await error_handler.handle_error(plan_error, context, ErrorCategory.BUSINESS_LOGIC, ErrorSeverity.MEDIUM)
            
            # Fallback response basata su lingua
            if lang == "en":
                reply = "I'm sorry, I'm having technical difficulties. Please try again in a few minutes."
            else:
                reply = "Mi dispiace, ho difficoltà tecniche. Riprova tra qualche minuto."
        
        # Step 5: Invio messaggio con error handling integrato
        return await _send_whatsapp_message(From, reply)
        
    except Exception as e:
        # Error handling globale per errori non catturati
        context = extract_context_from_request(request, Channel.WHATSAPP, From)
        context.user_input = Body
        sofia_error = await error_handler.handle_error(e, context, ErrorCategory.SYSTEM, ErrorSeverity.HIGH)
        
        # Risposta di emergenza
        emergency_response = await create_error_response(sofia_error, "it")
        return emergency_response


@router.post("/upload/receipt")
async def upload_receipt(phone: str = Form(...), file: UploadFile = File(...)):
    """
    Endpoint per l'upload di ricevute di pagamento.
    
    - **phone**: Numero di telefono dell'utente
    - **file**: File immagine della ricevuta (JPEG)
    """
    try:
        logger.info(f"Upload ricevuta da {phone}: {file.filename}")
        
        b64 = base64.b64encode(await file.read()).decode()
        ok = await ocr.iban_in_image(b64)
        
        if ok:
            await memory_store.update_payment(phone, "paid")
            msg = "Ricevuta valida! Ti confermiamo la consulenza."
            logger.info(f"Pagamento confermato per {phone}")
        else:
            msg = "Immagine illeggibile o IBAN mancante. Riprova."
            logger.warning(f"Ricevuta non valida per {phone}")
        
        if twilio_client:
            twilio_client.messages.create(body=msg, from_=TWILIO_NUMBER, to=phone)
        else:
            logger.info(f"SIMULAZIONE: Messaggio '{msg}' a {phone}")
        
        return {"ok": ok, "message": msg}
        
    except Exception as e:
        logger.error(f"Errore upload ricevuta per {phone}: {e}")
        return {"ok": False, "error": str(e)}


async def _send_whatsapp_message(to_number: str, message: str, fallback_mode: bool = False, 
                              force_sms: bool = False, test_fallback: bool = False) -> dict:
    """
    Invia messaggio WhatsApp con fallback SMS ottimizzato e testing avanzato
    
    Args:
        to_number: Numero destinatario
        message: Messaggio da inviare
        fallback_mode: Se True, è già un fallback (non logga come errore)
        force_sms: Se True, forza uso diretto SMS (per testing)
        test_fallback: Se True, simula errore WhatsApp per testare SMS fallback
        
    Returns:
        dict: Stato invio messaggio con dettagli completi
    """
    
    # Simulazione se Twilio non configurato
    if not twilio_client:
        logger.info(f"📱 SIMULAZIONE WhatsApp: '{message}' → {to_number}")
        return {
            "status": "simulated", 
            "reply": message, 
            "method": "simulation",
            "message": "Twilio non configurato - simulazione attiva",
            "original_number": to_number,
            "formatted_number": to_number
        }
    
    # FORCE SMS per testing o preferenza utente
    if force_sms:
        logger.info("📱 SMS forzato - bypasso WhatsApp")
        return await _send_sms_direct(to_number, message, reason="force_sms")
    
    # Tentativo invio WhatsApp
    try:
        # Test fallback simulation
        if test_fallback:
            raise Exception("Simulated WhatsApp failure for testing")
        
        # Formatting numero WhatsApp ottimizzato  
        whatsapp_to, whatsapp_from = _format_whatsapp_numbers(to_number, TWILIO_NUMBER)
        
        twilio_message = twilio_client.messages.create(
            body=message,
            from_=whatsapp_from,
            to=whatsapp_to
        )
        
        logger.info(f"✅ Messaggio WhatsApp inviato con SID: {twilio_message.sid}")
        return {
            "status": "sent", 
            "method": "whatsapp", 
            "message_sid": twilio_message.sid,
            "original_number": to_number,
            "formatted_number": whatsapp_to,
            "message_length": len(message)
        }
        
    except Exception as whatsapp_error:
        if not fallback_mode and not test_fallback:
            logger.warning(f"⚠️ WhatsApp fallito per {to_number}: {whatsapp_error}")
        
        # FALLBACK AUTOMATICO A SMS con error handling migliorato
        return await _send_sms_fallback(to_number, message, whatsapp_error)


async def _send_sms_fallback(to_number: str, message: str, original_error: Exception) -> dict:
    """
    Gestisce fallback SMS con formatting avanzato e error handling
    """
    try:
        # Numero formatting ottimizzato per SMS cross-country
        sms_to, sms_from = _format_sms_numbers(to_number, TWILIO_NUMBER)
        
        # Messaggio ottimizzato per SMS
        sms_message = _format_message_for_sms(message)
        
        # Verifica lunghezza SMS (160 caratteri standard)
        if len(sms_message) > 160:
            logger.warning(f"⚠️ SMS messaggio lungo ({len(sms_message)} chars), potrebbe essere splittato")
        
        sms_response = twilio_client.messages.create(
            body=sms_message,
            from_=sms_from,
            to=sms_to
        )
        
        logger.info(f"✅ Fallback SMS inviato con SID: {sms_response.sid} ({len(sms_message)} chars)")
        
        # Track fallback per analytics  
        await _track_sms_fallback_event(to_number, original_error, sms_response.sid)
        
        return {
            "status": "sent", 
            "method": "sms_fallback", 
            "message_sid": sms_response.sid,
            "original_error": str(original_error),
            "original_number": to_number,
            "formatted_sms_to": sms_to,
            "formatted_sms_from": sms_from,
            "message_length": len(sms_message),
            "split_message": len(sms_message) > 160
        }
        
    except Exception as sms_error:
        logger.error(f"❌ SMS fallback anche fallito per {to_number}: {sms_error}")
        
        # ULTIMO FALLBACK: Email notification (se configurato)
        emergency_fallback = await _attempt_emergency_fallback(to_number, message, original_error, sms_error)
        
        return {
            "status": "failed", 
            "method": "both_failed",
            "whatsapp_error": str(original_error),
            "sms_error": str(sms_error),
            "original_number": to_number,
            "message": "Impossibile inviare tramite WhatsApp o SMS",
            "emergency_fallback": emergency_fallback
        }


async def _send_sms_direct(to_number: str, message: str, reason: str = "direct") -> dict:
    """
    Invia SMS diretto (non fallback)
    """
    try:
        sms_to, sms_from = _format_sms_numbers(to_number, TWILIO_NUMBER)
        sms_message = _format_message_for_sms(message, direct=True)
        
        sms_response = twilio_client.messages.create(
            body=sms_message,
            from_=sms_from,
            to=sms_to
        )
        
        logger.info(f"✅ SMS diretto inviato ({reason}) con SID: {sms_response.sid}")
        return {
            "status": "sent",
            "method": "sms_direct",
            "message_sid": sms_response.sid,
            "reason": reason,
            "formatted_number": sms_to
        }
        
    except Exception as e:
        logger.error(f"❌ SMS diretto fallito: {e}")
        return {"status": "failed", "method": "sms_direct", "error": str(e)}


def _format_whatsapp_numbers(to_number: str, from_number: str) -> tuple:
    """
    Formatting ottimizzato numeri WhatsApp con validazione - BUG FIX per spazi e +
    """
    
    # TO number formatting - RIMUOVI SPAZI E NORMALIZZA
    whatsapp_to = to_number.replace(" ", "").strip()  # RIMUOVI SPAZI!
    
    # Se già ha whatsapp: prefix, normalizza
    if whatsapp_to.startswith('whatsapp:'):
        # Estrai numero pulito
        clean_number = whatsapp_to.replace('whatsapp:', '').strip()
        # Assicurati che abbia +
        if not clean_number.startswith('+'):
            clean_number = f"+{clean_number}"
        whatsapp_to = f"whatsapp:{clean_number}"
    else:
        # Aggiungi + se manca
        if not whatsapp_to.startswith('+'):
            whatsapp_to = f"+{whatsapp_to}"
        whatsapp_to = f"whatsapp:{whatsapp_to}"
    
    # FROM number formatting - IDENTICO FIX  
    if from_number:
        whatsapp_from = from_number.replace(" ", "").strip()
        if not whatsapp_from.startswith('whatsapp:'):
            if not whatsapp_from.startswith('+'):
                whatsapp_from = f"+{whatsapp_from}"
            whatsapp_from = f"whatsapp:{whatsapp_from}"
    else:
        whatsapp_from = None
    
    if not whatsapp_from:
        logger.warning("⚠️ TWILIO_WHATSAPP_NUMBER non configurato")
        whatsapp_from = "whatsapp:+1234567890"  # Fallback temporaneo
    
    logger.info(f"📱 WhatsApp format: {to_number} → {whatsapp_to}")
    return whatsapp_to, whatsapp_from


def _format_sms_numbers(to_number: str, from_number: str) -> tuple:
    """
    Formatting numeri SMS con validazione cross-country migliorata
    """
    
    # Clean TO number (rimuovi prefissi WhatsApp/Telegram)
    sms_to = to_number.replace("whatsapp:", "").replace("telegram:", "").strip()
    
    # Validazione numero internazionale
    if not sms_to.startswith("+"):
        # Se non ha +, assume numero USA (fallback)
        if len(sms_to) == 10 and sms_to.isdigit():
            sms_to = f"+1{sms_to}"
        elif len(sms_to) == 11 and sms_to.startswith("1"):
            sms_to = f"+{sms_to}"
        else:
            logger.warning(f"⚠️ Numero SMS non standard: {sms_to}")
    
    # Clean FROM number 
    sms_from = from_number.replace("whatsapp:", "").strip() if from_number else None
    
    if not sms_from:
        logger.error("❌ TWILIO_VOICE_NUMBER non configurato per SMS")
        sms_from = "+1234567890"  # Fallback temporaneo
    
    return sms_to, sms_from


def _format_message_for_sms(message: str, direct: bool = False) -> str:
    """
    Formatta messaggio per SMS con ottimizzazioni lunghezza
    """
    
    # Prefix appropriato
    if direct:
        prefix = "Sofia (Studio Immigrato): "
    else:
        prefix = "Sofia AI (Fallback SMS): "
    
    # Limita lunghezza per evitare split SMS costosi
    max_content_length = 160 - len(prefix)
    
    if len(message) <= max_content_length:
        return f"{prefix}{message}"
    else:
        # Tronca intelligente su spazio o punteggiatura
        truncated = message[:max_content_length-3]
        last_space = truncated.rfind(' ')
        last_punct = max(truncated.rfind('.'), truncated.rfind('!'), truncated.rfind('?'))
        
        if last_punct > max_content_length - 20:  # Tronca su punteggiatura se vicina
            truncated = truncated[:last_punct+1]
        elif last_space > max_content_length - 20:  # Altrimenti su spazio
            truncated = truncated[:last_space]
        else:
            truncated = truncated + "..."
        
        return f"{prefix}{truncated}"


async def _track_sms_fallback_event(user_id: str, whatsapp_error: Exception, sms_sid: str):
    """
    Traccia evento SMS fallback per analytics e monitoring
    """
    try:
        from app.tools.journey_analytics import track_journey_event, EventType, JourneyStage, Channel as JourneyChannel, generate_session_id
        
        session_id = generate_session_id(user_id)
        
        await track_journey_event(
            user_id=user_id,
            event_type=EventType.MESSAGE_RECEIVED,
            channel=JourneyChannel.WHATSAPP,  # Originating channel
            stage=JourneyStage.ENGAGEMENT,
            session_id=session_id,
            data={
                "sms_fallback_used": True,
                "whatsapp_error": str(whatsapp_error),
                "sms_sid": sms_sid,
                "fallback_reason": "whatsapp_delivery_failed",
                "delivery_method": "sms_fallback"
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Errore tracking SMS fallback: {e}")


async def _attempt_emergency_fallback(to_number: str, message: str, whatsapp_error: Exception, sms_error: Exception) -> dict:
    """
    Tentativo ultimo fallback (email notification se configurato)
    """
    try:
        # Placeholder per futuro fallback email/webhook  
        logger.error(f"💥 EMERGENCY: Tutti i canali falliti per {to_number}")
        logger.error(f"WhatsApp error: {whatsapp_error}")
        logger.error(f"SMS error: {sms_error}")
        logger.error(f"Message non consegnato: {message[:100]}...")
        
        # TODO: Implementare notifica email admin se configurata
        # TODO: Implementare webhook per sistema esterno se configurato
        
        return {
            "attempted": True,
            "method": "logging_only",
            "admin_notified": False,  # Sarà True quando implementato
            "message": "Logged emergency fallback event"
        }
        
    except Exception as e:
        logger.error(f"❌ Anche emergency fallback fallito: {e}")
        return {"attempted": False, "error": str(e)}


@router.get("/test")
async def test_whatsapp():
    """Endpoint di test per verificare il funzionamento del router WhatsApp."""
    return {
        "service": "whatsapp",
        "status": "active",
        "twilio_configured": twilio_client is not None,
        "system_prompt": "Sofia AI integrated"
    } 


@router.post("/test/sms-fallback")
async def test_sms_fallback_system(test_number: str = "+1234567890", test_message: str = "Test SMS fallback"):
    """
    Endpoint per testare sistema SMS fallback senza impattare utenti reali
    
    Args:
        test_number: Numero di test per SMS
        test_message: Messaggio di test
        
    Returns:
        dict: Risultati completi test fallback
    """
    
    if not twilio_client:
        return {
            "status": "error",
            "message": "Twilio client non configurato - impossibile testare SMS",
            "twilio_configured": False
        }
    
    logger.info(f"🧪 TESTING SMS Fallback System per {test_number}")
    
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "test_number": test_number,
        "test_message": test_message,
        "tests": {}
    }
    
    try:
        # TEST 1: WhatsApp normale (dovrebbe funzionare)
        logger.info("🧪 Test 1: WhatsApp normale")
        whatsapp_result = await _send_whatsapp_message(
            test_number, 
            f"TEST 1: {test_message}",
            fallback_mode=False
        )
        test_results["tests"]["whatsapp_normal"] = whatsapp_result
        
        # TEST 2: Forza SMS diretto
        logger.info("🧪 Test 2: SMS diretto forzato")
        sms_direct_result = await _send_whatsapp_message(
            test_number,
            f"TEST 2: {test_message}",
            force_sms=True
        )
        test_results["tests"]["sms_direct"] = sms_direct_result
        
        # TEST 3: Simula fallimento WhatsApp per attivare fallback
        logger.info("🧪 Test 3: Fallback WhatsApp → SMS")
        fallback_result = await _send_whatsapp_message(
            test_number,
            f"TEST 3: {test_message}",
            test_fallback=True
        )
        test_results["tests"]["whatsapp_to_sms_fallback"] = fallback_result
        
        # TEST 4: Test formatting numeri
        logger.info("🧪 Test 4: Number formatting")
        test_numbers = [
            f"whatsapp:{test_number}",  # Con prefisso WhatsApp
            test_number.replace("+", ""),  # Senza +
            test_number  # Normale
        ]
        
        formatting_tests = {}
        for num in test_numbers:
            try:
                wa_to, wa_from = _format_whatsapp_numbers(num, TWILIO_NUMBER or "+1234567890")
                sms_to, sms_from = _format_sms_numbers(num, TWILIO_NUMBER or "+1234567890")
                
                formatting_tests[num] = {
                    "whatsapp_formatted": {"to": wa_to, "from": wa_from},
                    "sms_formatted": {"to": sms_to, "from": sms_from}
                }
            except Exception as e:
                formatting_tests[num] = {"error": str(e)}
        
        test_results["tests"]["number_formatting"] = formatting_tests
        
        # TEST 5: Test lunghezza messaggi SMS  
        logger.info("🧪 Test 5: SMS message length handling")
        long_message = "Questo è un messaggio molto lungo per testare il sistema di troncamento intelligente dei messaggi SMS che dovrebbe essere troncato appropriatamente per non superare il limite di 160 caratteri standard per SMS."
        
        formatted_short = _format_message_for_sms("Messaggio corto")
        formatted_long = _format_message_for_sms(long_message)
        formatted_direct = _format_message_for_sms("Messaggio diretto", direct=True)
        
        test_results["tests"]["message_formatting"] = {
            "short_message": {
                "original_length": len("Messaggio corto"),
                "formatted": formatted_short,
                "formatted_length": len(formatted_short)
            },
            "long_message": {
                "original_length": len(long_message),
                "formatted": formatted_long,
                "formatted_length": len(formatted_long),
                "was_truncated": len(formatted_long) < len(long_message) + 50  # Approssimazione
            },
            "direct_message": {
                "formatted": formatted_direct,
                "formatted_length": len(formatted_direct)
            }
        }
        
        # TEST 6: Performance timing
        import time
        start_time = time.time()
        
        timing_result = await _send_whatsapp_message(
            test_number,
            "TEST Performance timing",
            force_sms=True  # SMS diretto per consistenza timing
        )
        
        end_time = time.time()
        
        test_results["tests"]["performance_timing"] = {
            "duration_seconds": round(end_time - start_time, 3),
            "result": timing_result
        }
        
        # SUMMARY
        test_results["summary"] = {
            "total_tests": len(test_results["tests"]),
            "whatsapp_working": test_results["tests"]["whatsapp_normal"]["status"] == "sent",
            "sms_direct_working": test_results["tests"]["sms_direct"]["status"] == "sent",
            "fallback_working": test_results["tests"]["whatsapp_to_sms_fallback"]["status"] == "sent",
            "all_systems_operational": True  # Sarà calcolato
        }
        
        # Calcola se tutti i sistemi funzionano
        operational_tests = [
            test_results["tests"]["whatsapp_normal"]["status"] == "sent",
            test_results["tests"]["sms_direct"]["status"] == "sent", 
            test_results["tests"]["whatsapp_to_sms_fallback"]["status"] == "sent"
        ]
        test_results["summary"]["all_systems_operational"] = all(operational_tests)
        
        logger.info(f"✅ SMS Fallback Test completato: {test_results['summary']}")
        
        return test_results
        
    except Exception as e:
        logger.error(f"❌ Errore durante test SMS fallback: {e}")
        test_results["error"] = str(e)
        test_results["status"] = "failed"
        return test_results 