"""
Sofia AI - Utils NLP
Funzioni unificate per Natural Language Processing
"""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def extract_name_from_input(user_message: str) -> Optional[str]:
    """Estrae il nome dall'input dell'utente - UNIFICATO"""
    
    if not user_message:
        return None
    
    logger.info(f"🔍 Estrazione nome da: {user_message[:50]}...")
    
    # Rimuovi caratteri speciali e normalizza
    clean_message = re.sub(r'[^\w\s]', ' ', user_message.lower())
    words = clean_message.split()
    
    # Lista di parole comuni da ignorare - ESPANSA
    common_words = {
        'mi', 'chiamo', 'sono', 'il', 'la', 'di', 'da', 'del', 'della', 'dello',
        'della', 'dei', 'delle', 'a', 'al', 'alla', 'allo', 'ai', 'agli', 'alle',
        'in', 'nel', 'nella', 'nello', 'nei', 'negli', 'nelle', 'con', 'su', 'sul',
        'sulla', 'sullo', 'sui', 'sugli', 'sulle', 'per', 'tra', 'fra', 'e', 'o',
        'ma', 'se', 'che', 'chi', 'cosa', 'come', 'dove', 'quando', 'perché',
        'ciao', 'salve', 'buongiorno', 'buonasera', 'grazie', 'prego', 'scusa',
        'piacere', 'conoscere', 'chiamare', 'dire', 'parlare', 'aiutare',
        'vorrei', 'potrei', 'posso', 'devo', 'voglio', 'ho', 'bisogno',
        'consulenza', 'appuntamento', 'servizio', 'aiuto', 'informazioni',
        'si', 'no', 'ok', 'perfetto', 'va', 'bene', 'male', 'tutto', 'niente'
    }
    
    # Cerca parole che potrebbero essere nomi (non comuni, lunghezza > 2)
    potential_names = []
    for word in words:
        if (len(word) > 2 and 
            word not in common_words and 
            word.isalpha() and
            (word[0].isupper() or word.islower())):
            potential_names.append(word.title())
    
    # Se trovi un nome, restituiscilo
    if potential_names:
        extracted_name = potential_names[0]
        logger.info(f"✅ Nome estratto: {extracted_name}")
        return extracted_name
    
    # Se non trova nomi, controlla se c'è un nome singolo (ma non parole comuni)
    if len(words) == 1 and words[0].isalpha() and len(words[0]) > 2 and words[0].lower() not in common_words:
        single_name = words[0].title()
        logger.info(f"✅ Nome singolo estratto: {single_name}")
        return single_name
    
    logger.info("ℹ️ Nessun nome estratto")
    return None

def normalize_phone(phone: str) -> str:
    """Normalizza il numero di telefono"""
    
    # Rimuovi spazi, trattini, parentesi
    clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Aggiungi + se manca
    if not clean_phone.startswith('+'):
        if clean_phone.startswith('39'):
            clean_phone = '+' + clean_phone
        elif clean_phone.startswith('0'):
            clean_phone = '+39' + clean_phone[1:]
        else:
            clean_phone = '+39' + clean_phone
    
    return clean_phone

def clean_message(message: str) -> str:
    """Pulisce il messaggio da caratteri speciali"""
    
    # Rimuovi caratteri di controllo
    clean = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', message)
    
    # Normalizza spazi multipli
    clean = re.sub(r'\s+', ' ', clean)
    
    return clean.strip()

def extract_intent_keywords(message: str) -> list:
    """Estrae parole chiave per l'intent"""
    
    message_lower = message.lower()
    keywords = []
    
    # Saluti
    if any(word in message_lower for word in ["ciao", "salve", "buongiorno", "buonasera"]):
        keywords.append("greeting")
    
    # Nomi
    if any(word in message_lower for word in ["mi chiamo", "sono", "chiamo"]):
        keywords.append("name")
    
    # Servizi
    if any(word in message_lower for word in ["servizi", "offrite", "cosa fate", "aiuto"]):
        keywords.append("services")
    
    # Consulenza
    if any(word in message_lower for word in ["consulenza", "appuntamento", "prenota"]):
        keywords.append("consultation")
    
    # Date/orari
    if any(word in message_lower for word in ["quando", "giorni", "orari", "data"]):
        keywords.append("slot")
    
    # Pagamento
    if any(word in message_lower for word in ["costo", "prezzo", "euro", "pagamento"]):
        keywords.append("payment")
    
    # Conferme
    if any(word in message_lower for word in ["grazie", "ok", "perfetto", "confermo"]):
        keywords.append("confirmation")
    
    return keywords 