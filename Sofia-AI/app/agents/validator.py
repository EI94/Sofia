from .context import Context

# State → Intent validation matrix
VALID_TRANSITIONS = {
    "GREETING": ["GREET", "ASK_NAME", "ROUTE_ACTIVE"],
    "ASK_NAME": ["ASK_NAME", "ASK_SERVICE", "CLARIFY"],
    "ASK_SERVICE": ["ASK_SERVICE", "PROPOSE_CONSULT", "CLARIFY"],
    "PROPOSE_CONSULT": ["PROPOSE_CONSULT", "ASK_CHANNEL", "CLARIFY"],
    "ASK_CHANNEL": ["ASK_CHANNEL", "ASK_SLOT", "CLARIFY"],
    "ASK_SLOT": ["ASK_SLOT", "ASK_PAYMENT", "CLARIFY"],
    "ASK_PAYMENT": ["ASK_PAYMENT", "CONFIRM", "CLARIFY"],
    "CONFIRM": ["CONFIRM", "GREETING", "CLARIFY"],
    "ROUTE_ACTIVE": ["ROUTE_ACTIVE", "GREETING", "CLARIFY"]
}

def validate(ctx: Context, intent: str) -> str:
    """Validate state→intent transition, return CLARIFY if invalid"""
    
    current_state = ctx.state
    valid_intents = VALID_TRANSITIONS.get(current_state, [])
    
    if intent in valid_intents:
        return intent
    else:
        return "CLARIFY" 