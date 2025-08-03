from sofia_lite.agents.prompt_builder import build_intent_specific_prompt
from sofia_lite.middleware.llm import chat

def run(ctx, user_msg):
    sys = build_intent_specific_prompt(ctx, "ASK_CHANNEL")
    user = "Il cliente non ha specificato la modalità di consulenza. Chiedi se preferisce consulenza online o in presenza."
    return chat(sys, user) 