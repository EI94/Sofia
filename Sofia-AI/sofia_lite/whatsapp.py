from fastapi import APIRouter, Form, Request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os
import logging

# Test webhook flag for direct testing
TEST_WEBHOOK = os.getenv("TEST_WEBHOOK") == "true"
from sofia_lite.middleware.llm import classify
from sofia_lite.agents.orchestrator import Orchestrator
# from sofia_lite.middleware.loop_guard import LoopGuard  # Removed - not implemented
from sofia_lite.skills import dispatch
from sofia_lite.agents.context import Context
from sofia_lite.middleware.memory import load_context, save_context
from sofia_lite.middleware import voice_transcript

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize components
orchestrator = Orchestrator()
# loop_guard = LoopGuard()  # Removed - not implemented

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
    """Unified handler for incoming messages using Sofia Lite core"""
    
    # Use new orchestrator
    result = orchestrator.process_message(phone, text, channel)
    return result["reply"]

@router.post("/webhook")
async def whatsapp_webhook(
    request: Request,
    From: str = Form(...),
    Body: str = Form(None),
    To: str = Form(...),
    MediaUrl0: str = Form(None),
    NumMedia: str = Form("0"),
    MediaContentType0: str = Form(None)
):
    """WhatsApp webhook handler - F22 support for voice notes"""
    
    logger.info(f"📱 WhatsApp webhook - From: {From}, Body: {Body}, Media: {NumMedia}, Type: {MediaContentType0}")
    
    try:
        # Skip Twilio validation if TEST_WEBHOOK is enabled
        if not TEST_WEBHOOK:
            # TODO: Add Twilio signature validation here if needed
            pass
        
        # Extract phone number
        phone = From.replace("whatsapp:", "")
        
        # Load context for language hint
        ctx = load_context(phone) or Context(phone)
        
        # Handle media (voice notes or payment receipt)
        if NumMedia and int(NumMedia) > 0 and MediaUrl0:
            media_type = MediaContentType0
            
            if media_type and media_type.startswith("audio/"):
                # F22: Handle voice notes
                logger.info(f"🎤 Processing voice note: {MediaUrl0}")
                try:
                    # Usa lingua già stimata, se disponibile
                    lang_hint = ctx.lang if ctx.lang and ctx.lang != "unknown" else None
                    user_msg = voice_transcript.transcribe_voice(MediaUrl0, lang_hint)
                    logger.info(f"✅ Voice transcription: '{user_msg[:50]}...'")
                except Exception as e:
                    logger.error(f"❌ Voice transcription failed: {e}")
                    user_msg = "Mi dispiace, non sono riuscito a trascrivere l'audio. Puoi scrivere il messaggio?"
            else:
                # Handle image (payment receipt)
                logger.info(f"📸 Processing image: {MediaUrl0}")
                ctx.slots["payment_image_url"] = MediaUrl0
                save_context(ctx)
                user_msg = "image"
        else:
            # Handle text message
            user_msg = Body or ""
        
        # Process message through orchestrator
        reply = handle_incoming(phone, user_msg, "whatsapp")
        
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