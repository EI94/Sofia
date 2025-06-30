from fastapi import FastAPI, Form
import uvicorn
from app.api import whatsapp, voice


def create_app() -> FastAPI:
    """Factory function per creare l'app FastAPI."""
    app = FastAPI(
        title="Sofia AI",
        description="API per assistente AI con WhatsApp e sintesi vocale",
        version="1.0.0"
    )
    
    # Include router
    app.include_router(whatsapp.router, prefix="/webhook", tags=["WhatsApp"])
    app.include_router(voice.router, prefix="/webhook", tags=["Voice"])
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Endpoint per verificare lo stato dell'applicazione."""
        return {"ok": True}
    
    # Debug endpoint diretto per WhatsApp
    @app.post("/webhook/whatsapp")
    async def debug_whatsapp(From: str = Form(...), Body: str = Form(...)):
        """Debug endpoint per WhatsApp."""
        return {"debug": "endpoint trovato", "from": From, "body": Body}
    
    return app


# Crea l'istanza dell'app
app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 