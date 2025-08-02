from sofia_lite.agents.prompt_builder import build_system_prompt
from sofia_lite.middleware.llm import chat

def run(ctx, user_msg):
    sys = build_system_prompt(ctx)
    user = "L'utente ti ha chiesto 'chi sei?'. Presentati come Sofia, l'assistente virtuale dello Studio Immigrato, e spiega brevemente come puoi aiutarlo con i servizi di immigrazione."
    return chat(sys, user) 