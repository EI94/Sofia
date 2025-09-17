import logging
from agents.prompt_builder import build_intent_specific_prompt
from middleware.llm import chat
from utils.name_extract import extract_name

log = logging.getLogger("sofia.ask_name")

def run(ctx, user_msg:str):
    log.info(f"🎯 ASK_NAME GOAL: Starting with user_msg='{user_msg}'")
    log.info(f"📊 Context: state={ctx.state}, name={ctx.name}, lang={ctx.lang}, asked_name={getattr(ctx, 'asked_name', False)}")
    log.info(f"🔍 DEBUG: Context slots={getattr(ctx, 'slots', {})}, history_len={len(getattr(ctx, 'history', []))}")
    
    # 🎯 GOAL-BASED NAME EXTRACTION
    
    # 1) Estrai nome dal messaggio
    name = extract_name(user_msg, ctx)
    log.info(f"🔍 Extracted name: '{name}' from '{user_msg}'")
    
    if name:
        # Nome estratto con successo
        ctx.name = name
        ctx.asked_name = True
        log.info(f"✅ GOAL: Name extracted '{name}', orchestrator will handle next state")
        log.info(f"🔍 DEBUG: After name extraction - ctx.name={ctx.name}, ctx.slots={getattr(ctx, 'slots', {})}")
        
        # Genera risposta di conferma
        sys = build_intent_specific_prompt(ctx, "ASK_NAME")
        user = f"Il cliente ha fornito il nome '{name}'. Conferma il nome e procedi con il prossimo step. IMPORTANTE: NON dire 'Sono Sofia dello Studio Immigrato' - vai direttamente al punto."
        response = chat(sys, user)
        log.info(f"🤖 LLM Response: {response}")
        log.info(f"🔍 DEBUG: After LLM response - ctx.name={ctx.name}, ctx.slots={getattr(ctx, 'slots', {})}")
        return response

    # 2) Se nome già presente, vai al prossimo step
    if ctx.name:
        log.info(f"✅ GOAL: Name already present '{ctx.name}', moving to next step")
        from ask_service import run as next_skill
        return next_skill(ctx, user_msg)

    # 3) Se non abbiamo ancora chiesto il nome
    if not ctx.asked_name:
        ctx.asked_name = True
        sys = build_intent_specific_prompt(ctx, "ASK_NAME")
        user = "Il cliente non ha ancora fornito il suo nome. Chiedigli gentilmente il suo nome per procedere con la consulenza. IMPORTANTE: NON dire 'Sono Sofia dello Studio Immigrato' - vai direttamente al punto."
        log.info(f"💬 GOAL: Asking for name - User prompt: {user}")
        response = chat(sys, user)
        log.info(f"🤖 LLM Response: {response}")
        return response

    # 4) Abbiamo già chiesto ma l'utente non risponde con nome → chiarimento
    sys = build_intent_specific_prompt(ctx, "ASK_NAME")
    user = "Il cliente non ha fornito il suo nome nonostante la richiesta precedente. Chiedi chiarimenti in modo gentile e spiega che serve il nome per procedere. IMPORTANTE: NON dire 'Sono Sofia dello Studio Immigrato' - vai direttamente al punto."
    log.info(f"💬 GOAL: Clarifying name request - User prompt: {user}")
    response = chat(sys, user)
    log.info(f"🤖 LLM Response: {response}")
    return response

def check_name_before_service(ctx, intent: str) -> str:
    """
    Check if name is needed before proceeding with service request.
    Returns prepend message if name is missing.
    """
    if ctx.name is None and intent in {"ASK_SERVICE", "PROPOSE_CONSULT"}:
        return "Prima di procedere potrei sapere il tuo nome? "
    return "" 