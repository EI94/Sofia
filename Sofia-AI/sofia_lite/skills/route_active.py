from sofia_lite.agents.prompt_builder import build_intent_specific_prompt
from sofia_lite.middleware.llm import chat
from sofia_lite.metrics import active_redirects

def run(ctx, user_msg):
    # Increment active redirects metric
    active_redirects.inc()
    
    sys = build_intent_specific_prompt(ctx, "ROUTE_ACTIVE")
    user = "Il cliente è un cliente attivo. Salutalo cordialmente e chiedi come può aiutarlo oggi."
    return chat(sys, user) 