"""
Test App - Completely isolated FastAPI app for testing deployment
"""

import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sofia Lite Test", version="1.0.0")

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Sofia Lite Test is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "sofia-lite-test"}

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    """WhatsApp webhook endpoint."""
    try:
        form_data = await request.form()
        phone = form_data.get("From", "").replace("whatsapp:", "")
        message = form_data.get("Body", "")
        
        logger.info(f"WhatsApp message from {phone}: {message[:50]}...")
        
        # Simple response
        response = {
            "reply": "Ciao! Sono Sofia Lite Test. Il sistema è in fase di configurazione.",
            "intent": "GREET",
            "state": "INITIAL",
            "lang": "it"
        }
        
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"Error in WhatsApp webhook: {e}")
        return JSONResponse(
            content={"error": "Internal server error"},
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Starting Sofia Lite Test on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
