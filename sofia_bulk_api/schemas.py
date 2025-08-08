"""
Pydantic schemas per Sofia Bulk API
"""

from pydantic import BaseModel, Field
from typing import List


class Message(BaseModel):
    """Schema per un singolo messaggio"""

    role: str = Field(..., description="Role del messaggio: 'user' o 'assistant'")
    message: str = Field(..., description="Contenuto del messaggio")


class ConversationIn(BaseModel):
    """Schema per input conversazione"""

    conversation_id: str = Field(..., description="ID univoco della conversazione")
    messages: List[Message] = Field(
        ..., description="Lista dei messaggi della conversazione"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "conv_123",
                "messages": [
                    {"role": "user", "message": "Ciao, mi chiamo Mario"},
                    {"role": "assistant", "message": ""},  # Vuoto per essere completato
                    {
                        "role": "user",
                        "message": "Vorrei informazioni sulla cittadinanza",
                    },
                    {"role": "assistant", "message": ""},  # Vuoto per essere completato
                ],
            }
        }


class ConversationOut(BaseModel):
    """Schema per output conversazione"""

    conversation_id: str = Field(..., description="ID univoco della conversazione")
    messages: List[Message] = Field(..., description="Lista dei messaggi completati")
    timestamp_utc: str = Field(..., description="Timestamp UTC della conversazione")

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "conv_123",
                "messages": [
                    {"role": "user", "message": "Ciao, mi chiamo Mario"},
                    {
                        "role": "assistant",
                        "message": (
                            "Ciao Mario! Sono Sofia di Studio Immigrato. "
                            "Come posso aiutarti?"
                        ),
                    },
                    {
                        "role": "user",
                        "message": "Vorrei informazioni sulla cittadinanza",
                    },
                    {
                        "role": "assistant",
                        "message": (
                            "Perfetto! Ti spiego i requisiti per la "
                            "cittadinanza italiana..."
                        ),
                    },
                ],
                "timestamp_utc": "2025-08-07T12:00:00Z",
            }
        }


class ErrorResponse(BaseModel):
    """Schema per errori API"""

    error: str = Field(..., description="Messaggio di errore")
    detail: str = Field(..., description="Dettagli dell'errore")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Unauthorized",
                "detail": "API key mancante o non valida",
            }
        }
