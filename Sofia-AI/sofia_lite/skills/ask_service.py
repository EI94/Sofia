from ..policy.language_support import T
from ..policy.exclusions import is_excluded
def run(ctx,text):
    if is_excluded(text, ctx.lang):
        return T("service_excluded",ctx.lang)
    lowers=text.lower()
    if any(k in lowers for k in ["permesso","residence","permit"]):
        ctx.slots["service"]="permesso"
    elif any(k in lowers for k in ["cittadinanza","citizenship"]):
        ctx.slots["service"]="cittadinanza"
    elif any(k in lowers for k in ["ricongiung","family"]):
        ctx.slots["service"]="ricongiungimento"
    if "service" in ctx.slots:
        ctx.state="PROPOSE_CONSULT"
        return T("propose_consult",ctx.lang).format(name=ctx.name or "")
    return T("ask_service",ctx.lang) 