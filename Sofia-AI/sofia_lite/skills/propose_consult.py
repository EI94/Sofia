from sofia_lite.agents.prompt_builder import build_intent_specific_prompt
from sofia_lite.middleware.llm import chat
from sofia_lite.metrics import new_leads

def run(ctx, text):
    # Increment new leads metric
    new_leads.inc()
    
    lowers = text.lower()
    if any(w in lowers for w in ["online","web","zoom","video"]):
        ctx.slots["channel"] = "online"
        ctx.state = "ASK_PAYMENT"
        sys = build_intent_specific_prompt(ctx, "PROPOSE_CONSULT")
        user = "Il cliente ha scelto la consulenza online. Spiega il costo di 60€ e chiedi come vuole procedere con il pagamento."
        return chat(sys, user)
    if any(w in lowers for w in ["presenza","office","ufficio"]):
        ctx.slots["channel"] = "office"
        ctx.state = "ASK_SLOT"
        sys = build_intent_specific_prompt(ctx, "PROPOSE_CONSULT")
        user = "Il cliente ha scelto la consulenza in presenza. Proponi i 3 slot orari disponibili: mattina (9-12), pomeriggio (14-17), sera (18-20)."
        return chat(sys, user)
    
    sys = build_intent_specific_prompt(ctx, "PROPOSE_CONSULT")
    user = "Il cliente non ha specificato la modalità di consulenza. Chiedi se preferisce consulenza online o in presenza."
    return chat(sys, user) 