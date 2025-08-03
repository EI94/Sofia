import logging
from .context import Context
from importlib import import_module
from ..utils.name_extract import extract_name
from ..middleware.memory import save_context
from ..policy.guardrails import is_inappropriate, abuse_reply, warning_reply

log = logging.getLogger("sofia.executor")
_ROUTE = {          # intent → skill module
    "GREET":"greet_user",
    "WHO_ARE_YOU":"greet_user",       # Map WHO_ARE_YOU to greet_user
    "ASK_NAME":"ask_name",
    "ASK_SERVICE":"ask_service",
    "PROPOSE_CONSULT":"propose_consult",
    "ASK_CHANNEL":"propose_consult",
    "ASK_SLOT":"ask_slot",
    "ASK_PAYMENT":"ask_payment",
    "CONFIRM":"confirm_booking",
    "ROUTE_ACTIVE":"route_active",
    "CLARIFY":"clarify",
    "REQUEST_SERVICE":"ask_service",  # Map REQUEST_SERVICE to ask_service
    "ASK_COST":"propose_consult",     # Map ASK_COST to propose_consult
}

def dispatch(intent, ctx, text):
    log.info(f"🚀 DISPATCH: intent={intent}, state={ctx.state}, text='{text[:50]}...'")
    log.info(f"📊 Context: name={ctx.name}, lang={ctx.lang}, client_type={ctx.client_type}")
    
    # Check for inappropriate content first
    if is_inappropriate(text):
        log.warning(f"⚠️ Inappropriate content detected: {text}")
        abuse_count = ctx.slots.get("abuse_count", 0)
        if abuse_count >= 1:
            # Second abuse - close conversation
            log.error(f"❌ Second abuse, closing conversation")
            return abuse_reply(ctx.lang)
        else:
            # First abuse - warning
            ctx.slots["abuse_count"] = abuse_count + 1
            save_context(ctx)
            log.warning(f"⚠️ First abuse, sending warning")
            return warning_reply(ctx.lang)
    
    # Guard: if client is active and intent is not ROUTE_ACTIVE, force ROUTE_ACTIVE
    if ctx.client_type == "active" and intent not in ["ROUTE_ACTIVE"]:
        intent = "ROUTE_ACTIVE"
        log.info(f"🔄 Active client guard: forcing intent to ROUTE_ACTIVE")
    
    # Reset clarify_count when intent is not CLARIFY
    if intent != "CLARIFY":
        ctx.clarify_count = 0
    
    # Special case: if validator forced ASK_NAME but we're in GREETING state,
    # we should call greet_user first to set the state, then ask_name
    if intent == "ASK_NAME" and ctx.state == "GREETING":
        greet_mod = import_module(f"sofia_lite.skills.greet_user")
        greet_mod.run(ctx, text)  # Set state to ASK_NAME
        ask_mod = import_module(f"sofia_lite.skills.ask_name")
        return ask_mod.run(ctx, text)  # Ask for name
    
    # Extract name when intent is ASK_NAME
    if intent == "ASK_NAME":
        name = extract_name(text, ctx)
        if name:
            ctx.name = name
            save_context(ctx)
    
    try:
        log.info(f"🎯 Importing skill: {_ROUTE[intent]}")
        mod = import_module(f"sofia_lite.skills.{_ROUTE[intent]}")
        response = mod.run(ctx, text)
        
        log.info(f"✅ Skill {_ROUTE[intent]} executed, response: {response[:100]}...")
        
        # Update ctx.state and ctx.stage after skill execution
        _update_context_state(ctx, intent)
        
        # Auto-advance state machine to prevent stuck states
        from .state import auto_advance
        new_state = auto_advance(ctx.state, intent)
        if new_state != ctx.state:
            ctx.state = new_state
            log.info(f"🚀 Auto-advanced state from {ctx.state} to {new_state}")
        
        return response
        
    except Exception as e:
        log.error(f"❌ Error importing skill {_ROUTE[intent]}: {e}")
        return f"Mi dispiace, c'è stato un errore nel processare la tua richiesta: {str(e)}"

def _update_context_state(ctx, intent):
    """Update context state and stage based on intent"""
    from .planner import next_state
    from .state import State, Stage
    
    # Update state
    try:
        current_state = State[ctx.state]
        new_state = next_state(current_state, intent)
        ctx.state = new_state.name
    except Exception as e:
        import logging
        log = logging.getLogger("sofia.executor")
        log.warning(f"⚠️ Error updating state: {e}")
    
    # Update stage based on intent
    stage_mapping = {
        "GREET": "DISCOVERY",
        "ASK_NAME": "DISCOVERY", 
        "ASK_SERVICE": "SERVICE_SELECTION",
        "PROPOSE_CONSULT": "SERVICE_SELECTION",
        "ASK_CHANNEL": "CONSULTATION_SCHEDULED",
        "ASK_SLOT": "CONSULTATION_SCHEDULED",
        "ASK_PAYMENT": "PAYMENT_PENDING",
        "CONFIRM_BOOKING": "COMPLETED",
        "ROUTE_ACTIVE": "SERVICE_SELECTION",
    }
    
    if intent in stage_mapping:
        ctx.stage = stage_mapping[intent] 