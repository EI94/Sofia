from sofia_lite.agents.prompt_builder import build_system_prompt
from sofia_lite.middleware.llm import chat

def run(ctx, user_msg):
    sys = build_system_prompt(ctx)
    user = "Il cliente è un cliente attivo. Salutalo cordialmente e chiedi come può aiutarlo oggi."
    return chat(sys, user) 