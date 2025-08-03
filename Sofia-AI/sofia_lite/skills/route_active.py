from sofia_lite.agents.prompt_builder import build_intent_specific_prompt
from sofia_lite.middleware.llm import chat

def run(ctx, user_msg):
    sys = build_intent_specific_prompt(ctx, "ROUTE_ACTIVE")
    user = "Il cliente è un cliente attivo. Salutalo cordialmente e chiedi come può aiutarlo oggi."
    return chat(sys, user) 