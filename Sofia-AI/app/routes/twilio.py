from fastapi import APIRouter, Request, status, Response
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse
from langchain_openai import ChatOpenAI
import os
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Router per Twilio endpoints
router = APIRouter()

# Inizializzazione validator Twilio
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
if TWILIO_AUTH_TOKEN:
    validator = RequestValidator(TWILIO_AUTH_TOKEN)
else:
    logger.warning("TWILIO_AUTH_TOKEN non configurato")
    validator = None

# LLM sarà inizializzato on-demand
llm = None

@router.post("/twilio/inbound", status_code=200)
async def inbound(req: Request):
    print("DEBUG Twilio: INIZIO FUNZIONE inbound")
    
    # LOG DI DEBUG IMMEDIATO
    logger.warning(f"DEBUG Twilio START: url={req.url} method={req.method} client={req.client}")
    
    """
    Endpoint per ricevere messaggi inbound da Twilio.
    Valida la richiesta, processa il messaggio con OpenAI e risponde via TwiML.
    """
    try:
        # Lettura del body della richiesta
        raw_body = await req.body()
        form_data = await req.form()
        
        # LOG DI DEBUG COMPLETO
        logger.warning(f"DEBUG Twilio: url={req.url} method={req.method} headers={dict(req.headers)} form_data={dict(form_data)}")
        
        # DEBUG: loggo i dati usati per la validazione Twilio
        print(f"DEBUG Twilio: url={req.url} form_data={dict(form_data)} signature={req.headers.get('X-Twilio-Signature', '')}")
        logger.warning(f"DEBUG Twilio: url={req.url} form_data={dict(form_data)} signature={req.headers.get('X-Twilio-Signature', '')}")
        
        # Validazione signature Twilio
        if validator:
            valid = validator.validate(
                str(req.url),  # URL completo
                {k: v for k, v in form_data.items()},
                req.headers.get("X-Twilio-Signature", "")
            )
            if not valid:
                logger.warning(f"Richiesta Twilio non valida da {req.client.host}")
                return Response(status_code=status.HTTP_403_FORBIDDEN)
        else:
            logger.warning("Validator Twilio non configurato, richiesta accettata senza validazione")

        # Estrazione dati del messaggio
        body = form_data.get("Body", "")
        from_number = form_data.get("From", "")
        
        logger.info(f"Messaggio ricevuto da {from_number}: {body}")
        
        # Risposta di default se il messaggio è vuoto
        if not body.strip():
            twiml = MessagingResponse()
            twiml.message("Ciao! Invia un messaggio per iniziare a chattare con Sofia.")
            return Response(content=str(twiml), media_type="application/xml")

        # Elaborazione del messaggio con OpenAI
        try:
            # Inizializzazione on-demand del LLM
            global llm
            if llm is None:
                try:
                    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
                except Exception as llm_error:
                    logger.error(f"Errore nell'inizializzazione LLM: {llm_error}")
                    raise Exception("LLM non configurato")
            
            # Uso il LLM moderno di Langchain
            messages = [
                {"role": "system", "content": "Sei Sofia, assistente virtuale dello Studio Immigrato di Milano. Rispondi in modo professionale e utile."},
                {"role": "user", "content": body}
            ]
            
            response = llm.invoke(messages)
            answer = response.content
            
            logger.info(f"Risposta generata per {from_number}: {answer}")
            
        except Exception as e:
            logger.error(f"Errore nell'elaborazione OpenAI: {e}")
            answer = "Mi dispiace, al momento non riesco a processare la tua richiesta. Riprova tra poco."

        # Creazione risposta TwiML
        twiml = MessagingResponse()
        twiml.message(answer)
        
        return Response(content=str(twiml), media_type="application/xml")
        
    except Exception as e:
        logger.error(f"Errore nell'endpoint Twilio inbound: {e}")
        
        # Risposta di errore
        twiml = MessagingResponse()
        twiml.message("Si è verificato un errore. Riprova più tardi.")
        return Response(content=str(twiml), media_type="application/xml")

@router.get("/twilio/status")
async def twilio_status():
    """Endpoint per verificare lo status della configurazione Twilio."""
    # Test configurazione OpenAI
    openai_configured = False
    try:
        test_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        openai_configured = True
    except:
        openai_configured = False
    
    return {
        "twilio_configured": validator is not None,
        "openai_configured": openai_configured,
        "endpoint": "/twilio/inbound"
    } 