from sofia_lite.agents.prompt_builder import build_system_prompt
from sofia_lite.middleware.llm import chat
from ..utils.name_extract import extract

def run(ctx, user_msg:str):
    # 1) proviamo ad estrarre il nome sempre
    name = extract(user_msg)
    if name:
        ctx.name = name
        ctx.asked_name = True      # segnala che la domanda è già passata
        ctx.state = "ASK_SERVICE"  # salto al passo successivo
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
        sys = build_system_prompt(ctx)
        user = "Il cliente non ha ancora fornito il suo nome. Chiedigli gentilmente il suo nome."
        return chat(sys, user)

    # 4) abbiamo già chiesto ma l'utente non risponde con nome → chiarimento
    sys = build_system_prompt(ctx)
    user = "Il cliente non ha fornito il suo nome nonostante la richiesta precedente. Chiedi chiarimenti in modo gentile."
    return chat(sys, user) 