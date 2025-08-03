import logging
from ..agents.prompt_builder import build_intent_specific_prompt
from ..middleware.llm import chat
from ..utils.name_extract import extract_name

log = logging.getLogger("sofia.ask_name")

def run(ctx, user_msg:str):
    log.info(f"🚀 ASK_NAME: Starting with user_msg='{user_msg}'")
    log.info(f"📊 Context: state={ctx.state}, name={ctx.name}, lang={ctx.lang}, asked_name={getattr(ctx, 'asked_name', False)}")
    
    # 1) proviamo ad estrarre il nome sempre
    name = extract_name(user_msg, ctx)
    log.info(f"🔍 Extracted name: '{name}' from '{user_msg}'")
    
    if name:
        ctx.name = name
        ctx.asked_name = True      # segnala che la domanda è già passata
        ctx.state = "ASK_SERVICE"  # salto al passo successivo
        log.info(f"✅ Name extracted, moving to ASK_SERVICE")
        from .ask_service import run as next_skill
        return next_skill(ctx, user_msg)

    # 2) se nome già noto → niente domanda ripetuta
    if ctx.name:
        ctx.state = "ASK_SERVICE"
        from .ask_service import run as next_skill
        return next_skill(ctx, user_msg)

    # 3) se non abbiamo ancora chiesto il nome
    if not ctx.asked_name:
        ctx.asked_name = True
        sys = build_intent_specific_prompt(ctx, "ASK_NAME")
        user = "Il cliente non ha ancora fornito il suo nome. Chiedigli gentilmente il suo nome."
        log.info(f"💬 Asking for name - User prompt: {user}")
        response = chat(sys, user)
        log.info(f"🤖 LLM Response: {response}")
        return response

    # 4) abbiamo già chiesto ma l'utente non risponde con nome → chiarimento
    sys = build_intent_specific_prompt(ctx, "ASK_NAME")
    user = "Il cliente non ha fornito il suo nome nonostante la richiesta precedente. Chiedi chiarimenti in modo gentile."
    log.info(f"💬 Clarifying name request - User prompt: {user}")
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