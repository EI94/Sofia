import logging
from .context import Context

log = logging.getLogger("sofia.validator")

# State → Intent validation matrix
VALID_TRANSITIONS = {
    "GREETING": ["GREET", "ASK_NAME", "ROUTE_ACTIVE"],
    "ASK_NAME": ["ASK_NAME", "ASK_SERVICE", "CLARIFY"],
    "ASK_SERVICE": ["ASK_SERVICE", "PROPOSE_CONSULT", "CLARIFY"],
    "PROPOSE_CONSULT": ["PROPOSE_CONSULT", "ASK_CHANNEL", "CLARIFY"],
    "ASK_CHANNEL": ["ASK_CHANNEL", "ASK_SLOT", "CLARIFY"],
    "ASK_SLOT": ["ASK_SLOT", "ASK_PAYMENT", "CONFIRM", "CLARIFY"],
    "ASK_PAYMENT": ["ASK_PAYMENT", "CONFIRM", "CLARIFY"],
    "CONFIRM": ["CONFIRM", "GREETING", "CLARIFY"],
    "ROUTE_ACTIVE": ["ROUTE_ACTIVE", "GREETING", "CLARIFY"]
}

def validate(ctx: Context, intent: str, confidence: float = 1.0) -> tuple[str, str, str]:
    """Validate state→intent transition, return (intent, state, warning)"""
    
    # Se confidence < 0.35, forza CLARIFY
    if confidence < 0.35:
        return ("CLARIFY", ctx.state, "LOW_CONFIDENCE")
    
    # Smart name handling: force ASK_NAME if no name and not already asking
    # BUT only if we're in GREETING state and intent is GREET
    if not ctx.name and ctx.state == "GREETING" and intent == "GREET":
        return ("GREET", ctx.state, "")  # Allow GREET to proceed to greet_user
    
    # If ASK_NAME but name already present, go to ASK_SERVICE
    if intent == "ASK_NAME" and ctx.name:
        return ("ASK_SERVICE", ctx.state, "")
    
    current_state = ctx.state
    valid_intents = VALID_TRANSITIONS.get(current_state, [])
    
    if intent in valid_intents:
        return (intent, ctx.state, "")
    else:
        # NON forzare clarifica, ma ritorna warning
        log.warning("Invalid transition %s→%s", ctx.state, intent)
        return (intent, ctx.state, "WARN_INVALID_TRANS") 