import logging
from sofia_lite.agents.prompt_builder import build_intent_specific_prompt
from sofia_lite.middleware.llm import chat
from sofia_lite.metrics import clarifies

log = logging.getLogger("sofia.greet_user")

def run(ctx, user_msg):
    log.info(f"🚀 GREET_USER: Starting with user_msg='{user_msg}'")
    log.info(f"📊 Context: state={ctx.state}, name={ctx.name}, lang={ctx.lang}")
    
    sys = build_intent_specific_prompt(ctx, "GREET")
    user = "Il cliente ha appena iniziato la conversazione. Presentati come Sofia di Studio Immigrato e chiedi il suo nome. NON ripetere la presentazione generica 'ciao, sono sofia, l'assistente virtuale di studio immigrato', vai direttamente a chiedere il nome in modo naturale. Usa un formato come 'Ciao! Sono Sofia di Studio Immigrato. Come ti chiami?'"
    
    log.info(f"💬 User prompt: {user}")
    
    # Don't set state here - let the orchestrator handle state transitions
    # ctx.state = "ASK_NAME"  # REMOVED - let orchestrator handle state
    response = chat(sys, user)
    
    # Increment metrics for new clients
    if ctx.client_type == "new":
        clarifies.inc()
    
    log.info(f"🤖 LLM Response: {response}")
    
    return response 