"""
EXCLUSIONS Unificato - Sofia AI
Definizione centralizzata dei servizi esclusi per tutti i canali
"""

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

# ===== EXCLUSIONS UNIFICATO - DEFINIZIONE CENTRALE =====

# Lista completa servizi esclusi (definizione autoritativa)
EXCLUDED_SERVICES = [
    {
        "category": "Visti turistici e lettere d'invito",
        "description": "Visti per turismo, lettere d'invito, pratiche consolari turistiche",
        "keywords": ["visto", "tourist", "turismo", "lettera invito", "consolato", "ambasciata", "viaggio"]
    },
    {
        "category": "Difesa penale e processi penali",
        "description": "Assistenza legale penale, difesa in tribunale penale",
        "keywords": ["penale", "processo", "tribunale", "difesa", "avvocato penalista", "reato", "crimine"]
    },
    {
        "category": "Sponsorizzazioni lavoro per aziende",
        "description": "Servizi di sponsorship lavorativo per datori di lavoro",
        "keywords": ["sponsor", "azienda", "datore", "assunzione", "contratto lavoro", "employer", "sponsorship aziendale"]
    },
    {
        "category": "Dichiarazioni dei redditi e fiscale",
        "description": "730, UNICO, consulenza fiscale, contabilità",
        "keywords": ["730", "dichiarazione", "redditi", "fiscale", "contabilità", "unico", "commercialista", "tasse", "caf"]
    },
    {
        "category": "Consulenze commerciali e societarie", 
        "description": "Apertura partita IVA, costituzione società, commerciale",
        "keywords": ["partita iva", "società", "commerciale", "impresa", "business", "srl", "ditta"]
    }
]

# Keywords unificate per detection automatica
EXCLUDED_KEYWORDS = []
for service in EXCLUDED_SERVICES:
    EXCLUDED_KEYWORDS.extend(service["keywords"])

# Lista categories per system prompt
EXCLUDED_CATEGORIES = [service["category"] for service in EXCLUDED_SERVICES]

# ===== FUNZIONI UNIFICATO =====

def is_excluded_service(text: str) -> bool:
    """
    Controlla se il servizio richiesto è escluso
    
    Args:
        text: Testo da analizzare (input utente)
        
    Returns:
        bool: True se servizio escluso, False altrimenti
    """
    if not text:
        return False
        
    text_lower = text.lower()
    
    # Controllo keyword-based unificato
    for keyword in EXCLUDED_KEYWORDS:
        if keyword.lower() in text_lower:
            logger.info(f"🚫 Servizio escluso rilevato: '{keyword}' in '{text[:50]}...'")
            return True
    
    return False


def get_excluded_categories_text(language: str = "it") -> str:
    """
    Restituisce lista formattata dei servizi esclusi
    
    Args:
        language: Codice lingua per localizzazione
        
    Returns:
        str: Testo formattato delle categorie escluse
    """
    if language == "en":
        categories_en = [
            "Tourist visas and invitation letters",
            "Criminal defense and criminal proceedings", 
            "Employment sponsorship for companies",
            "Tax returns and fiscal consulting",
            "Commercial and corporate consulting"
        ]
        return "• " + "\n• ".join(categories_en)
    else:
        # Italiano (default)
        return "• " + "\n• ".join(EXCLUDED_CATEGORIES)


def get_exclusion_response(language: str = "it", channel: str = "whatsapp") -> str:
    """
    Genera risposta unificata per servizi esclusi
    
    Args:
        language: Codice lingua
        channel: Canale (whatsapp, voice)
        
    Returns:
        str: Risposta formattata per il canale
    """
    if language == "en":
        base_response = "I'm sorry, we don't currently offer that service. We specialize in: residence permits, family reunification, Italian citizenship, and immigration procedures."
    elif language == "fr":
        base_response = "Désolé, nous n'offrons pas ce service. Nous sommes spécialisés en: permis de séjour, regroupement familial, citoyenneté italienne, procédures d'immigration."
    elif language == "es":
        base_response = "Lo siento, no ofrecemos ese servicio. Nos especializamos en: permisos de residencia, reagrupación familiar, ciudadanía italiana, trámites de inmigración."
    else:
        # Italiano (default)
        if channel == "voice":
            base_response = "Mi dispiace, al momento non offriamo questo servizio. Siamo specializzati in permessi di soggiorno, ricongiungimenti familiari, cittadinanza italiana e pratiche di immigrazione."
        else:
            base_response = "Mi dispiace, al momento non offriamo questo servizio. Possiamo aiutarti con:\n• Permessi di soggiorno\n• Ricongiungimenti familiari\n• Cittadinanza italiana\n• Pratiche di immigrazione"
    
    return base_response


def get_system_prompt_exclusions() -> str:
    """Restituisce sezione EXCLUSIONS per system prompt unificato"""
    return f"""
────────────────────────────────────────────────────────────────
[ E ]  EXCLUSIONS UNIFICATO (servizi da rifiutare)
────────────────────────────────────────────────────────────────
{get_excluded_categories_text("it")}

**RISPOSTA MODELLO:**
Usa get_exclusion_response() per risposta educata nella lingua dell'utente,
indicando sempre i servizi disponibili (immigrazione).

**DETECTION AUTOMATICA:**
Il sistema rileva automaticamente servizi esclusi tramite keywords unificate.
Non serve controllo manuale - gestione automatica attiva.
────────────────────────────────────────────────────────────────"""


def log_exclusion_stats():
    """Log statistiche configurazione exclusions per debugging"""
    logger.info(f"📊 EXCLUSIONS Config - Categories: {len(EXCLUDED_CATEGORIES)}, Keywords: {len(EXCLUDED_KEYWORDS)}")
    for i, service in enumerate(EXCLUDED_SERVICES, 1):
        logger.info(f"   {i}. {service['category']} ({len(service['keywords'])} keywords)")


# Auto-log configurazione all'import
log_exclusion_stats()

# Export per uso esterno
__all__ = [
    "is_excluded_service",
    "get_excluded_categories_text", 
    "get_exclusion_response",
    "get_system_prompt_exclusions",
    "EXCLUDED_SERVICES",
    "EXCLUDED_KEYWORDS",
    "EXCLUDED_CATEGORIES"
] 