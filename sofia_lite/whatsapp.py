"""
Sofia Lite - WhatsApp Handler
Handles incoming WhatsApp messages using the common handler.
"""

import logging
import os

from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse

from .handlers.common import handle_incoming

logger = logging.getLogger(__name__)

app = FastAPI(title="Sofia Lite WhatsApp Handler")


@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    """
    Webhook endpoint for WhatsApp Business API.
    """
    try:
        # Parse form data
        form_data = await request.form()

        # Extract message data
        phone = form_data.get("From", "").replace("whatsapp:", "")
        message = form_data.get("Body", "")

        if not phone or not message:
            logger.warning("❌ Missing phone or message in WhatsApp webhook")
            return JSONResponse(
                content={"error": "Missing required fields"}, status_code=400
            )

        logger.info(f"📱 WhatsApp message from {phone}: {message[:50]}...")

        # Process through common handler
        result = handle_incoming(phone, message, "whatsapp")

        # Return WhatsApp response
        response = {
            "reply": result["reply"],
            "intent": result["intent"],
            "state": result["state"],
            "lang": result["lang"],
        }

        logger.info(f"✅ WhatsApp response sent to {phone}")
        return JSONResponse(content=response)

    except Exception as e:
        logger.error(f"❌ Error in WhatsApp webhook: {e}")
        return JSONResponse(
            content={"error": "Internal server error", "details": str(e)},
            status_code=500,
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "sofia-lite-whatsapp"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
