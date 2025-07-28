from fastapi import APIRouter, Form, Request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os
import logging
from ..middleware import llm, memory
from ..agents import context, planner, validator, executor
from ..policy import guardrails

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize Twilio client
twilio_client = None
try:
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    if account_sid and auth_token:
        twilio_client = Client(account_sid, auth_token)
        logger.info("✅ Twilio client initialized")
    else:
        logger.warning("⚠️ Twilio credentials not found")
except Exception as e:
    logger.error(f"❌ Error initializing Twilio: {e}")

def handle_incoming(phone: str, text: str, channel: str = "text"):
    """Unified handler for incoming messages"""
    
    # Load or create context
    ctx = memory.load_context(phone) or context.Context(phone)
    
    # 1 - Guard rails
    abuse = guardrails.is_abusive(text)
    if abuse:
        return guardrails.close_message(ctx.lang)
    
    # 2 - Planner
    intent, reason = planner.plan(ctx, text, llm)
    intent = validator.validate(ctx, intent)
    
    # 3 - Execute skill
    reply = executor.dispatch(intent, ctx, text)
    
    # 4 - Persist
    memory.save_context(ctx)
    
    return reply

@router.post("/webhook")
async def whatsapp_webhook(
    request: Request,
    From: str = Form(...),
    Body: str = Form(...),
    To: str = Form(...)
):
    """WhatsApp webhook handler"""
    
    logger.info(f"📱 WhatsApp webhook - From: {From}, Body: {Body}")
    
    try:
        # Extract phone number
        phone = From.replace("whatsapp:", "")
        
        # Handle incoming message
        reply = handle_incoming(phone, Body, "whatsapp")
        
        # Send response
        response_data = _send_whatsapp_message(phone, reply)
        
        logger.info(f"✅ WhatsApp response sent: {response_data}")
        return response_data
        
    except Exception as e:
        logger.error(f"❌ Error in WhatsApp webhook: {e}")
        return {"status": "error", "message": str(e)}

def _send_whatsapp_message(to_number: str, message: str):
    """Send WhatsApp message via Twilio"""
    
    if not twilio_client:
        logger.warning("⚠️ Twilio not configured - local fallback")
        return {
            "status": "local_fallback",
            "reply": message,
            "method": "local",
            "message": "Twilio non disponibile - risposta locale",
            "original_number": to_number,
            "formatted_number": to_number
        }
    
    try:
        # Format number for WhatsApp
        formatted_number = f"whatsapp:{to_number}"
        from_number = os.getenv('TWILIO_WHATSAPP_NUMBER', '+18149149892')
        
        # Send message
        message_obj = twilio_client.messages.create(
            body=message,
            from_=f"whatsapp:{from_number}",
            to=formatted_number
        )
        
        logger.info(f"✅ WhatsApp message sent: {message_obj.sid}")
        
        return {
            "status": "sent",
            "reply": message,
            "method": "whatsapp",
            "message": "Messaggio inviato con successo",
            "sid": message_obj.sid,
            "original_number": to_number,
            "formatted_number": formatted_number
        }
        
    except Exception as e:
        logger.error(f"❌ Error sending WhatsApp message: {e}")
        return {
            "status": "error",
            "reply": message,
            "method": "error",
            "message": f"Errore invio: {str(e)}",
            "original_number": to_number,
            "formatted_number": to_number
        } 