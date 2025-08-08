"""
Sofia Bulk API - FastAPI application
Micro-servizio REST per test bulk conversazioni
"""

import os
import httpx
from datetime import datetime, timezone
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse

from .schemas import ConversationIn, ConversationOut, ErrorResponse, Message
from .memory import get_conv, upsert_conv
from .rate_limiter import rate_limit_10_per_second, get_api_key_limiter, RateLimitExceeded

# Security
security = HTTPBearer()

# Rate limiter
limiter = get_api_key_limiter()

# FastAPI app
app = FastAPI(
    title="Sofia Bulk API",
    description="Micro-servizio REST per test bulk conversazioni Sofia",
    version="1.0.0",
    tags=["Bulk Test"]
)

# Add rate limiter to app
app.state.limiter = limiter

# Rate limit exception handler
@app.exception_handler(RateLimitExceeded)
async def ratelimit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "detail": "Troppe richieste. Limite: 10/second per API key"
        }
    )


def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verifica API key"""
    expected_key = os.getenv("BULK_API_KEY")
    if not expected_key:
        raise HTTPException(
            status_code=500,
            detail="BULK_API_KEY non configurato"
        )
    
    if credentials.credentials != expected_key:
        raise HTTPException(
            status_code=401,
            detail="API key non valida"
        )
    
    return credentials.credentials


async def call_core_sofia(messages: List[Dict[str, str]]) -> str:
    """Chiama il core Sofia per completare un messaggio assistant vuoto"""
    core_url = os.getenv("CORE_SOFIA_URL")
    if not core_url:
        raise HTTPException(
            status_code=500,
            detail="CORE_SOFIA_URL non configurato"
        )
    
    # Costruisci il prompt dalla conversazione
    conversation_text = ""
    for msg in messages:
        if msg["role"] == "user":
            conversation_text += f"User: {msg['message']}\n"
        elif msg["role"] == "assistant" and msg["message"]:
            conversation_text += f"Assistant: {msg['message']}\n"
    
    # Aggiungi l'ultimo messaggio user se presente
    if messages and messages[-1]["role"] == "user":
        conversation_text += f"User: {messages[-1]['message']}\n"
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{core_url}/prompt",
                json={
                    "prompt": conversation_text,
                    "phone": "bulk_test",  # Phone fittizio per bulk test
                    "channel": "bulk"
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("reply", "Mi dispiace, non ho potuto generare una risposta.")
            else:
                return f"Errore Sofia Core: {response.status_code}"
                
    except Exception as e:
        return f"Errore chiamata Sofia Core: {str(e)}"


@app.post(
    "/api/sofia/conversation",
    response_model=ConversationOut,
    responses={
        401: {"model": ErrorResponse},
        429: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    tags=["Bulk Test"]
)
@rate_limit_10_per_second
async def process_conversation(
    request: Request,
    conversation: ConversationIn,
    api_key: str = Depends(verify_api_key)
) -> ConversationOut:
    """
    Processa una conversazione e completa i messaggi assistant vuoti
    
    - **conversation_id**: ID univoco della conversazione
    - **messages**: Lista dei messaggi (user/assistant)
    
    I messaggi assistant con message="" verranno completati chiamando Sofia Core
    """
    
    # Converti in dict per manipolazione
    messages_dict = [msg.model_dump() for msg in conversation.messages]
    
    # Processa ogni messaggio assistant vuoto
    for i, msg in enumerate(messages_dict):
        if msg["role"] == "assistant" and not msg["message"].strip():
            # Chiama Sofia Core per completare il messaggio
            reply = await call_core_sofia(messages_dict[:i])
            messages_dict[i]["message"] = reply
    
    # Crea l'output
    output = ConversationOut(
        conversation_id=conversation.conversation_id,
        messages=[Message(**msg) for msg in messages_dict],
        timestamp_utc=datetime.now(timezone.utc).isoformat()
    )
    
    # Salva nel database
    upsert_conv(
        conversation.conversation_id,
        output.model_dump()
    )
    
    return output


@app.get(
    "/api/sofia/conversation/{cid}",
    response_model=ConversationOut,
    responses={
        404: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        429: {"model": ErrorResponse}
    },
    tags=["Bulk Test"]
)
@rate_limit_10_per_second
async def get_conversation(
    request: Request,
    cid: str,
    api_key: str = Depends(verify_api_key)
) -> ConversationOut:
    """
    Recupera una conversazione salvata
    
    - **cid**: ID della conversazione da recuperare
    """
    
    conversation = get_conv(cid)
    if not conversation:
        raise HTTPException(
            status_code=404,
            detail=f"Conversazione {cid} non trovata"
        )
    
    return ConversationOut(**conversation)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "sofia-bulk-api",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sofia Bulk API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
