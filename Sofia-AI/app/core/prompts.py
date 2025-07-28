"""
Sistema di prompt ottimizzati per Sofia AI
Contiene il ParaHelp template che è il CUORE dell'agent
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# ===== PARAHELP TEMPLATE - IL CUORE DELL'AGENT =====

PARAHELP_SYSTEM_TEMPLATE = """You are **"Sofia"**, the assistant of **Studio Immigrato** ("Via Monte Cengio 5 – ZIP 20145").

**PURPOSE**: Lead "new clients" to a paid 60€ consultation, and guide "active clients" to the Studio Immigrato app.

**RULES**:
• Introduce yourself as Sofia only in the FIRST message
• Tone: warm-professional; female voice, 55-60 years
• Never disclose you are an AI
• Max 2-3 sentences; avoid bullet points
• If offensive → "Your language violates our policy. This conversation is now closed."
• Do not provide detailed legal advice via chat
• Format dates as dd/mm HH:MM and quote fee as "60€"

**ACTIVE CLIENT** (type="attivo"):
• Greet by name if available
• For case status → "You can track your case status in our app: download from Apple Store or Google Play"
• For new service → treat as "New client"

**NEW CLIENT** (type≠"attivo"):
• If asks about services → list AVAILABLE SERVICES
• If specifies service → propose 60€ consultation
• If service in EXCLUSIONS → refuse politely
• For consultation → explain 60€ fee, ask date/time
• For ONLINE → IBAN: IT60X0306234210000002350, upload: https://studioimmigrato.it/upload
• For IN OFFICE → immediate confirmation + address

**AVAILABLE SERVICES**: Residence permits, family reunification, citizenship, immigration procedures

**EXCLUSIONS**: Tourist visas, criminal defence, tax returns, INPS benefits, corporate sponsorships

**LANGUAGES**: it, en, fr, es, ar, hi, ur, bn, wo

**CONTEXT**: {context}

**INSTRUCTION**: {instruction}"""

# ===== TEMPLATE SPECIALIZZATI =====

PAYMENT_INSTRUCTIONS_TEMPLATE = """
Per completare la prenotazione della consulenza online, effettua il bonifico:

IBAN: IT60X0306234210000002350
Causale: "Consulenza immigrazione + [Nome]"
Importo: 60€

Dopo il pagamento, carica la ricevuta su: https://studioimmigrato.it/upload

La consulenza sarà confermata solo dopo la ricezione della ricevuta.
"""

APPOINTMENT_CONFIRMATION_TEMPLATE = """
✅ Appuntamento confermato!

📅 Data: {date}
⏰ Orario: {time}
📍 Modalità: {mode}
💰 Costo: 60€

{mode_instructions}

Per modifiche o cancellazioni, contattaci almeno 24h prima.
"""

# ===== FUNZIONI UTILITY =====

def get_optimized_prompt(
    text: str,
    lang: str = "it",
    context: Optional[Dict[str, Any]] = None,
    action: str = "general",
    instruction: str = "Rispondi in modo appropriato",
    user_state: str = "GREETING",
    turn_count: int = 1,
    user_name: Optional[str] = None,
    last_service: Optional[str] = None,
    conversation_context: str = "",
    phone: Optional[str] = None
) -> Dict[str, str]:
    """Genera prompt ottimizzato per LLM"""
    
    # Prepara contesto
    if context is None:
        context = {
            "user_name": user_name or "non specificato",
            "user_state": user_state,
            "turn_count": turn_count,
            "last_service": last_service or "nessuno",
            "conversation_context": conversation_context,
            "phone": phone or "non specificato"
        }
    
    # Costruisci stringa contesto
    context_str = f"""
Utente: {context.get('user_name', 'non specificato')}
Stato: {context.get('user_state', 'GREETING')}
Turno: {context.get('turn_count', 1)}
Ultimo servizio: {context.get('last_service', 'nessuno')}
Contesto conversazione: {context.get('conversation_context', '')}
Telefono: {context.get('phone', 'non specificato')}
    """.strip()
    
    # Genera prompt finale
    system_prompt = PARAHELP_SYSTEM_TEMPLATE.format(
        context=context_str,
        instruction=instruction
    )
    
    user_prompt = f"Messaggio utente: {text}"
    
    return {
        "system": system_prompt,
        "user": user_prompt
    }

def validate_prompt_size(prompt_dict: Dict[str, str], max_tokens: int = 8000) -> bool:
    """Valida dimensione prompt"""
    total_chars = sum(len(prompt) for prompt in prompt_dict.values())
    estimated_tokens = total_chars // 4  # Stima approssimativa
    return estimated_tokens <= max_tokens

def get_fallback_prompt(text: str, lang: str = "it") -> str:
    """Genera prompt di fallback"""
    return f"""
Sei Sofia, assistente dello Studio Immigrato.
Rispondi in modo professionale e cordiale in {lang}.
Messaggio utente: {text}
"""

def get_template_by_action(action: str, **kwargs) -> str:
    """Restituisce template specifico per azione"""
    if action == "payment_instructions":
        return PAYMENT_INSTRUCTIONS_TEMPLATE
    elif action == "appointment_confirmation":
        return APPOINTMENT_CONFIRMATION_TEMPLATE.format(**kwargs)
    else:
        return "Rispondi in modo appropriato"

def format_prompt_with_context(template: str, **context_vars) -> str:
    """Formatta template con variabili di contesto"""
    try:
        return template.format(**context_vars)
    except KeyError as e:
        logger.warning(f"⚠️ Variabile mancante nel template: {e}")
        return template 