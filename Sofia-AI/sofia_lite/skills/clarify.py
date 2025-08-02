from sofia_lite.agents.prompt_builder import build_system_prompt
from sofia_lite.middleware.llm import chat

def run(ctx, user_msg):
    sys = build_system_prompt(ctx)
    user = f"Il cliente ha inviato questo messaggio: '{user_msg}'. Se è un saluto, presentati come Sofia. Se è una domanda su chi sei, presentati. Se è una richiesta di servizi, chiedi di specificare quale servizio di immigrazione ti serve. Se non capisci, chiedi gentilmente chiarimenti."
    return chat(sys, user) 