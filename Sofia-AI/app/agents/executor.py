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
    mod = import_module(f"app.skills.{_ROUTE[intent]}")
    return mod.run(ctx,text) 