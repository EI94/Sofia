from .context import Context
from importlib import import_module
_ROUTE = {          # intent → skill module
    "GREET":"greet_user",
    "ASK_NAME":"ask_name",
    "ASK_SERVICE":"ask_service",
    "PROPOSE_CONSULT":"propose_consult",
    "ASK_CHANNEL":"propose_consult",
    "ASK_SLOT":"ask_slot",
    "ASK_PAYMENT":"ask_payment",
    "CONFIRM":"confirm_booking",
    "ROUTE_ACTIVE":"route_active",
    "CLARIFY":"clarify",
}

def dispatch(intent,ctx,text):
    # Special case: if validator forced ASK_NAME but we're in GREETING state,
    # we should call greet_user first to set the state, then ask_name
    if intent == "ASK_NAME" and ctx.state == "GREETING":
        greet_mod = import_module(f"app.skills.greet_user")
        greet_mod.run(ctx,text)  # Set state to ASK_NAME
        ask_mod = import_module(f"app.skills.ask_name")
        return ask_mod.run(ctx,text)  # Ask for name
    
    mod = import_module(f"app.skills.{_ROUTE[intent]}")
    return mod.run(ctx,text) 