from sofia_lite.agents.prompt_builder import build_intent_specific_prompt
from sofia_lite.middleware.llm import chat

def run(ctx, user_msg):
    sys = build_intent_specific_prompt(ctx, "GREET")
    user = "L'utente ti ha chiesto 'chi sei?'. Presentati come Sofia, l'assistente virtuale dello Studio Immigrato, e spiega brevemente come puoi aiutarlo con i servizi di immigrazione."
    return chat(sys, user) 