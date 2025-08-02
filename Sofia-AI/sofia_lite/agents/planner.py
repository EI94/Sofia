import json
import re
from typing import List, Tuple
from .prompt_builder import build_system_prompt
from .context import Context
from .state import State

# Definizione degli intent con priorità (più alta = più importante)
INTENTS = ["GREET","ASK_NAME","ASK_SERVICE","PROPOSE_CONSULT",
           "ASK_CHANNEL","ASK_SLOT","ASK_PAYMENT","CONFIRM",
           "ROUTE_ACTIVE","CLARIFY","UNKNOWN"]

# Pattern regex per classificazione intent
INTENT_PATTERNS = {
    "GREET": [
        r"\b(ciao|hello|hi|hola|bonjour|salve|buongiorno|buonasera)\b",
        r"\b(salve|ciao|hello|hi)\b",
        r"^ciao$",  # Solo "ciao"
        r"^hello$",  # Solo "hello"
        r"^hi$",     # Solo "hi"
    ],
    "REQUEST_SERVICE": [
        r"\b(permesso|soggiorno|cittadinanza|ricongiungimento|familiare)\b",
        r"\b(servizi|aiuto|consulenza|assistenza)\b",
        r"\b(ho bisogno|vorrei|voglio|cerco)\b",
    ],
    "ASK_COST": [
        r"\b(costo|quanto|price|prezzo|60|euro|€)\b",
        r"\b(quanto costa|quanto pagare|prezzo|tariffa)\b",
    ],
    "ASK_NAME": [
        r"\b(mi chiamo|sono|my name is|i'm|je m'appelle|me llamo)\b",
        r"\b(nome|name|chiamare)\b",
    ],
    "ASK_SLOT": [
        r"\b(appuntamento|slot|orario|data|quando|domani|lunedì)\b",
        r"\b(disponibilità|libero|prenotare|prenotazione)\b",
    ],
    "ASK_PAYMENT": [
        r"\b(pagare|pagamento|bonifico|iban|ricevuta)\b",
        r"\b(come pagare|metodo pagamento|trasferimento)\b",
    ],
    "CONFIRM": [
        r"\b(sì|yes|ok|va bene|perfetto|confermo|confermare)\b",
        r"\b(procedere|andare avanti|ok|va bene)\b",
    ],
    "CLARIFY": [
        r"\b(non capisco|non ho capito|ripeti|spiega)\b",
        r"\b(cosa|come|quando|dove|perché)\b",
    ],
    "WHO_ARE_YOU": [
        r"\b(chi sei|who are you|chi ti sei|what are you)\b",
        r"\b(sei|are you|what is your name)\b",
        r"^chi sei\?*$",  # Solo "chi sei?"
        r"^who are you\?*$",  # Solo "who are you?"
    ]
}

def classify_intents(text: str) -> List[str]:
    """
    Classifica tutti gli intent presenti nel testo in ordine di priorità.
    
    Args:
        text: Testo da analizzare
        
    Returns:
        Lista ordinata di intent (più alta priorità = più importante)
    """
    text_lower = text.lower().strip()
    detected_intents = []
    
    # Ordine di priorità degli intent (più alta = più importante)
    priority_order = [
        "WHO_ARE_YOU",      # Priorità alta - domanda su chi è Sofia
        "REQUEST_SERVICE",  # Priorità massima - richiesta servizio
        "ASK_COST",         # Informazioni sui costi
        "ASK_SLOT",         # Richiesta appuntamento
        "ASK_PAYMENT",      # Informazioni pagamento
        "ASK_NAME",         # Fornitura nome
        "CONFIRM",          # Conferma
        "GREET",            # Saluto
        "CLARIFY",          # Chiarimento
    ]
    
    # Cerca tutti gli intent presenti
    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                if intent not in detected_intents:
                    detected_intents.append(intent)
                break  # Trovato un pattern per questo intent, passa al prossimo
    
    # Ordina per priorità
    ordered_intents = []
    for intent in priority_order:
        if intent in detected_intents:
            ordered_intents.append(intent)
    
    # Aggiungi intent non classificati
    for intent in detected_intents:
        if intent not in ordered_intents:
            ordered_intents.append(intent)
    
    return ordered_intents

def plan(ctx: Context, user_msg: str, llm) -> tuple[str, str]:
    """
    Returns (intent:str, rationale:str) usando multi-intent con priorità
    """
    # Prima prova con classificazione regex
    intents = classify_intents(user_msg)
    
    if intents:
        # Prova ogni intent in ordine di priorità
        for intent in intents:
            state = next_state(ctx.state, intent)
            if state and state != State.ASK_CLARIFICATION:
                return intent, f"Multi-intent detected: {intent} (from: {intents})"
    
    # Fallback a LLM se regex non trova nulla
    sys_prompt = build_system_prompt(ctx)
    plan_prompt = f"""{sys_prompt}

You must answer with strict JSON:
{{"intent": "<one_of_{INTENTS}>", "reason": "<short why>"}}

User: \"{user_msg}\"
"""
    
    try:
        rsp = llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": plan_prompt}
        ], model="gpt-4o-mini")
        
        data = json.loads(rsp)
        return data["intent"], data["reason"]
    except Exception as e:
        # Fallback to CLARIFY if parsing fails
        return "CLARIFY", f"Error parsing response: {str(e)}"

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