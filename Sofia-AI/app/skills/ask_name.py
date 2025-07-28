from ..policy.language_support import T

def run(ctx,text):
    if ctx.name:   # nome già noto ⇒ salta
        from .ask_service import run as nxt
        return nxt(ctx,text)
    # prova estrazione rapida
    parts = text.split()
    if len(parts)==1 and parts[0].isalpha():
        ctx.name=parts[0].title()
        from .ask_service import run as nxt
        return nxt(ctx,text)
    return T("ask_name",ctx.lang) 