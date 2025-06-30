"""
Sofia AI Planner - Assistente WhatsApp per Studio Immigrato - VERSIONE CORRETTA
"""

import logging
from app.tools.memory import FirestoreMemory
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import os

logger = logging.getLogger(__name__)
memory = FirestoreMemory()

async def plan(lang: str, intent: str, text: str, phone: str) -> str:
    """
    Sofia AI Planner - Intelligente che NON si ripresenta mai
    """
    try:
        # Recupera dati utente
        user_data = await memory.get_user(phone)
        conversation_count = user_data.get("message_count", 0) if user_data else 0
        
        # CONTROLLO SERVIZI ESCLUSI PRIMA DI TUTTO
        excluded_keywords = ["730", "dichiarazione", "redditi", "fiscale", "contabilità", "unico"]
        if any(keyword.lower() in text.lower() for keyword in excluded_keywords):
            if lang == "en":
                return "I'm sorry, we don't offer tax services. We specialize in immigration: residence permits, family reunification, citizenship."
            else:
                return "Mi dispiace, non offriamo servizi fiscali. Siamo specializzati in immigrazione: permessi di soggiorno, ricongiungimenti familiari, cittadinanza."
        
        # Determina se è il PRIMO messaggio di sempre
        is_first_ever = conversation_count == 0
        
        # Aggiorna contatore messaggi
        await memory.upsert_user(phone, lang, message_count=conversation_count + 1)
        
        # LOGICA INTELLIGENTE SENZA RIPRESENTAZIONI
        if is_first_ever:
            # SOLO il primo messaggio - presentazione
            if lang == "en":
                return "Hi! I'm Sofia from Studio Immigrato. How can I help you with your immigration needs?"
            else:
                return "Ciao! Sono Sofia dello Studio Immigrato. Come posso aiutarti con le tue pratiche di immigrazione?"
        
        else:
            # TUTTI gli altri messaggi - MAI ripresentarsi
            
            # Logica business intelligente
            if any(word in text.lower() for word in ["prenotazione", "appuntamento", "consulenza", "booking", "appointment"]):
                if lang == "en":
                    return "For assistance, I need to schedule an initial consultation (60€ online or in-office). What date and time work for you?"
                else:
                    return "Per assisterti serve una consulenza iniziale di 60€ (online o in studio). Che data e ora preferisci?"
            
            elif any(word in text.lower() for word in ["info", "informazioni", "servizi", "services", "help"]):
                if lang == "en":
                    return "We specialize in residence permits, family reunification, Italian citizenship, and immigration practices. What specific help do you need?"
                else:
                    return "Siamo specializzati in permessi di soggiorno, ricongiungimenti familiari, cittadinanza italiana e pratiche di immigrazione. Di cosa hai bisogno nello specifico?"
            
            elif any(word in text.lower() for word in ["cosa", "what", "dicendo", "saying", "??"]):
                if lang == "en":
                    return "I can help you with immigration matters. What specific service do you need?"
                else:
                    return "Ti posso aiutare con pratiche di immigrazione. Di che servizio specifico hai bisogno?"
            
            else:
                # Risposta generica
                if lang == "en":
                    return "How can I help you with your immigration needs today?"
                else:
                    return "Come posso aiutarti oggi con le tue pratiche di immigrazione?"
        
    except Exception as e:
        logger.error(f"Errore nel planner Sofia AI: {e}")
        # Fallback senza mai ripresentarsi
        if lang == "en":
            return "How can I help you with immigration matters?"
        else:
            return "Come posso aiutarti con le pratiche di immigrazione?" 