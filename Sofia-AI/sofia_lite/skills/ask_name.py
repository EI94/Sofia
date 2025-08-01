from ..policy.language_support import T
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
        return T("ask_name", ctx.lang)

    # 4) abbiamo già chiesto ma l'utente non risponde con nome → chiarimento
    return T("clarify_name", ctx.lang) 