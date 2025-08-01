from sofia_lite.agents.prompt_builder import build_system_prompt
from sofia_lite.middleware.llm import chat

def run(ctx, user_msg):
    sys = build_system_prompt(ctx)
    user = "Il cliente non ha specificato la modalità di consulenza. Chiedi se preferisce consulenza online o in presenza."
    return chat(sys, user) 