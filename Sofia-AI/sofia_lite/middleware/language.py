"""
Sofia Lite - Language Detection Middleware
"""

import logging
from typing import Optional

log = logging.getLogger("sofia.language")

def detect(text: str) -> str:
    """
    Detect language from text.
    Returns language code (it, en, fr, es, ar, hi, ur, bn)
    """
    try:
        from langdetect import detect as langdetect_detect
        
        # Clean text for better detection
        clean_text = text.strip()[:100]  # Use first 100 chars
        
        if not clean_text:
            return "it"  # Default to Italian
        
        # Detect language
        lang = langdetect_detect(clean_text)
        
        # Map to supported languages
        lang_map = {
            "it": "it",  # Italian
            "en": "en",  # English
            "fr": "fr",  # French
            "es": "es",  # Spanish
            "ar": "ar",  # Arabic
            "hi": "hi",  # Hindi
            "ur": "ur",  # Urdu
            "bn": "bn",  # Bengali
        }
        
        detected_lang = lang_map.get(lang, "it")
        log.info(f"Language detected: {lang} -> {detected_lang}")
        
        return detected_lang
        
    except Exception as e:
        log.warning(f"Language detection failed: {e}, defaulting to Italian")
        return "it"

def get_message(lang: str, key: str) -> str:
    """
    Get localized message.
    """
    messages = {
        "it": {
            "greeting": "Ciao! Sono Sofia, l'assistente virtuale dello Studio Immigrato. Come posso aiutarti?",
            "name_request": "Perfetto! Come ti chiami?",
            "service_request": "Quale servizio ti interessa? Posso aiutarti con: pratiche immigrazione, cittadinanza, permessi di soggiorno, ricongiungimenti familiari.",
            "consultation_request": "Ottimo! Preferisci una consulenza online o in presenza?",
            "slot_request": "Perfetto! Quando preferisci? Ho disponibilità per domani e dopodomani.",
            "confirmation": "Perfetto! Ti confermo l'appuntamento. Riceverai un SMS di conferma.",
            "error": "Mi dispiace, non ho capito. Puoi ripetere?",
            "goodbye": "Grazie per aver contattato lo Studio Immigrato. A presto!"
        },
        "en": {
            "greeting": "Hello! I'm Sofia, the virtual assistant of the Immigration Law Firm. How can I help you?",
            "name_request": "Perfect! What's your name?",
            "service_request": "Which service are you interested in? I can help you with: immigration procedures, citizenship, residence permits, family reunification.",
            "consultation_request": "Great! Do you prefer an online or in-person consultation?",
            "slot_request": "Perfect! When would you prefer? I have availability for tomorrow and the day after.",
            "confirmation": "Perfect! I confirm your appointment. You will receive a confirmation SMS.",
            "error": "I'm sorry, I didn't understand. Can you repeat?",
            "goodbye": "Thank you for contacting the Immigration Law Firm. See you soon!"
        },
        "fr": {
            "greeting": "Bonjour! Je suis Sofia, l'assistante virtuelle du Cabinet d'Immigration. Comment puis-je vous aider?",
            "name_request": "Parfait! Comment vous appelez-vous?",
            "service_request": "Quel service vous intéresse? Je peux vous aider avec: procédures d'immigration, citoyenneté, permis de séjour, regroupement familial.",
            "consultation_request": "Parfait! Préférez-vous une consultation en ligne ou en personne?",
            "slot_request": "Parfait! Quand préférez-vous? J'ai de la disponibilité pour demain et après-demain.",
            "confirmation": "Parfait! Je confirme votre rendez-vous. Vous recevrez un SMS de confirmation.",
            "error": "Je suis désolé, je n'ai pas compris. Pouvez-vous répéter?",
            "goodbye": "Merci d'avoir contacté le Cabinet d'Immigration. À bientôt!"
        },
        "es": {
            "greeting": "¡Hola! Soy Sofia, la asistente virtual del Estudio de Inmigración. ¿Cómo puedo ayudarte?",
            "name_request": "¡Perfecto! ¿Cómo te llamas?",
            "service_request": "¿Qué servicio te interesa? Puedo ayudarte con: trámites de inmigración, ciudadanía, permisos de residencia, reagrupación familiar.",
            "consultation_request": "¡Perfecto! ¿Prefieres una consulta online o presencial?",
            "slot_request": "¡Perfecto! ¿Cuándo prefieres? Tengo disponibilidad para mañana y pasado mañana.",
            "confirmation": "¡Perfecto! Te confirmo la cita. Recibirás un SMS de confirmación.",
            "error": "Lo siento, no he entendido. ¿Puedes repetir?",
            "goodbye": "¡Gracias por contactar con el Estudio de Inmigración. ¡Hasta pronto!"
        }
    }
    
    # Default to Italian if language not supported
    lang_messages = messages.get(lang, messages["it"])
    return lang_messages.get(key, lang_messages["error"]) 