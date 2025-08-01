from sofia_lite.agents.prompt_builder import build_system_prompt
from sofia_lite.middleware.llm import chat

def run(ctx, user_msg):
    sys = build_system_prompt(ctx)
    user = "Il cliente ha inviato un messaggio che non hai capito bene. Chiedi gentilmente chiarimenti in modo professionale."
    return chat(sys, user) 