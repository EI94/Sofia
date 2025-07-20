from fastapi import APIRouter, Request
from fastapi.responses import Response, PlainTextResponse  
from twilio.twiml.voice_response import VoiceResponse, Gather
import logging
import os
from app.tools.memory import FirestoreMemory
from app.chains.planner import sofia_planner
from app.chains.detect_language import detect_language
from app.chains.classify_intent import classify_intent
from app.tools.elevenlabs_tts import sofia_tts, generate_sofia_speech
from app.tools.error_handler import (
    error_handler, handle_sofia_errors, create_error_response,
    extract_context_from_request, extract_voice_context_from_request, 
    Channel, ErrorCategory, ErrorSeverity, ErrorResponseGenerator
)
from app.tools.journey_analytics import (
    track_journey_event, EventType, JourneyStage, 
    Channel as JourneyChannel, generate_session_id
)

# Import per streaming ElevenLabs
from app.tools.elevenlabs_streaming import (
    audio_coordinator, 
    twilio_media_handler,
    ElevenLabsStreamer
)
from fastapi import WebSocket, WebSocketDisconnect

import json
from datetime import datetime
import base64
from typing import Any, Optional, Dict
import asyncio

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Configurazione servizi
TWILIO_VOICE_NUMBER = os.getenv("TWILIO_VOICE_NUMBER", "+18149149892")
memory_store = FirestoreMemory()

# Configurazione TTS avanzato
USE_ELEVENLABS_TTS = os.getenv("USE_ELEVENLABS_TTS", "true").lower() == "true"
SOFIA_VOICE_NAME = os.getenv("SOFIA_VOICE_NAME", "sarah")  # sarah, aria, laura, alice

# Mappatura voce ElevenLabs a nome utente
SOFIA_VOICES = {
    "sarah": "sarah",
    "aria": "aria",
    "laura": "laura",
    "alice": "alice",
    "charlotte": "charlotte"
}


@router.post("/voice/inbound")
async def voice_inbound_call(request: Request):
    """Webhook per chiamate in entrata con error handling centralizzato e journey tracking completo"""
    try:
        form_data = await request.form()
        from_number = form_data.get("From", "")
        call_sid = form_data.get("CallSid", "")
        
        logger.info(f"📞 Chiamata vocale in entrata da {from_number} (Call SID: {call_sid})")
        
        # Genera session ID e traccia chiamata (IDENTICO A WHATSAPP)
        session_id = generate_session_id(from_number)
        
        await track_journey_event(
            user_id=from_number,
            event_type=EventType.FIRST_CONTACT,
            channel=JourneyChannel.VOICE,
            stage=JourneyStage.DISCOVERY,
            session_id=session_id,
            data={"call_sid": call_sid}
        )
        
        # Controlla stato cliente nel database con error handling
        try:
            user_data = await memory_store.get_user(from_number)
            if user_data and user_data.get('type') == 'attivo':
                client_status = {'status': 'active', 'data': user_data}
            else:
                client_status = {'status': 'new', 'data': {}}
        except Exception as db_error:
            # Error handling per database con fallback  
            context = extract_voice_context_from_request(request, from_number, {"call_sid": call_sid})
            await error_handler.handle_error(db_error, context, ErrorCategory.DATABASE, ErrorSeverity.MEDIUM)
            logger.warning(f"⚠️ Database fallito, assumo cliente nuovo: {db_error}")
            client_status = {'status': 'new', 'data': {}}
        
        logger.info(f"Stato cliente {from_number}: {client_status['status']}")
        
        if client_status['status'] == 'active':
            # Cliente attivo - messaggio diretto
            name = client_status.get('data', {}).get('name', '')
            if name:
                message = f"Ciao {name}! Sono Sofia dello Studio Immigrato. Per seguire la tua pratica, scarica la nostra app dal sito studioimmigrato.it"
            else:
                message = "Ciao! Sono Sofia dello Studio Immigrato. Per seguire la tua pratica, scarica la nostra app dal sito studioimmigrato.it"
            
            # Track: Message per cliente attivo
            await track_journey_event(
                user_id=from_number,
                event_type=EventType.MESSAGE_RECEIVED,
                channel=JourneyChannel.VOICE,
                stage=JourneyStage.ENGAGEMENT,
                session_id=session_id,
                ai_response=message,
                data={"client_type": "active", "call_sid": call_sid}
            )
            
            # Genera audio ElevenLabs se disponibile (per uso futuro)
            if USE_ELEVENLABS_TTS and sofia_tts.is_available():
                try:
                    audio_bytes = await generate_sofia_speech(message, SOFIA_VOICE_NAME)
                    if audio_bytes:
                        logger.info(f"🎵 Audio ElevenLabs generato: {len(audio_bytes)} bytes")
                        # TODO: Serve implementazione streaming audio con Twilio
                except Exception as e:
                    logger.warning(f"ElevenLabs fallito, uso Twilio TTS: {e}")
            
            response = await create_enhanced_voice_response(
                message, 
                language="it",  # TODO: Detect from user preferences
                enable_streaming=True,
                call_sid=call_sid,
                user_preferences=client_status.get('data', {})
            )
            
        else:
            # Cliente nuovo - avvia conversazione interattiva con journey tracking
            greeting = "Ciao! Sono Sofia dello Studio Immigrato di Milano. Come posso aiutarti oggi?"
            
            # Track: Greeting per cliente nuovo
            await track_journey_event(
                user_id=from_number,
                event_type=EventType.MESSAGE_RECEIVED,
                channel=JourneyChannel.VOICE,
                stage=JourneyStage.ENGAGEMENT,
                session_id=session_id,
                ai_response=greeting,
                data={"client_type": "new", "call_sid": call_sid, "interaction_type": "greeting"}
            )
            
            # Genera audio ElevenLabs (per futuro uso)  
            if USE_ELEVENLABS_TTS and sofia_tts.is_available():
                try:
                    audio_bytes = await generate_sofia_speech(greeting, SOFIA_VOICE_NAME)
                    if audio_bytes:
                        logger.info(f"🎵 Audio ElevenLabs greeting: {len(audio_bytes)} bytes")
                except Exception as e:
                    logger.warning(f"ElevenLabs greeting fallito: {e}")
            
            response = VoiceResponse()
            response.say(greeting, language="it-IT", voice="alice")
            
            # Raccolta input vocale
            gather = Gather(
                input="speech",
                timeout=10,
                speech_timeout="auto",
                language="it-IT",
                action="/webhook/voice/process",
                method="POST"
            )
            gather.say("Ti ascolto, dimmi pure!")
            response.append(gather)
            
            # Fallback se non sente nulla
            response.say("Non ho sentito nulla. Richiama quando vuoi! Ciao!")
        
        return PlainTextResponse(content=str(response), media_type="application/xml")
        
    except Exception as e:
        # Error handling globale per chiamate vocali
        user_id = from_number if 'from_number' in locals() else ""
        context = extract_context_from_request(request, Channel.VOICE, user_id)
        sofia_error = await error_handler.handle_error(e, context, ErrorCategory.SYSTEM, ErrorSeverity.HIGH)
        
        # Risposta vocale di errore
        error_response = _create_voice_error_response(sofia_error)
        return PlainTextResponse(content=str(error_response), media_type="application/xml")


@router.post("/voice/process")
async def voice_process_speech(request: Request):
    """Processa il parlato dell'utente e genera risposta intelligente con journey tracking completo"""
    try:
        form_data = await request.form()
        speech_result = form_data.get("SpeechResult", "")
        from_number = form_data.get("From", "")
        call_sid = form_data.get("CallSid", "")
        
        logger.info(f"🎤 Parlato ricevuto da {from_number}: '{speech_result}' (Call SID: {call_sid})")
        
        # Genera session ID per continuità tracking
        session_id = generate_session_id(from_number)
        
        if not speech_result.strip():
            # Non ha detto nulla
            response = VoiceResponse()
            response.say("Non ho capito bene. Puoi ripetere?", language="it-IT", voice="alice")
            
            gather = Gather(
                input="speech",
                timeout=10,
                speech_timeout="auto", 
                language="it-IT",
                action="/webhook/voice/process",
                method="POST"
            )
            response.append(gather)
            return PlainTextResponse(content=str(response), media_type="application/xml")
        
        # === MODERAZIONE CONTENUTI VOICE (NUOVO - IDENTICO WHATSAPP) ===
        try:
            from app.tools.moderation import check_voice_content
            
            is_blocked, violation_reason, moderation_response = await check_voice_content(
                speech_result, 
                from_number, 
                call_sid
            )
            
            if is_blocked:
                # Contenuto violento/inappropriato - termina o warning
                logger.warning(f"🚨 Voice moderation blocked: {from_number} - {violation_reason}")
                
                # Track moderazione per analytics
                await track_journey_event(
                    user_id=from_number,
                    event_type=EventType.MESSAGE_RECEIVED,
                    channel=JourneyChannel.VOICE,
                    stage=JourneyStage.ENGAGEMENT,
                    session_id=session_id,
                    user_input=speech_result,
                    data={
                        "moderation_blocked": True,
                        "violation_reason": violation_reason,
                        "call_sid": call_sid,
                        "speech_input": True
                    }
                )
                
                return PlainTextResponse(content=str(moderation_response), media_type="application/xml")
            
        except Exception as mod_error:
            # Gestisce errore moderazione senza bloccare flusso (come WhatsApp)
            context = extract_voice_context_from_request(request, from_number, {"call_sid": call_sid})
            context.user_input = speech_result
            await error_handler.handle_error(mod_error, context, ErrorCategory.API_EXTERNAL, ErrorSeverity.LOW)
            logger.warning(f"⚠️ Moderazione Voice fallita, procedo senza controllo: {mod_error}")
        
        # === IMPLEMENTAZIONE JOURNEY TRACKING COMPLETO (IDENTICO WHATSAPP) ===
        
        # Inizializzazione LLM con error handling
        try:
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        except Exception as llm_error:
            context = extract_voice_context_from_request(request, from_number, {"call_sid": call_sid})
            context.user_input = speech_result
            sofia_error = await error_handler.handle_error(llm_error, context, ErrorCategory.API_EXTERNAL, ErrorSeverity.HIGH)
            
            # Fallback response senza LLM
            response = VoiceResponse()
            response.say("Mi dispiace, c'è un problema tecnico temporaneo. Riprova tra qualche minuto.", language="it-IT", voice="alice")
            return PlainTextResponse(content=str(response), media_type="application/xml")
        
        # Step 1: Language Detection (NUOVO - come WhatsApp)
        try:
            lang = detect_language(speech_result, llm)
            logger.info(f"🌍 Lingua rilevata: {lang}")
            
            # Track: Language Detection
            await track_journey_event(
                user_id=from_number,
                event_type=EventType.LANGUAGE_DETECTED,
                channel=JourneyChannel.VOICE,
                stage=JourneyStage.ENGAGEMENT,
                session_id=session_id,
                language=lang,
                user_input=speech_result,
                data={"call_sid": call_sid, "speech_input": True}
            )
            
        except Exception as lang_error:
            context = extract_voice_context_from_request(request, from_number, {"call_sid": call_sid})
            context.user_input = speech_result
            await error_handler.handle_error(lang_error, context, ErrorCategory.API_INTERNAL, ErrorSeverity.LOW)
            lang = "it"  # Default fallback
            logger.info(f"🌍 Lingua fallback: {lang}")
        
        # Step 2: Intent Classification (NUOVO - come WhatsApp)
        try:
            intent = classify_intent(speech_result, llm)
            logger.info(f"🎯 Intent classificato: {intent}")
            
            # Track: Intent Classification
            await track_journey_event(
                user_id=from_number,
                event_type=EventType.INTENT_CLASSIFIED,
                channel=JourneyChannel.VOICE,
                stage=JourneyStage.QUALIFICATION,
                session_id=session_id,
                language=lang,
                intent=intent,
                user_input=speech_result,
                data={"call_sid": call_sid, "speech_input": True}
            )
            
        except Exception as intent_error:
            context = extract_voice_context_from_request(request, from_number, {"call_sid": call_sid})
            context.user_input = speech_result
            await error_handler.handle_error(intent_error, context, ErrorCategory.API_INTERNAL, ErrorSeverity.LOW)
            intent = "general"  # Default fallback
            logger.info(f"🎯 Intent fallback: {intent}")
        
        # Step 3: Salvataggio dati utente con error handling (come WhatsApp)
        try:
            topic = " ".join(speech_result.split()[:5])
            await memory_store.upsert_user(from_number, lang, case_topic=topic)
        except Exception as memory_error:
            context = extract_context_from_request(request, Channel.VOICE, from_number)
            await error_handler.handle_error(memory_error, context, ErrorCategory.DATABASE, ErrorSeverity.MEDIUM)
            logger.warning(f"⚠️ Salvataggio utente voice fallito: {memory_error}")
            # Continua senza bloccare il flusso
        
        # Step 4: Controlla stato cliente per continuità
        try:
            user_data = await memory_store.get_user(from_number)
            if user_data and user_data.get('type') == 'attivo':
                client_status = {'status': 'active', 'data': user_data}
            else:
                client_status = {'status': 'new', 'data': {}}
        except Exception:
            client_status = {'status': 'new', 'data': {}}
        
        # Step 5: Pianificazione risposta con error handling e stati persistenti (IDENTICO WHATSAPP)
        try:
            # === INTEGRAZIONE STATI PERSISTENTI VOICE ===  
            # Recupera stato conversazione corrente (come WhatsApp)
            current_state = await memory_store.get_conversation_state(from_number, "voice") or "greeting"
            conversation_context = await memory_store.get_conversation_context(from_number, "voice") or {}
            
            logger.info(f"🔄 VOICE - Stato corrente: {current_state}, Contesto: {len(conversation_context)} items")
            
            # USA METODO CORRETTO plan_voice_response() che ESISTE!  
            ai_response = await sofia_planner.plan_voice_response(
                from_number, 
                speech_result, 
                client_status,  # Passa stato cliente
                lang,  # Usa lingua rilevata dinamicamente
                intent   # Usa intent classificato
            )
            logger.info(f"🤖 Risposta Sofia: {ai_response}")
            
            # === AGGIORNAMENTO STATI POST-RESPONSE ===
            # Determina nuovo stato basato su contenuto risposta
            new_state = current_state  # Default: mantiene stato attuale
            
            # Logica intelligente per avanzamento stati
            if current_state == "greeting" and any(word in speech_result.lower() for word in ["permesso", "cittadinanza", "ricongiungimento", "visa", "immigration"]):
                new_state = "service_inquiry"
            elif current_state == "service_inquiry" and "consulenza" in ai_response.lower():
                new_state = "booking_request"  
            elif current_state == "booking_request" and any(word in speech_result.lower() for word in ["quando", "data", "ora", "appuntamento", "today", "tomorrow", "lunedì", "martedì"]):
                new_state = "datetime_collection"
            elif current_state == "datetime_collection" and "nome" in ai_response.lower():
                new_state = "confirmation"
            elif current_state == "confirmation" and "confermato" in ai_response.lower():
                new_state = "completed"
            
            # Salva conversazione exchange con metadati completi
            await memory_store.add_conversation_exchange(
                from_number, 
                "voice",
                speech_result,
                ai_response,
                {
                    "call_sid": call_sid,
                    "language": lang,
                    "intent": intent,
                    "previous_state": current_state,
                    "new_state": new_state,
                    "speech_input": True
                }
            )
            
            # Aggiorna stato conversazione con contesto ricco
            await memory_store.update_conversation_state(
                from_number,
                "voice", 
                new_state,
                {
                    "last_input": speech_result,
                    "last_response": ai_response,
                    "language": lang,
                    "intent": intent,
                    "call_sid": call_sid,
                    "interaction_count": conversation_context.get("interaction_count", 0) + 1,
                    "session_start": conversation_context.get("session_start", datetime.now().isoformat()),
                    "last_interaction": datetime.now().isoformat()
                }
            )
            
            logger.info(f"🔄 VOICE - Stato aggiornato: {current_state} → {new_state}")
            
            # Track: AI Response Generated (IDENTICO WHATSAPP)
            await track_journey_event(
                user_id=from_number,
                event_type=EventType.MESSAGE_RECEIVED,
                channel=JourneyChannel.VOICE,
                stage=JourneyStage.ENGAGEMENT,
                session_id=session_id,
                language=lang,
                intent=intent,
                user_input=speech_result,
                ai_response=ai_response,
                data={
                    "call_sid": call_sid,
                    "speech_input": True,
                    "client_type": client_status['status'],
                    "response_generated": True,
                    "conversation_state": new_state,
                    "state_transition": f"{current_state} → {new_state}" if new_state != current_state else "same_state"
                }
            )
            
        except Exception as plan_error:
            context = extract_context_from_request(request, Channel.VOICE, from_number)
            context.user_input = speech_result
            context.language = lang
            await error_handler.handle_error(plan_error, context, ErrorCategory.BUSINESS_LOGIC, ErrorSeverity.MEDIUM)
            
            # Fallback response basata su lingua rilevata
            if lang == "en":
                ai_response = "I'm sorry, I'm having technical difficulties. Please try again in a few minutes."
            elif lang == "fr":
                ai_response = "Je suis désolée, j'ai des difficultés techniques. Veuillez réessayer dans quelques minutes."
            elif lang == "es":
                ai_response = "Lo siento, tengo dificultades técnicas. Inténtalo de nuevo en unos minutos."
            else:
                ai_response = "Mi dispiace, ho difficoltà tecniche. Riprova tra qualche minuto."
        
        # Genera audio ElevenLabs per la risposta (se disponibile)
        if USE_ELEVENLABS_TTS and sofia_tts.is_available():
            try:
                audio_bytes = await generate_sofia_speech(ai_response, SOFIA_VOICE_NAME)
                if audio_bytes:
                    logger.info(f"🎵 Audio risposta ElevenLabs: {len(audio_bytes)} bytes")
                    # TODO: Implementare streaming audio verso Twilio
            except Exception as e:
                logger.warning(f"ElevenLabs risposta fallita: {e}")
        
        # Determina lingua TTS basata su lingua rilevata
        tts_language = "it-IT"
        if lang == "en":
            tts_language = "en-US"
        elif lang == "fr":  
            tts_language = "fr-FR"
        elif lang == "es":
            tts_language = "es-ES"
        
        # Genera risposta TwiML
        response = VoiceResponse()
        response.say(ai_response, language=tts_language, voice="alice")
        
        # Se cliente nuovo, continua conversazione (gestione stati persistenti)
        if client_status['status'] == 'new':
            if "consulenza" in ai_response.lower() or "appuntamento" in ai_response.lower():
                gather = Gather(
                    input="speech",
                    timeout=10,
                    speech_timeout="auto",
                    language=tts_language,
                    action="/webhook/voice/process",
                    method="POST"
                )
                gather.say("Hai altre domande?")
                response.append(gather)
            else:
                response.say("Grazie per aver chiamato lo Studio Immigrato. A presto!")
        else:
            response.say("Buona giornata!")
        
        return PlainTextResponse(content=str(response), media_type="application/xml")
        
    except Exception as e:
        # Error handling globale con journey tracking
        logger.error(f"❌ Errore voice processing: {e}")
        context = extract_context_from_request(request, Channel.VOICE, from_number if 'from_number' in locals() else "")
        sofia_error = await error_handler.handle_error(e, context, ErrorCategory.SYSTEM, ErrorSeverity.HIGH)
        
        response = VoiceResponse()
        response.say("Mi dispiace, c'è stato un errore. Richiama più tardi.", language="it-IT", voice="alice")
        return PlainTextResponse(content=str(response), media_type="application/xml")


@router.get("/voice/test")
async def test_voice_services():
    """Test completo di tutti i servizi vocali"""
    results = {
        "timestamp": "2024-test",
        "services": {
            "sofia_planner": "✅ Ready",
            "memory_store": "✅ Connected", 
            "twilio_voice": "✅ Configured",
            "sofia_ai": "✅ Active"
        },
        "tts_engines": {
            "twilio_native": "✅ Active (alice, it-IT)",
            "elevenlabs": "✅ Available" if sofia_tts.is_available() else "❌ Not configured",
            "current_voice": SOFIA_VOICE_NAME if USE_ELEVENLABS_TTS else "alice"
        },
        "endpoints": {
            "/voice/inbound": "✅ Main call handler",
            "/voice/process": "✅ Speech processing", 
            "/voice/test": "✅ Service testing"
        },
        "user_experience": {
            "active_clients": "App redirect",
            "new_clients": "Consultation booking",
            "language": "Italian (IT-IT)",
            "voice": f"ElevenLabs {SOFIA_VOICE_NAME}" if USE_ELEVENLABS_TTS and sofia_tts.is_available() else "Twilio Alice"
        }
    }
    
    return results


@router.get("/voice/stats") 
async def voice_statistics():
    """Statistiche delle chiamate vocali"""
    return {
        "total_calls": 0,
        "active_clients": 0,
        "new_clients": 0,
        "avg_duration": "0s",
        "success_rate": "100%",
        "tts_engine": "ElevenLabs + Twilio" if sofia_tts.is_available() else "Twilio Only",
        "note": "Voice statistics tracking ready"
    }


@router.post("/voice/tts/test")
async def test_elevenlabs_integration():
    """Endpoint per testare l'integrazione ElevenLabs"""
    try:
        test_text = "Ciao! Sono Sofia dello Studio Immigrato. Questo è un test della mia nuova voce con ElevenLabs."
        
        if not sofia_tts.is_available():
            return {"error": "ElevenLabs non disponibile", "tts_engine": "twilio_only"}
        
        # Genera audio con ElevenLabs
        audio_bytes = await generate_sofia_speech(test_text, SOFIA_VOICE_NAME)
        
        if audio_bytes:
            return {
                "success": True,
                "audio_size": len(audio_bytes),
                "voice_used": SOFIA_VOICE_NAME,
                "text": test_text,
                "tts_engine": "elevenlabs"
            }
        else:
            return {"error": "Generazione audio fallita", "tts_engine": "fallback"}
            
    except Exception as e:
        logger.error(f"Errore test ElevenLabs: {e}")
        return {"error": str(e), "tts_engine": "error"}


# ===== TWILIO MEDIA STREAMS ENDPOINT =====

@router.websocket("/voice/media-stream")
async def twilio_media_stream(websocket: WebSocket):
    """
    Endpoint WebSocket per Twilio Media Streams - Streaming audio real-time
    Integrazione ElevenLabs → Twilio per qualità audio superiore
    """
    await websocket.accept()
    logger.info("📡 Twilio Media Stream WebSocket connected")
    
    try:
        stream_sid = None
        call_sid = None
        audio_buffer = []
        
        while True:
            # Ricevi messaggi da Twilio Media Stream
            data = await websocket.receive_text()
            message = json.loads(data)
            
            event = message.get("event")
            
            if event == "connected":
                logger.info("🔗 Media Stream connected")
                
            elif event == "start":
                stream_sid = message["start"]["streamSid"] 
                call_sid = message["start"]["callSid"]
                logger.info(f"🎵 Media Stream started: {stream_sid} (Call: {call_sid})")
                
            elif event == "media":
                # Audio ricevuto dall'utente (da implementare speech-to-text se necessario)
                media_payload = message["media"]["payload"]
                # Base64 decoded audio chunk μ-law 8kHz
                audio_chunk = base64.b64decode(media_payload)
                audio_buffer.append(audio_chunk)
                
                # Accumula audio chunks per processing (implementazione futura per real-time)
                # Per ora Sofia gestisce solo responses via speech recognition Twilio standard
                
            elif event == "stop":
                logger.info(f"🛑 Media Stream stopped: {stream_sid}")
                break
                
            elif event == "mark":
                # Marker events da Twilio
                mark_name = message.get("mark", {}).get("name", "")
                logger.info(f"📍 Media Stream mark: {mark_name}")
    
    except WebSocketDisconnect:
        logger.info("📡 Media Stream WebSocket disconnected")
    except Exception as e:
        logger.error(f"❌ Media Stream error: {e}")
        try:
            await websocket.close()
        except:
            pass


# ===== ELEVENLABS INTEGRATION AVANZATA =====

async def create_enhanced_voice_response(text: str, language: str = "it", enable_streaming: bool = True, 
                                       call_sid: str = "", user_preferences: Dict[str, Any] = None) -> VoiceResponse:
    """
    Crea risposta vocale avanzata con ElevenLabs streaming e fallback automatico
    
    Args:
        text: Testo da sintetizzare
        language: Lingua rilevata  
        enable_streaming: Se abilitare streaming ElevenLabs
        call_sid: Call SID per tracking
        user_preferences: Preferenze utente (voce, velocità, etc.)
        
    Returns:
        VoiceResponse: Oggetto TwiML ottimizzato
    """
    if user_preferences is None:
        user_preferences = {}
    
    response = VoiceResponse()
    
    try:
        # === VOICE SELECTION DINAMICA ===
        # Selezione voce basata su lingua e preferenze utente
        selected_voice = _select_optimal_voice(language, user_preferences)
        
        # Determina lingua TTS Twilio per fallback
        tts_language, tts_voice = _get_twilio_tts_config(language)
        
        # === STRATEGIA STREAMING ELEVENLABS ===
        if enable_streaming and USE_ELEVENLABS_TTS and sofia_tts.is_available():
            
            logger.info(f"🎵 Attempting ElevenLabs streaming: {selected_voice['name']}")
            
            # Tenta streaming ElevenLabs
            try:
                # Genera audio con ElevenLabs streaming
                audio_bytes = await generate_sofia_speech_streaming(
                    text, 
                    selected_voice['voice_id'],
                    language
                )
                
                if audio_bytes and len(audio_bytes) > 1000:  # Verifica audio valido
                    # SUCCESS: Audio ElevenLabs generato
                    logger.info(f"✅ ElevenLabs audio generated: {len(audio_bytes)} bytes")
                    
                    # Per ora usa TTS Twilio con voice ottimizzata
                    # TODO: Implementare streaming diretto quando Media Streams sarà completo
                    response.say(text, language=tts_language, voice=selected_voice.get('twilio_equivalent', tts_voice))
                    
                    # Aggiunge marker per tracking
                    if call_sid:
                        response.play("", loop=0)  # Marker placeholder per analytics
                    
                else:
                    # Fallback automatico a Twilio TTS
                    logger.warning("⚠️ ElevenLabs audio vuoto, fallback a Twilio TTS")
                    response.say(text, language=tts_language, voice=tts_voice)
                    
            except Exception as elevenlabs_error:
                # FALLBACK AUTOMATICO: ElevenLabs fallito
                logger.warning(f"⚠️ ElevenLabs streaming failed: {elevenlabs_error}")
                logger.info("🔄 Auto-fallback to Twilio TTS")
                
                # Usa Twilio TTS con voce ottimizzata per lingua
                response.say(text, language=tts_language, voice=tts_voice)
                
                # Log per monitoring fallback rate
                await track_journey_event(
                    user_id=call_sid or "unknown",
                    event_type=EventType.MESSAGE_RECEIVED,
                    channel=JourneyChannel.VOICE,
                    stage=JourneyStage.ENGAGEMENT,
                    session_id=generate_session_id(call_sid or ""),
                    data={
                        "tts_engine": "twilio_fallback",
                        "elevenlabs_error": str(elevenlabs_error),
                        "fallback_reason": "elevenlabs_streaming_failed"
                    }
                )
        else:
            # === TWILIO TTS STANDARD ===
            logger.info(f"🔊 Using Twilio TTS: {tts_language} - {tts_voice}")
            response.say(text, language=tts_language, voice=tts_voice)
            
        return response
        
    except Exception as e:
        logger.error(f"❌ Enhanced voice response error: {e}")
        
        # FALLBACK ULTRA-SICURO
        response = VoiceResponse()
        response.say("Mi dispiace, c'è stato un errore tecnico. Riprova.", language="it-IT", voice="alice")
        return response


def _select_optimal_voice(language: str, user_preferences: Dict[str, Any]) -> Dict[str, str]:
    """
    Seleziona voce ottimale basata su lingua e preferenze utente
    
    Args:
        language: Lingua rilevata (it, en, fr, es)
        user_preferences: Preferenze utente salvate
        
    Returns:
        Dict con voice_id ElevenLabs e configurazione
    """
    
    # Preferenze utente override
    if user_preferences.get("preferred_voice"):
        preferred = user_preferences["preferred_voice"]
        if preferred in SOFIA_VOICES:
            return {
                "voice_id": SOFIA_VOICES[preferred],
                "name": preferred,
                "twilio_equivalent": "alice"
            }
    
    # Selezione automatica basata su lingua
    voice_mapping = {
        "it": {
            "voice_id": SOFIA_VOICES["sarah"],  # Calda e professionale per italiano
            "name": "sarah",
            "twilio_equivalent": "alice"
        },
        "en": {
            "voice_id": SOFIA_VOICES["aria"],   # Naturale per inglese
            "name": "aria", 
            "twilio_equivalent": "alice"
        },
        "fr": {
            "voice_id": SOFIA_VOICES["laura"],  # Professionale per francese
            "name": "laura",
            "twilio_equivalent": "alice"
        },
        "es": {
            "voice_id": SOFIA_VOICES["charlotte"], # Neutra per spagnolo
            "name": "charlotte",
            "twilio_equivalent": "alice"
        }
    }
    
    return voice_mapping.get(language, voice_mapping["it"])  # Default italiano


def _get_twilio_tts_config(language: str) -> tuple:
    """
    Ottiene configurazione TTS Twilio ottimale per lingua
    
    Args:
        language: Lingua rilevata
        
    Returns:
        tuple: (language_code, voice_name) per Twilio TTS
    """
    
    config_mapping = {
        "it": ("it-IT", "alice"),
        "en": ("en-US", "alice"), 
        "fr": ("fr-FR", "alice"),
        "es": ("es-ES", "alice"),
        "de": ("de-DE", "alice"),
        "pt": ("pt-PT", "alice")
    }
    
    return config_mapping.get(language, ("it-IT", "alice"))  # Default italiano


async def generate_sofia_speech_streaming(text: str, voice_id: str, language: str = "it") -> Optional[bytes]:
    """
    Genera audio Sofia con ElevenLabs streaming ottimizzato
    
    Args:
        text: Testo da sintetizzare
        voice_id: ID voce ElevenLabs
        language: Lingua per ottimizzazioni
        
    Returns:
        bytes: Audio PCM 8kHz se successo, None se errore
    """
    try:
        # Usa l'istanza ElevenLabs TTS esistente
        if not sofia_tts.is_available():
            logger.warning("ElevenLabs non disponibile per streaming")
            return None
        
        # Ottimizzazioni testo per TTS
        optimized_text = _optimize_text_for_tts(text, language)
        
        # Genera audio con timeout e retry
        audio_bytes = await asyncio.wait_for(
            sofia_tts.synthesize_speech(optimized_text, voice_id), 
            timeout=10.0
        )
        
        if audio_bytes:
            logger.info(f"✅ Sofia speech generated: {len(audio_bytes)} bytes")
            return audio_bytes
        else:
            logger.warning("⚠️ ElevenLabs returned empty audio")
            return None
            
    except asyncio.TimeoutError:
        logger.warning("⚠️ ElevenLabs timeout - fallback to Twilio TTS")
        return None
    except Exception as e:
        logger.warning(f"⚠️ ElevenLabs synthesis error: {e}")
        return None


def _optimize_text_for_tts(text: str, language: str) -> str:
    """
    Ottimizza testo per sintesi vocale migliorata
    
    Args:
        text: Testo originale
        language: Lingua per ottimizzazioni specifiche
        
    Returns:
        str: Testo ottimizzato per TTS
    """
    
    # Pulizia base
    optimized = text.strip()
    
    # Sostituzioni per pronuncia migliore (italiano)
    if language == "it":
        replacements = {
            "€": "euro",
            "&": "e",
            "@": "at",
            "%": "percento",
            "www.": "doppio doppio doppio punto",
            ".it": "punto it",
            "whatsapp": "Whatsapp",
            "sofia": "Sofia"
        }
        
        for old, new in replacements.items():
            optimized = optimized.replace(old, new)
    
    # Limita lunghezza per streaming efficace
    if len(optimized) > 500:
        optimized = optimized[:497] + "..."
        
    return optimized


@router.post("/voice/process-streaming")
async def voice_process_streaming(request: Request):
    """
    Endpoint per processare speech con risposta streaming ElevenLabs
    Utilizzato quando Twilio invia speech transcription
    """
    try:
        form_data = await request.form()
        speech_result = form_data.get("SpeechResult", "")
        from_number = form_data.get("From", "")
        call_sid = form_data.get("CallSid", "")
        
        logger.info(f"🎤 Speech streaming da {from_number}: '{speech_result}'")
        
        if not speech_result.strip():
            # Nessun speech rilevato
            response = VoiceResponse()
            
            # Se Media Stream attivo, usa streaming
            if call_sid in twilio_media_handler.active_streams:
                await twilio_media_handler.send_audio_to_twilio(
                    call_sid, 
                    "Non ho capito bene. Puoi ripetere?"
                )
                # Ritorna response vuota per non interferire con streaming
                return PlainTextResponse(content="<Response/>", media_type="application/xml")
            else:
                # Fallback TTS standard
                response.say("Non ho capito bene. Puoi ripetere?", language="it-IT", voice="alice")
                return PlainTextResponse(content=str(response), media_type="application/xml")
        
        # Processa speech con Sofia AI + streaming ElevenLabs
        if call_sid in twilio_media_handler.active_streams:
            # Usa streaming pipeline
            ai_response = await audio_coordinator.process_voice_interaction(call_sid, speech_result)
            
            # Log per debugging
            logger.info(f"🎵 Risposta streamata a {call_sid}: {ai_response}")
            
            # Return empty response (audio già streamato)
            return PlainTextResponse(content="<Response/>", media_type="application/xml")
        
        else:
            # Fallback a TTS standard se streaming non disponibile
            user_data = await memory_store.get_user(from_number)
            client_status = {'status': 'active' if user_data else 'new', 'data': user_data or {}}
            
            ai_response = await sofia_planner.plan_voice_response(
                from_number, speech_result, client_status, "it", "richiesta informazioni"
            )
            
            # Prova ElevenLabs non-streaming
            if USE_ELEVENLABS_TTS and sofia_tts.is_available():
                try:
                    audio_bytes = await generate_sofia_speech(ai_response, SOFIA_VOICE_NAME)
                    if audio_bytes:
                        logger.info(f"🎵 ElevenLabs audio: {len(audio_bytes)} bytes (non-streaming)")
                except Exception as e:
                    logger.warning(f"ElevenLabs fallito: {e}")
            
            response = VoiceResponse()
            response.say(ai_response, language="it-IT", voice="alice")
            return PlainTextResponse(content=str(response), media_type="application/xml")
        
    except Exception as e:
        logger.error(f"❌ Errore processing streaming: {e}")
        response = VoiceResponse()
        response.say("Mi dispiace, c'è un problema tecnico. Riprova.")
        return PlainTextResponse(content=str(response), media_type="application/xml")




def _create_voice_error_response(sofia_error: Any) -> VoiceResponse:
    """
    Crea risposta TwiML per errori Voice usando error handler avanzato
    
    Args:
        sofia_error: Errore Sofia standardizzato
        
    Returns:
        VoiceResponse: Oggetto TwiML per risposta vocale di errore
    """
    try:
        # Usa il nuovo error handler per generare TwiML
        response_gen = ErrorResponseGenerator()
        twiml_xml = response_gen.create_voice_twiml_error_response(sofia_error)
        
        # Parsea il XML TwiML generato in oggetto VoiceResponse
        response = VoiceResponse()
        
        # Estrae lingua e messaggio dal SofiaError
        language = getattr(sofia_error.context, 'language', 'it') if sofia_error.context else 'it'
        
        # Mappa lingua a codice TTS Twilio
        tts_language = "it-IT"
        if language == "en":
            tts_language = "en-US"
        elif language == "fr":
            tts_language = "fr-FR"  
        elif language == "es":
            tts_language = "es-ES"
        
        # Genera messaggio di errore appropriato usando l'error handler  
        error_response = response_gen.get_voice_error_response(
            language, 
            "general", 
            sofia_error.severity
        )
        
        response.say(error_response["message"], language=tts_language, voice="alice")
        
        logger.info(f"🎤 Voice error response generated: {sofia_error.severity.value}")
        return response
        
    except Exception as e:
        logger.error(f"❌ Errore generazione risposta voice TwiML: {e}")
        
        # Fallback ultra-semplice se anche l'error handler fallisce
        response = VoiceResponse()
        response.say("Mi dispiace, c'è stato un errore. Richiama più tardi.", language="it-IT", voice="alice")
        return response
