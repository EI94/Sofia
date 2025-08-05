import logging
from .context import Context

log = logging.getLogger("sofia.validator")

# State → Intent validation matrix
VALID_TRANSITIONS = {
    "GREETING": ["GREET", "ASK_NAME", "ASK_SERVICE", "ROUTE_ACTIVE"],
    "ASK_NAME": ["ASK_NAME", "ASK_SERVICE", "CLARIFY"],
    "ASK_SERVICE": ["ASK_SERVICE", "PROPOSE_CONSULT", "CLARIFY"],
    "PROPOSE_CONSULT": ["PROPOSE_CONSULT", "ASK_CHANNEL", "CLARIFY"],
    "ASK_CHANNEL": ["ASK_CHANNEL", "ASK_SLOT", "CLARIFY"],
    "ASK_SLOT": ["ASK_SLOT", "ASK_PAYMENT", "CONFIRM", "CLARIFY"],
    "ASK_PAYMENT": ["ASK_PAYMENT", "CONFIRM", "CLARIFY"],
    "CONFIRM": ["CONFIRM", "GREETING", "CLARIFY"],
    "ROUTE_ACTIVE": ["ROUTE_ACTIVE", "GREETING", "CLARIFY"],
    "ASK_CLARIFICATION": ["GREET", "ASK_NAME", "ASK_SERVICE", "CLARIFY"]
}

def validate(ctx: Context, intent: str, confidence: float = 1.0) -> tuple[str, str, str]:
    """Validate state→intent transition, return (new_state, intent, warning)"""
    
    # Se confidence < 0.35, forza CLARIFY
    if confidence < 0.35:
        return ("ASK_CLARIFICATION", intent, "LOW_CONFIDENCE")
    
    # Check allowed transitions
    from .state import ALLOWED_TRANSITIONS
    if (ctx.state, intent) in ALLOWED_TRANSITIONS:
        return (ALLOWED_TRANSITIONS[(ctx.state, intent)], intent, "OK")
    
    # Invalid transition - stay in current state
    log.warning("Invalid transition %s→%s", ctx.state, intent)
    return (ctx.state, intent, "WARN_INVALID_TRANS") 