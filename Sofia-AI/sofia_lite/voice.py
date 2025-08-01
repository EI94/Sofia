from fastapi import APIRouter, Form, Request
from twilio.twiml.voice_response import VoiceResponse
import os
import logging
from sofia_lite.middleware.llm import classify
from sofia_lite.agents.orchestrator import Orchestrator
from sofia_lite.middleware.loop_guard import LoopGuard
from sofia_lite.skills import dispatch
from sofia_lite.agents.context import Context
from sofia_lite.middleware.memory import load_context, save_context

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize components
orchestrator = Orchestrator()
loop_guard = LoopGuard()

def handle_incoming(phone: str, text: str, channel: str = "voice"):
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
    
    # 4 - Check for loops
    loop_check = loop_guard.check_loop(ctx, intent, reply)
    if loop_check["escalate"]:
        logger.warning(f"🔄 Loop detected: {loop_check['reason']}")
        reply = loop_check["message"]
    
    # 5 - Persist context
    save_context(ctx)
    
    return reply

@router.post("/webhook")
async def voice_webhook(
    request: Request,
    From: str = Form(...),
    To: str = Form(...),
    SpeechResult: str = Form(None)
):
    """Voice webhook handler"""
    
    logger.info(f"📞 Voice webhook - From: {From}, Speech: {SpeechResult}")
    
    try:
        # Extract phone number
        phone = From.replace("client:", "")
        
        # Handle incoming message
        if SpeechResult:
            reply = handle_incoming(phone, SpeechResult, "voice")
        else:
            reply = "Ciao! Sono Sofia, l'assistente di Studio Immigrato. Come posso aiutarti?"
        
        # Generate speech response
        speech_url = voice_tts.synthesize_speech(reply, "Polly.Bianca")
        
        # Create TwiML response
        response = VoiceResponse()
        
        if speech_url:
            response.play(speech_url)
        else:
            # Fallback to text-to-speech
            response.say(reply, voice="Polly.Bianca", language="it-IT")
        
        logger.info(f"✅ Voice response generated: {reply}")
        return str(response)
        
    except Exception as e:
        logger.error(f"❌ Error in voice webhook: {e}")
        response = VoiceResponse()
        response.say("Mi dispiace, c'è stato un errore tecnico. Riprova più tardi.", voice="Polly.Bianca", language="it-IT")
        return str(response)
