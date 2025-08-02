import json
import os
import logging
from typing import Tuple
from tenacity import retry, stop_after_attempt, wait_exponential
from .prompt_builder import build_system_prompt
from .context import Context
from .state import State
from .. import get_config

log = logging.getLogger("sofia.planner")

# Definizione degli intent con priorità (più alta = più importante)
INTENTS = ["GREET","ASK_NAME","ASK_SERVICE","PROPOSE_CONSULT",
           "ASK_CHANNEL","ASK_SLOT","ASK_PAYMENT","CONFIRM",
           "ROUTE_ACTIVE","CLARIFY","UNKNOWN"]

# Few-shot examples per OpenAI
FEW_SHOT_EXAMPLES = """
Examples:
User: "Ciao!" → Intent: GREET
User: "Hello" → Intent: GREET  
User: "Salve" → Intent: GREET
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

def classify_intent(text: str, lang: str) -> Tuple[str, float]:
    """
    Classifica l'intent del testo usando LLM + similarity fallback.
    
    Args:
        text: Testo da analizzare
        lang: Lingua del testo
        
    Returns:
        Tuple (intent, confidence)
    """
    # In test mode, usa solo similarity
    if os.getenv("TEST_MODE") == "true":
        try:
            intent, confidence = _classify_with_similarity(text)
            log.info(f"🔍 Test mode: similarity classified '{text}' as {intent} (conf: {confidence:.2f})")
            return intent, confidence
        except Exception as e:
            log.error(f"❌ Test mode similarity failed: {e}")
            return "CLARIFY", 0.1
    
    # Primo tentativo: OpenAI
    try:
        intent, confidence = _classify_with_openai(text, lang)
        log.info(f"🤖 OpenAI classified '{text}' as {intent} (conf: {confidence:.2f})")
        return intent, confidence
    except Exception as e:
        log.warning(f"⚠️ OpenAI classification failed: {e}, trying similarity fallback")
        
        # Fallback: similarity
        try:
            intent, confidence = _classify_with_similarity(text)
            log.info(f"🔍 Similarity classified '{text}' as {intent} (conf: {confidence:.2f})")
            return intent, confidence
        except Exception as e2:
            log.error(f"❌ Both OpenAI and similarity failed: {e2}")
            return "CLARIFY", 0.1

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def _classify_with_openai(text: str, lang: str) -> Tuple[str, float]:
    """Classifica intent usando OpenAI con few-shot examples"""
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
        
        # Se similarity < 0.55, ritorna CLARIFY
        if best_similarity < 0.55:
            return "CLARIFY", best_similarity
        
        return best_intent, best_similarity
        
    except Exception as e:
        log.error(f"❌ Similarity classification error: {e}")
        raise

def plan(ctx: Context, user_msg: str, llm) -> tuple[str, str]:
    """
    Returns (intent:str, rationale:str) usando Intent Engine 2.0
    """
    # Classifica intent con confidence
    intent, confidence = classify_intent(user_msg, ctx.lang)
    
    log.info(f"🎯 Intent Engine 2.0: '{user_msg}' → {intent} (conf: {confidence:.2f})")
    
    return intent, f"Intent Engine 2.0: {intent} (confidence: {confidence:.2f})"

def next_state(current_state: State, intent: str) -> State:
    """
    Determine the next state based on current state and intent.
    
    Args:
        current_state: Current conversation state
        intent: Detected user intent
        
    Returns:
        Next state to transition to
    """
    # Intent to state mapping
    intent_to_state = {
        "GREET": State.ASK_NAME,
        "WHO_ARE_YOU": State.GREETING,  # Rimane in GREETING per presentarsi
        "ASK_NAME": State.ASK_SERVICE,
        "ASK_SERVICE": State.PROPOSE_CONSULT,
        "REQUEST_SERVICE": State.ASK_SERVICE,  # Mappa a ASK_SERVICE
        "ASK_COST": State.PROPOSE_CONSULT,     # Mappa a PROPOSE_CONSULT
        "PROPOSE_CONSULT": State.WAIT_SLOT,
        "ASK_CHANNEL": State.WAIT_SLOT,
        "ASK_SLOT": State.WAIT_PAYMENT,
        "ASK_PAYMENT": State.CONFIRMED,
        "CONFIRM": State.CONFIRMED,
        "ROUTE_ACTIVE": State.ASK_SERVICE,
        "CLARIFY": State.ASK_CLARIFICATION,
        "UNKNOWN": State.ASK_CLARIFICATION,
    }
    
    # Get target state from intent
    target_state = intent_to_state.get(intent, State.ASK_CLARIFICATION)
    
    # Validate transition
    from .state import can_transition
    if can_transition(current_state, target_state):
        return target_state
    else:
        # Fallback to clarification if transition is invalid
        return State.ASK_CLARIFICATION 