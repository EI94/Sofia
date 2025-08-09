"""
Sofia Lite - Common Handler for Voice & WhatsApp
Unified flow for processing incoming messages from any channel.
"""

import logging
import os
from typing import Any, Dict, Optional

from ..agents.context import Context
from ..agents.orchestrator import Orchestrator
from ..middleware.language import detect
from ..middleware.memory import load_context, save_context
from ..policy.guardrails import abuse_reply, is_inappropriate, warning_reply

logger = logging.getLogger(__name__)


def handle_incoming(phone: str, text: str, channel: str = "whatsapp") -> Dict[str, Any]:
    """
    Unified handler for incoming messages from any channel.

    Args:
        phone: Phone number of the user
        text: Text content (transcript for voice)
        channel: Channel type ("whatsapp" or "voice")

    Returns:
        Dictionary with response data
    """
    try:
        logger.info(f"📥 Incoming message from {phone} via {channel}: {text[:50]}...")

        # Load or create context
        ctx = load_context(phone)
        if not ctx:
            ctx = Context(phone=phone, lang="it", state="GREETING")
            logger.info(f"🆕 New user context created: {phone}")

        # Detect language if not set
        if not ctx.lang or ctx.lang == "unknown":
            ctx.lang = detect(text)
            logger.info(f"🌍 Language detected: {ctx.lang} for {phone}")

        # Check for inappropriate content first
        if is_inappropriate(text):
            abuse_count = ctx.slots.get("abuse_count", 0)
            if abuse_count >= 1:
                # Second abuse - close conversation
                reply = abuse_reply(ctx.lang)
                logger.warning(
                    f"🚫 Conversation closed for {phone} due to repeated abuse"
                )
                return {
                    "reply": reply,
                    "intent": "ABUSE_CLOSE",
                    "state": "CLOSED",
                    "lang": ctx.lang,
                    "phone": phone,
                    "channel": channel,
                }
            else:
                # First abuse - warning
                ctx.slots["abuse_count"] = abuse_count + 1
                save_context(ctx)
                reply = warning_reply(ctx.lang)
                logger.warning(f"⚠️ Warning sent to {phone} for inappropriate content")
                return {
                    "reply": reply,
                    "intent": "ABUSE_WARNING",
                    "state": ctx.state,
                    "lang": ctx.lang,
                    "phone": phone,
                    "channel": channel,
                }

        # Process message through orchestrator
        orchestrator = Orchestrator()

        if channel == "voice":
            # Voice channel - return TwiML response
            result = orchestrator.process_voice(phone, text)
            logger.info(f"🎤 Voice response generated for {phone}")
            return {
                "twiml": result["twiml"],
                "reply": result["reply"],
                "intent": result["intent"],
                "state": result["state"],
                "lang": result["lang"],
                "phone": phone,
                "channel": channel,
            }
        else:
            # WhatsApp channel - return text response
            result = orchestrator.process_message(phone, text, channel)
            logger.info(f"💬 WhatsApp response generated for {phone}")
            return {
                "reply": result["reply"],
                "intent": result["intent"],
                "state": result["state"],
                "lang": result["lang"],
                "phone": phone,
                "channel": channel,
            }

    except Exception as e:
        logger.error(f"❌ Error processing message from {phone}: {e}")

        # Fallback response
        fallback_reply = "Mi dispiace, si è verificato un errore. Riprova più tardi."
        if ctx and ctx.lang != "it":
            fallback_reply = "Sorry, an error occurred. Please try again later."

        return {
            "reply": fallback_reply,
            "intent": "ERROR",
            "state": "ERROR",
            "lang": ctx.lang if ctx else "it",
            "phone": phone,
            "channel": channel,
            "error": str(e),
        }


def handle_voice_with_fallback(phone: str, transcript: str) -> Dict[str, Any]:
    """
    Handle voice messages with TTS fallback.

    Args:
        phone: Phone number of the user
        transcript: Voice transcript

    Returns:
        Dictionary with TwiML response and audio file path
    """
    try:
        # Process through common handler
        result = handle_incoming(phone, transcript, "voice")

        # Generate TTS with fallback
        audio_path = generate_tts_with_fallback(result["reply"], result["lang"])

        result["audio_path"] = audio_path
        return result

    except Exception as e:
        logger.error(f"❌ Error in voice handler: {e}")
        return {
            "twiml": """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Bianca" rate="medium" pitch="medium">
        Mi dispiace, si è verificato un errore. Riprova più tardi.
    </Say>
</Response>""",
            "reply": "Mi dispiace, si è verificato un errore. Riprova più tardi.",
            "intent": "ERROR",
            "state": "ERROR",
            "lang": "it",
            "phone": phone,
            "channel": "voice",
            "audio_path": None,
            "error": str(e),
        }


def generate_tts_with_fallback(text: str, lang: str = "it") -> Optional[str]:
    """
    Generate TTS with ElevenLabs fallback to pyttsx3.

    Args:
        text: Text to synthesize
        lang: Language code

    Returns:
        Path to generated audio file or None if failed
    """
    try:
        # Try ElevenLabs first
        from ..middleware.voice_tts import synthesize_speech

        audio_data = synthesize_speech(text)

        if audio_data and len(audio_data) > 0:
            # Save to file
            audio_path = "/tmp/audio.wav"
            with open(audio_path, "wb") as f:
                f.write(audio_data)
            logger.info(f"✅ ElevenLabs TTS generated: {audio_path}")
            return audio_path

    except Exception as e:
        logger.warning(f"⚠️ ElevenLabs TTS failed: {e}")

    try:
        # Fallback to pyttsx3

        import pyttsx3

        engine = pyttsx3.init()

        # Configure voice based on language
        voices = engine.getProperty("voices")
        if voices:
            # Try to find appropriate voice for language
            for voice in voices:
                if lang in voice.languages[0].lower() if voice.languages else "":
                    engine.setProperty("voice", voice.id)
                    break

        # Set properties
        engine.setProperty("rate", 150)
        engine.setProperty("volume", 0.9)

        # Generate audio
        audio_path = "/tmp/audio.wav"
        engine.save_to_file(text, audio_path)
        engine.runAndWait()

        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
            logger.info(f"✅ pyttsx3 TTS fallback generated: {audio_path}")
            return audio_path

    except Exception as e:
        logger.error(f"❌ pyttsx3 TTS fallback failed: {e}")

    return None


def get_channel_specific_response(
    result: Dict[str, Any], channel: str
) -> Dict[str, Any]:
    """
    Format response for specific channel.

    Args:
        result: Common handler result
        channel: Channel type

    Returns:
        Channel-specific response
    """
    if channel == "voice":
        # Voice channel needs TwiML
        if "twiml" not in result:
            # Generate TwiML from text reply
            twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Bianca" rate="medium" pitch="medium">{result['reply']}</Say>
</Response>"""
            result["twiml"] = twiml

        return {
            "twiml": result["twiml"],
            "audio_path": result.get("audio_path"),
            "reply": result["reply"],
            "intent": result["intent"],
            "state": result["state"],
            "lang": result["lang"],
        }
    else:
        # WhatsApp channel - return text only
        return {
            "reply": result["reply"],
            "intent": result["intent"],
            "state": result["state"],
            "lang": result["lang"],
        }
