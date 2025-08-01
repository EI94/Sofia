from sofia_lite.agents.prompt_builder import build_system_prompt
from sofia_lite.middleware.llm import chat
from ..policy.exclusions import is_excluded

def run(ctx, text):
    if is_excluded(text, ctx.lang):
        sys = build_system_prompt(ctx)
        user = "Il cliente ha fatto una richiesta che non possiamo soddisfare. Spiega gentilmente che non possiamo aiutare con questo tipo di richieste."
        return chat(sys, user)
    
    lowers = text.lower()
    if any(k in lowers for k in ["permesso","residence","permit"]):
        ctx.slots["service"] = "permesso"
    elif any(k in lowers for k in ["cittadinanza","citizenship"]):
        ctx.slots["service"] = "cittadinanza"
    elif any(k in lowers for k in ["ricongiung","family"]):
        ctx.slots["service"] = "ricongiungimento"
    
    if "service" in ctx.slots:
        ctx.state = "PROPOSE_CONSULT"
        sys = build_system_prompt(ctx)
        user = f"Il cliente {ctx.name or ''} ha scelto il servizio: {ctx.slots['service']}. Proponi una consulenza specifica per questo servizio."
        return chat(sys, user)
    
    sys = build_system_prompt(ctx)
    user = "Il cliente non ha ancora specificato quale servizio desidera. Presenta i servizi disponibili: permesso di soggiorno, cittadinanza, ricongiungimento familiare."
    return chat(sys, user) 