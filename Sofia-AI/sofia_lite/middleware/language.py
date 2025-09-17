"""
Sofia Lite - Language Detection Middleware
"""

import logging
import functools
from typing import Optional
from latency import track_latency
from utils.memo import ttl_cache

log = logging.getLogger("sofia.language")

# TTL cache per language detection - Δmini optimization
@ttl_cache(ttl=30, maxsize=256)
def _cached_detect_lang(text: str) -> str:
    """Cached language detection with TTL 1 hour (handled by LRU)"""
    return _detect_lang_impl(text)

def _detect_lang_impl(text: str) -> str:
    """
    Detect language from text with double fallback.
    Returns ISO-2 language code (it, en, fr, es, ar, hi, ur, bn, wo)
    """
    try:
        from langdetect import detect as langdetect_detect
        
        # Clean text for better detection
        clean_text = text.strip()[:100]  # Use first 100 chars
        
        if not clean_text:
            return "it"  # Default to Italian
        
        # Fallback 1: langdetect (fast probabilistic)
        try:
            lang = langdetect_detect(clean_text)
            lang_map = {
                "it": "it",  # Italian
                "en": "en",  # English
                "fr": "fr",  # French
                "es": "es",  # Spanish
                "ar": "ar",  # Arabic
                "hi": "hi",  # Hindi
                "ur": "ur",  # Urdu
                "bn": "bn",  # Bengali
                "wo": "wo",  # Wolof
            }
            
            detected_lang = lang_map.get(lang, None)
            if detected_lang:
                log.info(f"🌍 Langdetect: {lang} -> {detected_lang}")
                return detected_lang
                
        except Exception as e:
            log.warning(f"Langdetect failed: {e}")
        
        # Fallback 2: keyword-based detection
        detected_lang = detect_by_keywords(clean_text)
        if detected_lang:
            log.info(f"🔍 Keyword detection: {detected_lang}")
            return detected_lang
        
        # Fallback 3: default to Italian
        log.warning("All language detection failed, defaulting to Italian")
        return "it"
        
    except Exception as e:
        log.error(f"Language detection completely failed: {e}, defaulting to Italian")
        return "it"

@track_latency("LANG")
def detect_lang(text: str) -> str:
    """
    Detect language from text with micro-cache LRU(512).
    Returns ISO-2 language code (it, en, fr, es, ar, hi, ur, bn, wo)
    """
    # Use cached detection with text[:32] for cache key
    cache_key = text[:32]
    return _cached_detect_lang(cache_key)

def heuristic_lang(text: str) -> Optional[str]:
    """
    Fast heuristic language detection based on first word.
    Returns language code or None if no match.
    """
    if not text.strip():
        return None
    
    # Get first word
    first_word = text.strip().split()[0].lower()
    
    # Greeting words by language
    GREET_WORDS = {
        "it": ["ciao", "salve", "buongiorno", "buonasera"],
        "en": ["hello", "hi", "good", "hey"],
        "fr": ["bonjour", "salut", "bonsoir"],
        "es": ["hola", "buenos", "buenas"],
        "ar": ["مرحبا", "أهلا", "صباح", "مساء"],
        "hi": ["नमस्ते", "हैलो", "शुभ"],
        "ur": ["السلام", "ہیلو", "صبح", "شام"]
    }
    
    # Check if first word matches any greeting
    for lang, greet_words in GREET_WORDS.items():
        if any(greet_word in first_word for greet_word in greet_words):
            log.info(f"🚀 Heuristic lang detection: '{first_word}' -> {lang}")
            return lang
    
    return None

def detect_lang_with_heuristics(text: str, ctx=None) -> tuple[str, Optional[str]]:
    """Detect language with optimistic guess → verify once - γ5 optimization"""
    """
    Detect language with post-detect heuristics and 1-shot cache.
    Returns (lang, extra_tag) where extra_tag can be "GREETING_QUICK"
    """
    # Check 1-shot cache first
    if ctx and ctx.slots.get("lang_confirmed"):
        cached_lang = ctx.slots["lang_confirmed"]
        log.info(f"🔄 Using cached language: {cached_lang}")
        return cached_lang, None
    
    # Try heuristic detection first
    heuristic_result = heuristic_lang(text)
    if heuristic_result:
        # Cache the result for future turns
        if ctx:
            ctx.slots["lang_confirmed"] = heuristic_result
            log.info(f"💾 Cached heuristic language: {heuristic_result}")
        return heuristic_result, "GREETING_QUICK"
    
    # Quick greeting whitelist for ≤3 tokens
    greeting_whitelist = {
        "ciao", "hi", "hola", "bonjour", "هلا", "नमस्ते", "ہیلو", "হাই", "nanga"
    }
    
    # Check if text is a quick greeting (≤3 tokens)
    tokens = text.strip().split()
    if len(tokens) <= 3 and text.strip().lower() in greeting_whitelist:
        # Force language detection for quick greetings
        lang = detect_lang(text)
        log.info(f"🚀 Quick greeting detected: '{text}' -> {lang}")
        return lang, "GREETING_QUICK"
    
    # Normal detection
    lang = detect_lang(text)
    
    # Cache the result for future turns
    if ctx:
        ctx.slots["lang_confirmed"] = lang
        log.info(f"💾 Cached language: {lang}")
    
    return lang, None

def detect_by_keywords(text: str) -> str:
    """
    Keyword-based language detection for 9 languages.
    """
    text_lower = text.lower()
    
    # Italian keywords
    if any(word in text_lower for word in ["ciao", "salve", "buongiorno", "buonasera", "grazie", "per favore", "mi chiamo", "sono"]):
        return "it"
    
    # English keywords
    if any(word in text_lower for word in ["hello", "hi", "good morning", "good evening", "thank you", "please", "my name is", "i am"]):
        return "en"
    
    # French keywords
    if any(word in text_lower for word in ["bonjour", "salut", "bonsoir", "merci", "s'il vous plaît", "je m'appelle", "je suis"]):
        return "fr"
    
    # Spanish keywords
    if any(word in text_lower for word in ["hola", "buenos días", "buenas tardes", "gracias", "por favor", "me llamo", "soy"]):
        return "es"
    
    # Arabic keywords
    if any(word in text_lower for word in ["مرحبا", "أهلا", "صباح الخير", "مساء الخير", "شكرا", "من فضلك", "اسمي", "أنا"]):
        return "ar"
    
    # Hindi keywords
    if any(word in text_lower for word in ["नमस्ते", "हैलो", "शुभ प्रभात", "शुभ संध्या", "धन्यवाद", "कृपया", "मेरा नाम", "मैं"]):
        return "hi"
    
    # Urdu keywords
    if any(word in text_lower for word in ["السلام علیکم", "ہیلو", "صبح بخیر", "شام بخیر", "شکریہ", "براہ کرم", "میرا نام", "میں"]):
        return "ur"
    
    # Bengali keywords
    if any(word in text_lower for word in ["হ্যালো", "নমস্কার", "শুভ সকাল", "শুভ সন্ধ্যা", "ধন্যবাদ", "অনুগ্রহ করে", "আমার নাম", "আমি"]):
        return "bn"
    
    # Wolof keywords
    if any(word in text_lower for word in ["salamalekum", "salam", "bonjour", "merci", "jerejef", "ma naam", "man"]):
        return "wo"
    
    return None

def detect(text: str) -> str:
    """
    Alias for detect_lang for backward compatibility.
    """
    return detect_lang(text)

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