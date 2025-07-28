from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import uvicorn
import re
from typing import Optional
from app.api import whatsapp, health, journey
from app.web import dashboard
import logging
from app.gateways.firebase_init import initialize_firebase

logger = logging.getLogger(__name__)

from app.utils.nlp import extract_name_from_input

def extract_name_from_speech(text: str) -> Optional[str]:
    """Estrae nome dal discorso - usa funzione unificata"""
    return extract_name_from_input(text)

def create_app() -> FastAPI:
    """Factory function per creare l'app FastAPI."""
    
    # Inizializza Firebase all'avvio
    logger.info("🚀 Avvio Sofia AI...")
    if initialize_firebase():
        logger.info("✅ Firebase inizializzato con successo")
    else:
        logger.warning("⚠️ Firebase non disponibile, uso fallback")
    
    app = FastAPI(
        title="Sofia AI",
        description="API per assistente AI con WhatsApp e sintesi vocale",
        version="1.0.0"
    )
    
    # HEALTH CHECK ENDPOINT
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "service": "Sofia AI",
            "version": "1.0.0",
            "environment": "production"
        }
    
    # ROOT ENDPOINT
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": "Sofia AI - Il miglior agent del mondo!",
            "version": "1.0.0",
            "endpoints": {
                "health": "/health",
                "whatsapp": "/webhook/whatsapp",
                "voice": "/webhook/voice"
            }
        }
    
    # VOICE ENDPOINTS DIRETTAMENTE QUI - NO CRASH POSSIBLE
    @app.post("/webhook/voice")
    async def voice_webhook(request: Request):
        """Gestisce chiamate vocali - SUPPORTO WHATSAPP CALLING"""
        try:
            form_data = await request.form()
            from_number = form_data.get("From", "")
            to_number = form_data.get("To", "")
            call_status = form_data.get("CallStatus", "")
            call_sid = form_data.get("CallSid", "")
            
            logger.info(f"📞 Voice call: {from_number} → {to_number}, Status: {call_status}, SID: {call_sid}")
            
            # Controlla se è una chiamata WhatsApp
            is_whatsapp_call = from_number.startswith("whatsapp:") or to_number.startswith("whatsapp:")
            
            if is_whatsapp_call:
                logger.info(f"📱 WhatsApp Voice Call detected!")
                # Risposta specifica per WhatsApp Calling
                return PlainTextResponse(f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
        Ciao! Sono Sofia dello Studio Immigrato. Grazie per la chiamata WhatsApp!
    </Say>
    <Gather input="speech" timeout="10" speechTimeout="auto" language="it-IT" 
            action="/webhook/voice/process" method="POST">
        <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
            Come posso aiutarti con le tue pratiche di immigrazione?
        </Say>
    </Gather>
    <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
        Non ho sentito nulla. Puoi scrivermi su WhatsApp quando vuoi. Ciao!
    </Say>
</Response>""", media_type="application/xml")
            
            else:
                # Chiamata telefonica normale
                return PlainTextResponse(f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
        Ciao! Sono Sofia dello Studio Immigrato. Come posso aiutarti?
    </Say>
    <Gather input="speech" timeout="10" speechTimeout="auto" language="it-IT" 
            action="/webhook/voice/process" method="POST">
        <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
            Ti ascolto, dimmi pure!
        </Say>
    </Gather>
    <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
        Non ho sentito nulla. Richiama quando vuoi! Ciao!
    </Say>
</Response>""", media_type="application/xml")
            
        except Exception as e:
            logger.error(f"❌ Errore voice webhook: {e}")
            # Risposta di emergenza che non chiude la chiamata
            return PlainTextResponse(f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
        Ciao! Sono Sofia dello Studio Immigrato. C'è un piccolo problema tecnico, ma sono qui per aiutarti!
    </Say>
    <Pause length="1"/>
    <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
        Puoi scrivermi su WhatsApp o richiamare tra poco. Grazie!
    </Say>
</Response>""", media_type="application/xml")

    @app.post("/webhook/voice/inbound")
    async def voice_inbound_direct(request: Request):
        """Voice inbound - VERSIONE UMANA NON ROBOTICA"""
        return PlainTextResponse(
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<Response>'
            '<Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">'
            'Ciao! Sono Sofia dello Studio Immigrato. Come posso aiutarti?'
            '</Say>'
            '<Gather input="speech" timeout="10" speechTimeout="auto" language="it-IT" action="/webhook/voice/process" method="POST">'
            '<Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">Ti ascolto, dimmi pure!</Say>'
            '</Gather>'
            '<Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">'
            'Non ho sentito nulla. Richiama quando vuoi! Ciao!'
            '</Say>'
            '</Response>',
            media_type="application/xml"
        )

    @app.post("/webhook/voice/process")
    async def voice_process(request: Request):
        """Processa il riconoscimento vocale e genera risposta"""
        try:
            form_data = await request.form()
            speech_result = form_data.get("SpeechResult", "")
            from_number = form_data.get("From", "")
            
            logger.info(f"🎤 Speech ricevuto da {from_number}: {speech_result}")
            
            if not speech_result:
                return PlainTextResponse("""
                    <Response>
                        <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
                            Non ho capito bene. Puoi ripetere?
                        </Say>
                        <Gather input="speech" timeout="10" speechTimeout="auto" language="it-IT" 
                                action="/webhook/voice/process" method="POST">
                            <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
                                Ti ascolto di nuovo!
                            </Say>
                        </Gather>
                    </Response>
                """, media_type="application/xml")
            
            # Estrai nome se presente
            extracted_name = extract_name_from_speech(speech_result)
            
            from app.planner.planner import sofia_planner
            response_text = await sofia_planner.plan_voice_response(
                phone_number=from_number,
                speech_text=speech_result,
                extracted_name=extracted_name
            )
            
            return PlainTextResponse(f"""
                <Response>
                    <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
                        {response_text}
                    </Say>
                    <Gather input="speech" timeout="10" speechTimeout="auto" language="it-IT" 
                            action="/webhook/voice/process" method="POST">
                        <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
                            C'è altro che posso fare per te?
                        </Say>
                    </Gather>
                    <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
                        Perfetto! Ti ricontatto presto. Ciao!
                    </Say>
                </Response>
            """, media_type="application/xml")
            
        except Exception as e:
            logger.error(f"❌ Errore voice process: {e}")
            return PlainTextResponse("""
                <Response>
                    <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
                        Mi dispiace, c'è stato un problema tecnico. Riprova più tardi.
                    </Say>
                </Response>
            """, media_type="application/xml")

    @app.post("/webhook/whatsapp-voice")
    async def whatsapp_voice_webhook(request: Request):
        """Gestisce chiamate vocali WhatsApp in-app (nuova API luglio 2025)"""
        try:
            form_data = await request.form()
            from_number = form_data.get("From", "")
            call_status = form_data.get("CallStatus", "")
            
            logger.info(f"📞 WhatsApp Voice Call da {from_number}: {call_status}")
            
            if call_status == "ringing":
                # Risposta automatica per chiamata WhatsApp
                return PlainTextResponse(f"""
                    <Response>
                        <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
                            Ciao! Sono Sofia dello Studio Immigrato. Grazie per la chiamata WhatsApp!
                        </Say>
                        <Gather input="speech" timeout="10" speechTimeout="auto" language="it-IT" 
                                action="/webhook/whatsapp-voice/process" method="POST">
                            <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
                                Come posso aiutarti con le tue pratiche di immigrazione?
                            </Say>
                        </Gather>
                        <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
                            Non ho sentito nulla. Puoi scrivermi su WhatsApp. Ciao!
                        </Say>
                    </Response>
                """, media_type="application/xml")
                
            return PlainTextResponse("<Response></Response>", media_type="application/xml")
            
        except Exception as e:
            logger.error(f"❌ Errore WhatsApp voice webhook: {e}")
            return PlainTextResponse("<Response></Response>", media_type="application/xml")

    @app.post("/webhook/whatsapp-voice/process")
    async def whatsapp_voice_process(request: Request):
        """Processa il riconoscimento vocale da chiamate WhatsApp"""
        try:
            form_data = await request.form()
            speech_result = form_data.get("SpeechResult", "")
            from_number = form_data.get("From", "")
            
            logger.info(f"🎤 WhatsApp Speech da {from_number}: {speech_result}")
            
            if not speech_result:
                return PlainTextResponse("""
                    <Response>
                        <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
                            Non ho capito bene. Puoi ripetere o scrivermi su WhatsApp?
                        </Say>
                        <Gather input="speech" timeout="8" speechTimeout="auto" language="it-IT" 
                                action="/webhook/whatsapp-voice/process" method="POST">
                            <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
                                Ti ascolto!
                            </Say>
                        </Gather>
                    </Response>
                """, media_type="application/xml")
            
            # Estrai nome se presente
            extracted_name = extract_name_from_speech(speech_result)
            
            from app.planner.planner import sofia_planner
            response_text = await sofia_planner.plan_voice_response(
                phone_number=from_number,
                speech_text=speech_result,
                extracted_name=extracted_name
            )
            
            return PlainTextResponse(f"""
                <Response>
                    <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
                        {response_text}
                    </Say>
                    <Gather input="speech" timeout="8" speechTimeout="auto" language="it-IT" 
                            action="/webhook/whatsapp-voice/process" method="POST">
                        <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
                            Posso aiutarti con altro?
                        </Say>
                    </Gather>
                    <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
                        Perfetto! Puoi sempre scrivermi su WhatsApp. A presto!
                    </Say>
                </Response>
            """, media_type="application/xml")
            
        except Exception as e:
            logger.error(f"❌ Errore WhatsApp voice process: {e}")
            return PlainTextResponse("""
                <Response>
                    <Say voice="Polly.Bianca" language="it-IT" rate="medium" pitch="medium">
                        Mi dispiace, c'è stato un problema. Scrivimi su WhatsApp!
                    </Say>
                </Response>
            """, media_type="application/xml")
    
    # TEST ENDPOINT - TWIML MINIMALE PER DEBUG WHATSAPP CALLING
    @app.post("/webhook/voice/test-minimal")
    async def voice_test_minimal(request: Request):
        """TEST TwiML minimale per debug chiamate WhatsApp che cadono subito"""
        try:
            form_data = await request.form()
            from_number = form_data.get("From", "")
            to_number = form_data.get("To", "")
            call_status = form_data.get("CallStatus", "")
            call_sid = form_data.get("CallSid", "")
            
            logger.info(f"🧪 TEST MINIMAL: {from_number} → {to_number}, Status: {call_status}, SID: {call_sid}")
            
            # TwiML SUPER MINIMALE - NIENTE GATHER, NIENTE COMPLESSITÀ
            return PlainTextResponse("""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Bianca" language="it-IT">
        Sofia ti risponde. Resta in attesa. Test minimale funzionante.
    </Say>
    <Pause length="2"/>
    <Say voice="Polly.Bianca" language="it-IT">
        Se senti questo messaggio, il webhook funziona perfettamente.
    </Say>
</Response>""", media_type="application/xml")
            
        except Exception as e:
            logger.error(f"❌ Errore test minimal: {e}")
            # Risposta di emergenza ULTRA SEMPLICE
            return PlainTextResponse("""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Test emergency response. Webhook is working.</Say>
</Response>""", media_type="application/xml")
    
    # Include routers
    app.include_router(whatsapp.router, prefix="/webhook")
    app.include_router(health.router, prefix="/health")
    app.include_router(journey.router, prefix="/journey")
    app.include_router(dashboard.router, prefix="/dashboard")
    
    return app

# Crea l'app a livello globale per gunicorn/uvicorn
app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 