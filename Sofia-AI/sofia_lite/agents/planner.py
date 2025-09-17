import json
import os
import logging
import functools
from typing import Tuple
from tenacity import retry, stop_after_attempt, wait_exponential
from prompt_builder import build_system_prompt
from context import Context
from state import State
from __init__ import get_config

log = logging.getLogger("sofia.planner")

# Tiny cache for intent classification (LRU 1024)
_intent_cache = {}
_MAX_CACHE_SIZE = 1024

# Definizione degli intent con priorità (più alta = più importante)
INTENTS = ["GREET","ASK_NAME","ASK_SERVICE","PROPOSE_CONSULT",
           "ASK_CHANNEL","ASK_SLOT","ASK_PAYMENT","CONFIRM",
           "ROUTE_ACTIVE","CLARIFY","WHO_ARE_YOU","REQUEST_SERVICE","ASK_COST","UNKNOWN"]

# Few-shot examples per OpenAI
FEW_SHOT_EXAMPLES = """
Examples:
User: "Ciao!" → Intent: GREET
User: "Hello" → Intent: GREET  
User: "Salve" → Intent: GREET
User: "Buongiorno" → Intent: GREET
User: "Good morning" → Intent: GREET
User: "Buonasera" → Intent: GREET
User: "Good evening" → Intent: GREET
User: "Bonjour" → Intent: GREET
User: "¡Hola!" → Intent: GREET
User: "مرحبا" → Intent: GREET
User: "नमस्ते" → Intent: GREET
User: "السلام علیکم" → Intent: GREET
User: "Chi sei?" → Intent: WHO_ARE_YOU
User: "Who are you?" → Intent: WHO_ARE_YOU
User: "Che servizi offrite?" → Intent: ASK_SERVICE
User: "What services do you offer?" → Intent: ASK_SERVICE
User: "Ho bisogno di un permesso di soggiorno" → Intent: REQUEST_SERVICE
User: "I need a residence permit" → Intent: REQUEST_SERVICE
User: "Quanto costa?" → Intent: ASK_COST
User: "How much does it cost?" → Intent: ASK_COST
User: "Mi chiamo Mario" → Intent: ASK_NAME
User: "My name is John" → Intent: ASK_NAME
User: "Quando hai disponibilità?" → Intent: ASK_SLOT
User: "When are you available?" → Intent: ASK_SLOT
User: "Come posso pagare?" → Intent: ASK_PAYMENT
User: "How can I pay?" → Intent: ASK_PAYMENT
User: "Sì, va bene" → Intent: CONFIRM
User: "Yes, that's fine" → Intent: CONFIRM
User: "Non ho capito" → Intent: CLARIFY
User: "I don't understand" → Intent: CLARIFY
User: "asdfghjkl" → Intent: CLARIFY
"""

def classify_intent(text: str, lang: str, ctx=None) -> Tuple[str, float]:
    """
    Classifica l'intent del testo usando nuova pipeline con cache.
    
    Args:
        text: Testo da analizzare
        lang: Lingua del testo
        ctx: Conversation context (optional, for language caching)
        
    Returns:
        Tuple (intent, confidence)
    """
    import asyncio
    
    # Step 1: Language detection with heuristics
    from middleware.language import detect_lang_with_heuristics
    detected_lang, extra_tag = detect_lang_with_heuristics(text, ctx)
    log.info(f"🌍 Language detected: {detected_lang} for text: '{text[:20]}...'")
    
    # Step 2: Quick greeting heuristic
    if extra_tag == "GREETING_QUICK":
        log.info(f"🚀 Quick greeting heuristic: '{text}' -> GREET")
        return "GREET", 0.99
    
    # FORCE SEQUENCE: If message contains greeting words or name phrases, force GREET intent
    greeting_words = ["ciao", "salve", "buongiorno", "buonasera", "hello", "hi", "bonjour", "hola"]
    name_phrases = ["mi chiamo", "my name is", "je m'appelle", "me llamo"]
    text_lower = text.lower()
    if any(word in text_lower for word in greeting_words) or any(phrase in text_lower for phrase in name_phrases):
        log.info(f"🚀 Force GREET intent for greeting/name message: '{text}'")
        return "GREET", 0.95
    
    # FORCE SEQUENCE: If message starts with greeting, force GREET intent regardless of content
    first_word = text.strip().split()[0].lower() if text.strip() else ""
    if first_word in greeting_words:
        log.info(f"🚀 Force GREET intent for message starting with greeting: '{text}'")
        return "GREET", 0.95
    
    # FORCE SEQUENCE: If message contains greeting words or name phrases anywhere, force GREET intent
    if any(word in text_lower for word in greeting_words) or any(phrase in text_lower for phrase in name_phrases):
        log.info(f"🚀 Force GREET intent for message containing greeting/name: '{text}'")
        return "GREET", 0.95
    
    # Step 3: Execute OpenAI + similarity in parallel
    try:
        # Run both classification methods in parallel
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def parallel_classify():
            tasks = [
                asyncio.create_task(_classify_with_openai_fast_async(text, detected_lang)),
                asyncio.create_task(_classify_with_similarity_async(text))
            ]
            
            # Wait for first result or timeout - Ottimizzato per γ4-a
            done, pending = await asyncio.wait(tasks, timeout=0.8, return_when=asyncio.FIRST_COMPLETED)
            
            # Cancel pending tasks
            for task in pending:
                task.cancel()
            
            if done:
                result = done.pop().result()
                return result
            else:
                raise TimeoutError("Both classification methods timed out")
        
        intent, confidence = loop.run_until_complete(parallel_classify())
        loop.close()
        
        log.info(f"🚀 Parallel classified '{text}' as {intent} (conf: {confidence:.2f})")
        
        # Step 4: Apply confidence threshold
        if confidence < 0.25:
            log.warning(f"⚠️ Low confidence ({confidence:.2f}), falling back to CLARIFY")
            return "CLARIFY", confidence
            
        return intent, confidence
        
    except Exception as e:
        log.warning(f"⚠️ Parallel classification failed: {e}, trying sequential fallback")
        
        # Fallback to sequential execution
        try:
            intent, confidence = _classify_with_openai_fast(text, detected_lang)
            log.info(f"🤖 OpenAI classified '{text}' as {intent} (conf: {confidence:.2f})")
            
            if confidence < 0.25:
                return "CLARIFY", confidence
                
            return intent, confidence
            
        except Exception as e2:
            log.warning(f"⚠️ OpenAI failed: {e2}, trying similarity")
            
            try:
                intent, confidence = _classify_with_similarity(text)
                log.info(f"🔍 Similarity classified '{text}' as {intent} (conf: {confidence:.2f})")
                
                if confidence < 0.25:
                    return "CLARIFY", confidence
                    
                return intent, confidence
                
            except Exception as e3:
                log.error(f"❌ All classification methods failed: {e3}")
                return "CLARIFY", 0.1

@retry(stop=stop_after_attempt(1), wait=wait_exponential(multiplier=1, min=1, max=2))
def _classify_with_openai_fast(text: str, lang: str) -> Tuple[str, float]:
    """Classifica intent usando OpenAI con timeout 0.8s e 1 retry - Ottimizzato γ4-a"""
    try:
        import openai
        import httpx
        cfg = get_config()
        
        # Configure client with timeout
        client = openai.OpenAI(
            api_key=cfg["OPENAI_API_KEY"],
            http_client=httpx.Client(timeout=0.8)  # 0.8 second timeout - Ottimizzato γ4-a
        )
        
        prompt = f"""{FEW_SHOT_EXAMPLES}

Classify the intent of this user message. Respond with JSON only:
{{"intent": "INTENT_NAME", "confidence": 0.95}}

User message: "{text}"
Language: {lang}

JSON response:"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=48  # Reduced for faster response
        )
        
        result = json.loads(response.choices[0].message.content.strip())
        return result["intent"], result["confidence"]
        
    except Exception as e:
        log.error(f"❌ OpenAI fast classification error: {e}")
        raise

async def _classify_with_openai_fast_async(text: str, lang: str) -> Tuple[str, float]:
    """Async version of OpenAI classification"""
    return _classify_with_openai_fast(text, lang)

async def _classify_with_similarity_async(text: str) -> Tuple[str, float]:
    """Async version of similarity classification"""
    return _classify_with_similarity(text)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def _classify_with_openai(text: str, lang: str) -> Tuple[str, float]:
    """Classifica intent usando OpenAI con few-shot examples (legacy)"""
    try:
        import openai
        cfg = get_config()
        client = openai.OpenAI(api_key=cfg["OPENAI_API_KEY"])
        
        prompt = f"""{FEW_SHOT_EXAMPLES}

Classify the intent of this user message. Respond with JSON only:
{{"intent": "INTENT_NAME", "confidence": 0.95}}

User message: "{text}"
Language: {lang}

JSON response:"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=50
        )
        
        result = json.loads(response.choices[0].message.content.strip())
        return result["intent"], result["confidence"]
        
    except Exception as e:
        log.error(f"❌ OpenAI classification error: {e}")
        raise

def _classify_with_similarity(text: str) -> Tuple[str, float]:
    """Classifica intent usando sentence-transformers similarity"""
    try:
        from sentence_transformers import SentenceTransformer
        import numpy as np
        
        # Carica il modello
        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # Carica gli esempi
        examples_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'intent_examples.json')
        with open(examples_path, 'r', encoding='utf-8') as f:
            intent_examples = json.load(f)
        
        # Vettorizza il testo di input
        text_embedding = model.encode([text])[0]
        
        best_intent = "CLARIFY"
        best_similarity = 0.0
        
        # Calcola similarità con tutti gli esempi
        for intent, examples in intent_examples.items():
            if examples:
                example_embeddings = model.encode(examples)
                similarities = np.dot(example_embeddings, text_embedding) / (
                    np.linalg.norm(example_embeddings, axis=1) * np.linalg.norm(text_embedding)
                )
                max_similarity = np.max(similarities)
                
                if max_similarity > best_similarity:
                    best_similarity = max_similarity
                    best_intent = intent
        
        # Se similarity < 0.22, ritorna CLARIFY (abbassato da 0.25)
        if best_similarity < 0.22:
            # Heuristica: se il primo token è una parola di saluto, forza GREET
            GREET_WORDS = {
                "it": ["ciao", "salve", "buongiorno", "buonasera"],
                "en": ["hello", "hi", "good", "hey"],
                "fr": ["bonjour", "salut", "bonsoir"],
                "es": ["hola", "buenos", "buenas"],
                "ar": ["مرحبا", "أهلا", "صباح", "مساء"],
                "hi": ["नमस्ते", "हैलो", "शुभ"],
                "ur": ["السلام", "ہیلو", "صبح", "شام"]
            }
            
            # Estrai la prima parola del testo
            first_word = text.strip().split()[0].lower() if text.strip() else ""
            
            # Controlla se la prima parola è un saluto
            for lang, greet_words in GREET_WORDS.items():
                if any(greet_word in first_word for greet_word in greet_words):
                    log.info(f"🚀 Greeting heuristic: '{first_word}' -> GREET")
                    return "GREET", 0.85
            
            return "CLARIFY", best_similarity
        
        return best_intent, best_similarity
        
    except Exception as e:
        log.error(f"❌ Similarity classification error: {e}")
        raise

def plan(ctx: Context, user_msg: str, llm) -> tuple[str, str]:
    """
    Returns (intent:str, rationale:str) usando Intent Engine 2.0
    """
    # FORCE SEQUENCE: Force GREET intent for any message containing greeting words
    greeting_words = ["ciao", "hello", "buongiorno", "salve", "bonjour", "hola"]
    if any(greeting in user_msg.lower() for greeting in greeting_words):
        log.info(f"🔄 FORCE GREET intent for message containing greeting: '{user_msg}'")
        intent = "GREET"
        confidence = 0.95
    else:
        # Classifica intent con confidence (pass context for language caching)
        intent, confidence = classify_intent(user_msg, ctx.lang, ctx)
    
    log.info(f"🎯 Intent Engine 2.0: '{user_msg}' → {intent} (conf: {confidence:.2f})")
    
    return intent, f"Intent Engine 2.0: {intent} (confidence: {confidence:.2f})"

def next_state(current_state: State, intent: str, ctx=None) -> State:
    """
    🎯 LINEAR GOAL-BASED STATE PLANNER - Sofia Lite
    Determina il prossimo stato basato su obiettivo finale: PRENOTAZIONE CONSULENZA
    LOGICA LINEARE: Ogni stato ha un solo prossimo stato possibile
    
    Args:
        current_state: Stato corrente della conversazione
        intent: Intent rilevato dall'utente
        ctx: Context della conversazione (opzionale)
        
    Returns:
        Prossimo stato verso il goal finale
    """
    
    # 🎯 GOAL: PRENOTAZIONE CONSULENZA
    # Flusso LINEARE: GREETING → ASK_NAME → ASK_SERVICE → PROPOSE_CONSULT → ASK_CHANNEL → ASK_SLOT → ASK_PAYMENT → CONFIRMED
    
    if ctx:
        # 🧠 LINEAR GOAL-BASED LOGIC - Ogni stato avanza solo verso il prossimo
        
        # 1. GREETING → ASK_NAME (sempre, se non abbiamo nome)
        if current_state == State.GREETING:
            if not ctx.name:
                log.info(f"🎯 LINEAR: GREETING → ASK_NAME (no name)")
                return State.ASK_NAME
            else:
                log.info(f"🎯 LINEAR: GREETING → ASK_SERVICE (name present: {ctx.name})")
                return State.ASK_SERVICE
        
        # 2. ASK_NAME → ASK_SERVICE (sempre, dopo aver ottenuto nome)
        if current_state == State.ASK_NAME:
            log.info(f"🎯 LINEAR: ASK_NAME → ASK_SERVICE")
            return State.ASK_SERVICE
        
        # 3. ASK_SERVICE → PROPOSE_CONSULT (sempre, dopo aver ottenuto servizio)
        if current_state == State.ASK_SERVICE:
            log.info(f"🎯 LINEAR: ASK_SERVICE → PROPOSE_CONSULT")
            return State.PROPOSE_CONSULT
        
        # 4. PROPOSE_CONSULT → ASK_CHANNEL (sempre, dopo aver accettato consulenza)
        if current_state == State.PROPOSE_CONSULT:
            log.info(f"🎯 LINEAR: PROPOSE_CONSULT → ASK_CHANNEL")
            return State.ASK_CHANNEL
        
        # 5. ASK_CHANNEL → ASK_SLOT (sempre, dopo aver scelto canale)
        if current_state == State.ASK_CHANNEL:
            log.info(f"🎯 LINEAR: ASK_CHANNEL → ASK_SLOT")
            return State.ASK_SLOT
        
        # 6. ASK_SLOT → ASK_PAYMENT (sempre, dopo aver scelto slot)
        if current_state == State.ASK_SLOT:
            # 🎯 FIX 1: Avanza automaticamente se l'utente conferma lo slot
            if intent in ["ASK_SLOT", "ASK_PAYMENT", "CONFIRM"] or "slot" in intent.lower() or "confermo" in intent.lower():
                log.info(f"🎯 LINEAR: ASK_SLOT → ASK_PAYMENT (user confirmed slot)")
                return State.ASK_PAYMENT
            else:
                log.info(f"🎯 LINEAR: ASK_SLOT → ASK_PAYMENT (default advance)")
                return State.ASK_PAYMENT
        
        # 7. ASK_PAYMENT → CONFIRMED (sempre, dopo aver confermato pagamento)
        if current_state == State.ASK_PAYMENT:
            log.info(f"🎯 LINEAR: ASK_PAYMENT → CONFIRMED")
            return State.CONFIRMED
        
        # 8. CONFIRM → CONFIRMED (sempre, dopo aver confermato tutto)
        if current_state == State.CONFIRM:
            log.info(f"🎯 LINEAR: CONFIRM → CONFIRMED (user confirmed everything)")
            return State.CONFIRMED
        
        # 9. CONFIRMED → CONFIRMED (stato finale, nessuna transizione)
        if current_state == State.CONFIRMED:
            log.info(f"🎯 LINEAR: CONFIRMED → CONFIRMED (final state)")
            return State.CONFIRMED
    
    # 🎯 INTENT TO STATE MAPPING (Linear)
    intent_to_state = {
        "GREET": State.GREETING,
        "ASK_NAME": State.ASK_NAME,
        "ASK_SERVICE": State.ASK_SERVICE,
        "PROPOSE_CONSULT": State.PROPOSE_CONSULT,
        "ASK_CHANNEL": State.ASK_CHANNEL,
        "ASK_SLOT": State.ASK_SLOT,
        "ASK_PAYMENT": State.ASK_PAYMENT,
        "CONFIRM_BOOKING": State.CONFIRMED,
        "ROUTE_ACTIVE": State.ROUTE_ACTIVE,
        "CLARIFY": State.ASK_CLARIFICATION,
        "WHO_ARE_YOU": State.GREETING,
        "REQUEST_SERVICE": State.ASK_SERVICE,
        "ASK_COST": State.PROPOSE_CONSULT,
        "CONFIRM": State.CONFIRMED,
        "UNKNOWN": State.ASK_CLARIFICATION,
    }
    
    # Special handling for INITIAL state
    if current_state == State.INITIAL:
        log.info(f"🎯 LINEAR: INITIAL → GREETING")
        return State.GREETING
    
    # Get target state from intent
    to_state = intent_to_state.get(intent, State.ASK_CLARIFICATION)
    
    # Validate transition
    from state import can_transition
    if can_transition(current_state, to_state):
        return to_state
    else:
        # Fallback to clarification if transition is invalid
        log.warning(f"🎯 LINEAR: Transizione invalida {current_state} → {to_state}, fallback a ASK_CLARIFICATION")
        return State.ASK_CLARIFICATION 