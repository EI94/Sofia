import logging
from context import Context

log = logging.getLogger("sofia.validator")

# 🎯 GOAL-BASED INTENT VALIDATION - Sofia Lite
# Ogni stato accetta solo intent che portano al goal finale
VALID_TRANSITIONS = {
    "GREETING": ["GREET", "ASK_NAME", "ASK_SERVICE"],  # Solo nome o servizio
    "ASK_NAME": ["ASK_NAME", "ASK_SERVICE"],  # Solo nome o servizio
    "ASK_SERVICE": ["ASK_SERVICE", "PROPOSE_CONSULT"],  # Solo servizio o consulenza
    "PROPOSE_CONSULT": ["PROPOSE_CONSULT", "ASK_CHANNEL"],  # Solo consulenza o canale
    "ASK_CHANNEL": ["ASK_CHANNEL", "ASK_SLOT"],  # Solo canale o slot
    "ASK_SLOT": ["ASK_SLOT", "ASK_PAYMENT"],  # Solo slot o pagamento
    "ASK_PAYMENT": ["ASK_PAYMENT", "CONFIRM_BOOKING"],  # Solo pagamento o conferma
    "CONFIRMED": ["CONFIRM_BOOKING"],  # Solo conferma (stato finale)
    "ROUTE_ACTIVE": ["ROUTE_ACTIVE", "ASK_SERVICE"],  # Solo servizio per clienti attivi
    "ASK_CLARIFICATION": ["ASK_NAME", "ASK_SERVICE"]  # Solo nome o servizio
}

def validate(ctx: Context, intent: str, confidence: float = 1.0) -> tuple[str, str, str]:
    """🎯 GOAL-BASED: Validate state→intent transition, return (new_state, intent, warning)"""
    
    # Se confidence < 0.35, forza CLARIFY
    if confidence < 0.35:
        return ("ASK_CLARIFICATION", intent, "LOW_CONFIDENCE")
    
    # 🎯 GOAL-BASED: Usa la logica lineare del planner invece di transizioni complesse
    from planner import next_state
    from state import State
    
    try:
        current_state = State[ctx.state]
        new_state = next_state(current_state, intent, ctx)
        log.info(f"🎯 GOAL: Validated transition {ctx.state} → {new_state.name}")
        return (new_state.name, intent, "OK")
    except Exception as e:
        log.warning(f"🎯 GOAL: Error validating transition {ctx.state} → {intent}: {e}")
        return (ctx.state, intent, "WARN_INVALID_TRANS") 