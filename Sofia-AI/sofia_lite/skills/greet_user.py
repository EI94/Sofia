from sofia_lite.agents.prompt_builder import build_system_prompt
from sofia_lite.middleware.llm import chat

def run(ctx, user_msg):
    sys = build_system_prompt(ctx)
    user = "Il cliente ha appena iniziato la conversazione. Presentati come Sofia di Studio Immigrato e chiedi il suo nome."
    ctx.state = "ASK_NAME"
    return chat(sys, user) 