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
    
    # Load or create context
    ctx = load_context(phone) or Context(phone=phone, lang="it", state="GREETING")
    
    # 1 - Classify intent
    intent, confidence = classify(text, ctx.lang)
    logger.info(f"🎯 Intent: {intent} (confidence: {confidence})")
    
    # 2 - Get next stage from orchestrator
    next_stage = orchestrator.next_stage(ctx, intent)
    logger.info(f"🔄 Stage transition: {ctx.state} → {next_stage}")
    
    # 3 - Execute skill
    reply = dispatch(next_stage, ctx, text)
    logger.info(f"💬 Skill response: {reply[:50]}...")
    
    # 4 - Check for loops (simplified)
    # loop_check = loop_guard.check_loop(ctx, intent, reply)  # Removed - not implemented
    # if loop_check["escalate"]:
    #     logger.warning(f"🔄 Loop detected: {loop_check['reason']}")
    #     reply = loop_check["message"]
    
    # 5 - Persist context
    save_context(ctx)
    
    return reply

@router.post("/webhook")
async def whatsapp_webhook(
    request: Request,
    From: str = Form(...),
    Body: str = Form(None),
    To: str = Form(...),
    MediaUrl0: str = Form(None),
    NumMedia: str = Form("0")
):
    """WhatsApp webhook handler"""
    
    logger.info(f"📱 WhatsApp webhook - From: {From}, Body: {Body}, Media: {NumMedia}")
    
    try:
        # Skip Twilio validation if TEST_WEBHOOK is enabled
        if not TEST_WEBHOOK:
            # TODO: Add Twilio signature validation here if needed
            pass
        
        # Extract phone number
        phone = From.replace("whatsapp:", "")
        
        # Handle media (payment receipt)
        if NumMedia and int(NumMedia) > 0 and MediaUrl0:
            logger.info(f"📸 Processing media: {MediaUrl0}")
            # Store image URL in context for OCR processing
            ctx = memory.load_context(phone) or context.Context(phone)
            ctx.slots["payment_image_url"] = MediaUrl0
            memory.save_context(ctx)
            
            # Process as payment receipt
            reply = handle_incoming(phone, "image", "whatsapp")
        else:
            # Handle text message
            reply = handle_incoming(phone, Body or "", "whatsapp")
        
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