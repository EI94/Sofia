"""
Sofia Lite - Voice Handler
Handles incoming voice calls using the common handler with TTS fallback.
"""

import logging
import os

from fastapi import FastAPI, Form, Request
from fastapi.responses import Response

from .handlers.common import handle_voice_with_fallback

logger = logging.getLogger(__name__)

app = FastAPI(title="Sofia Lite Voice Handler")


@app.post("/webhook/voice")
async def voice_webhook(request: Request):
    """
    Webhook endpoint for Twilio Voice API.
    """
    try:
        # Parse form data
        form_data = await request.form()

        # Extract call data
        phone = form_data.get("From", "")
        transcript = form_data.get("SpeechResult", "")

        if not phone:
            logger.warning("❌ Missing phone in voice webhook")
            return Response(content="Error: Missing phone", status_code=400)

        logger.info(
            f"📞 Voice call from {phone}: {transcript[:50] if transcript else 'No transcript'}..."
        )

        # Process through common handler with TTS fallback
        result = handle_voice_with_fallback(phone, transcript or "ciao")

        # Return TwiML response
        twiml_response = result["twiml"]

        logger.info(f"✅ Voice response sent to {phone}")
        return Response(content=twiml_response, media_type="application/xml")

    except Exception as e:
        logger.error(f"❌ Error in voice webhook: {e}")

        # Fallback TwiML response
        fallback_twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Bianca" rate="medium" pitch="medium">Mi dispiace, si è verificato un errore. Riprova più tardi.</Say>
</Response>"""

        return Response(content=fallback_twiml, media_type="application/xml")


@app.post("/webhook/voice/transcribe")
async def voice_transcribe_webhook(request: Request):
    """
    Webhook endpoint for voice transcription (alternative flow).
    """
    try:
        # Parse form data
        form_data = await request.form()

        # Extract data
        phone = form_data.get("From", "")
        transcript = form_data.get("TranscriptionText", "")
        confidence = form_data.get("TranscriptionConfidence", "0")

        if not phone:
            logger.warning("❌ Missing phone in transcription webhook")
            return Response(content="Error: Missing phone", status_code=400)

        logger.info(
            f"🎤 Voice transcription from {phone}: {transcript[:50]}... (confidence: {confidence})"
        )

        # Process through common handler
        result = handle_voice_with_fallback(phone, transcript or "ciao")

        # Return TwiML response
        twiml_response = result["twiml"]

        logger.info(f"✅ Voice transcription response sent to {phone}")
        return Response(content=twiml_response, media_type="application/xml")

    except Exception as e:
        logger.error(f"❌ Error in voice transcription webhook: {e}")

        # Fallback TwiML response
        fallback_twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Bianca" rate="medium" pitch="medium">Mi dispiace, si è verificato un errore. Riprova più tardi.</Say>
</Response>"""

        return Response(content=fallback_twiml, media_type="application/xml")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "sofia-lite-voice"}


@app.get("/audio/{filename}")
async def serve_audio(filename: str):
    """
    Serve generated audio files.
    """
    audio_path = f"/tmp/{filename}"

    if os.path.exists(audio_path):
        with open(audio_path, "rb") as f:
            audio_data = f.read()
        return Response(content=audio_data, media_type="audio/wav")
    else:
        return Response(content="Audio file not found", status_code=404)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
