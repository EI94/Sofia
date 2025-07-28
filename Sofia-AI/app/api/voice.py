from fastapi import APIRouter, Form, Request
from twilio.twiml.voice_response import VoiceResponse
import os
import logging
from ..middleware import llm, memory, voice_transcript, voice_tts
from ..agents import context, planner, validator, executor
from ..policy import guardrails

router = APIRouter()
logger = logging.getLogger(__name__)

def handle_incoming(phone: str, text: str, channel: str = "voice"):
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
