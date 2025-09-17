import logging
from agents.prompt_builder import build_intent_specific_prompt
from middleware.llm import chat

log = logging.getLogger("sofia.greet_user")

def run(ctx, user_msg):
    log.info(f"🚀 GREET_USER: Starting with user_msg='{user_msg}'")
    log.info(f"📊 Context: state={ctx.state}, name={ctx.name}, lang={ctx.lang}")
    
    sys = build_intent_specific_prompt(ctx, "GREET")
    user = "Il cliente ha appena iniziato la conversazione. Presentati come Sofia di Studio Immigrato e chiedi il suo nome. NON ripetere la presentazione generica 'ciao, sono sofia, l'assistente virtuale di studio immigrato', vai direttamente a chiedere il nome in modo naturale. Usa un formato come 'Ciao! Sono Sofia di Studio Immigrato. Come ti chiami?' IMPORTANTE: Dopo questo primo messaggio, NON dire mai più 'Sono Sofia dello Studio Immigrato'. CRITICO: Questo è l'UNICO messaggio dove puoi presentarti."
    
    log.info(f"💬 User prompt: {user}")
    
    # Don't set state here - let the orchestrator handle state transitions
    # ctx.state = "ASK_NAME"  # REMOVED - let orchestrator handle state
    response = chat(sys, user)
    
    log.info(f"🤖 LLM Response: {response}")
    
    return response 