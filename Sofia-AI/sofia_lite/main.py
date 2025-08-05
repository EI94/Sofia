"""
Sofia Lite - Main Application Entry Point
Integrazione completa di tutti i moduli
"""

import os
import logging
from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse, Response
from contextlib import asynccontextmanager
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global orchestrator instance
orchestrator = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager per inizializzazione e cleanup"""
    global orchestrator
    
    # Inizializzazione
    try:
        logger.info("Inizializzazione Sofia Lite...")
        
        # Import orchestrator solo quando necessario
        from .agents.orchestrator import Orchestrator
        orchestrator = Orchestrator()
        
        logger.info("✅ Sofia Lite inizializzata con successo")
        
    except Exception as e:
        logger.error(f"❌ Errore durante l'inizializzazione: {e}")
        orchestrator = None
    
    yield
    
    # Cleanup
    logger.info("Cleanup Sofia Lite...")

app = FastAPI(
    title="Sofia Lite", 
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Sofia Lite è operativa!", 
        "status": "healthy",
        "version": "1.0.0",
        "orchestrator": "ready" if orchestrator else "initializing"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy", 
        "service": "sofia-lite",
        "orchestrator": "ready" if orchestrator else "initializing"
    }

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    """WhatsApp webhook endpoint."""
    try:
        # Try to get JSON data first
        try:
            json_data = await request.json()
            logger.info(f"📋 JSON data received: {json_data}")
            phone = json_data.get("From", "").replace("whatsapp:", "")
            message = json_data.get("Body", "")
            logger.info(f"📱 Extracted from JSON - phone: '{phone}', message: '{message}'")
        except Exception as e:
            logger.warning(f"⚠️ JSON parsing failed: {e}, trying form data")
            # Fallback to form data
            form_data = await request.form()
            phone = form_data.get("From", "").replace("whatsapp:", "")
            message = form_data.get("Body", "")
            logger.info(f"📱 Extracted from form - phone: '{phone}', message: '{message}'")
        
        logger.info(f"WhatsApp message from {phone}: {message[:50]}...")
        
        if not orchestrator:
            return JSONResponse(
                content={
                    "reply": "Sofia è temporaneamente non disponibile. Riprova tra qualche minuto.",
                    "intent": "ERROR",
                    "state": "INITIAL",
                    "lang": "it",
                    "phone": phone
                }
            )
        
        # Processa il messaggio con l'orchestrator
        try:
            response = orchestrator.process_message(phone, message)
            logger.info(f"Processed message for {phone}: {response.get('reply', '')[:100]}...")
            
            return JSONResponse(content=response)
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return JSONResponse(
                content={
                    "reply": "Mi dispiace, c'è stato un errore nel processare il tuo messaggio. Riprova.",
                    "intent": "ERROR",
                    "state": "INITIAL",
                    "lang": "it",
                    "phone": phone
                }
            )
        
    except Exception as e:
        logger.error(f"Error in WhatsApp webhook: {e}")
        return JSONResponse(
            content={
                "reply": "Errore interno del server. Riprova più tardi.",
                "intent": "ERROR",
                "state": "INITIAL",
                "lang": "it",
                "phone": ""
            },
            status_code=500
        )

@app.post("/webhook/voice")
async def voice_webhook(request: Request):
    """Voice webhook endpoint."""
    try:
        form_data = await request.form()
        phone = form_data.get("From", "")
        speech_result = form_data.get("SpeechResult", "")
        
        logger.info(f"Voice call from {phone}: {speech_result[:50]}...")
        
        if not orchestrator:
            return JSONResponse(
                content={
                    "reply": "Sofia è temporaneamente non disponibile. Riprova tra qualche minuto.",
                    "intent": "ERROR",
                    "state": "INITIAL",
                    "lang": "it"
                }
            )
        
        # Processa il messaggio vocale con l'orchestrator
        try:
            response = orchestrator.process_message(phone, speech_result)
            logger.info(f"Processed voice for {phone}: {response[:100]}...")
            
            return JSONResponse(content={
                "reply": response,
                "intent": "PROCESSED",
                "state": "ACTIVE",
                "lang": "it"
            })
            
        except Exception as e:
            logger.error(f"Error processing voice: {e}")
            return JSONResponse(
                content={
                    "reply": "Mi dispiace, c'è stato un errore nel processare la tua richiesta vocale. Riprova.",
                    "intent": "ERROR",
                    "state": "INITIAL",
                    "lang": "it"
                }
            )
        
    except Exception as e:
        logger.error(f"Error in voice webhook: {e}")
        return JSONResponse(
            content={
                "reply": "Errore interno del server. Riprova più tardi.",
                "intent": "ERROR",
                "state": "INITIAL",
                "lang": "it"
            },
            status_code=500
        )

@app.get("/status")
async def status():
    """Status endpoint per monitoraggio."""
    return {
        "service": "sofia-lite",
        "version": "1.0.0",
        "orchestrator": "ready" if orchestrator else "initializing",
        "endpoints": {
            "whatsapp": "/webhook/whatsapp",
            "voice": "/webhook/voice",
            "health": "/health"
        }
    }

@app.get("/metrics")
def metrics():
    """Prometheus metrics endpoint."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Starting Sofia Lite on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port) 