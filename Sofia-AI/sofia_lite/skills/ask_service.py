import logging
from sofia_lite.agents.prompt_builder import build_intent_specific_prompt
from sofia_lite.middleware.llm import chat
from ..policy.exclusions import is_excluded

log = logging.getLogger("sofia.ask_service")

def run(ctx, text):
    log.info(f"🚀 ASK_SERVICE: Starting with text='{text}'")
    log.info(f"📊 Context: state={ctx.state}, name={ctx.name}, lang={ctx.lang}, slots={getattr(ctx, 'slots', {})}")
    
    if is_excluded(text, ctx.lang):
        log.info(f"❌ Service excluded: {text}")
        sys = build_intent_specific_prompt(ctx, "ASK_SERVICE")
        user = "Il cliente ha fatto una richiesta che non possiamo soddisfare. Spiega gentilmente che non possiamo aiutare con questo tipo di richieste."
        log.info(f"💬 Excluded service - User prompt: {user}")
        response = chat(sys, user)
        log.info(f"🤖 LLM Response: {response}")
        return response
    
    lowers = text.lower()
    if any(k in lowers for k in ["permesso","residence","permit"]):
        ctx.slots["service"] = "permesso"
    elif any(k in lowers for k in ["cittadinanza","citizenship"]):
        ctx.slots["service"] = "cittadinanza"
    elif any(k in lowers for k in ["ricongiung","family"]):
        ctx.slots["service"] = "ricongiungimento"
    
    if "service" in ctx.slots:
        ctx.state = "PROPOSE_CONSULT"
        log.info(f"✅ Service identified: {ctx.slots['service']}, moving to PROPOSE_CONSULT")
        sys = build_intent_specific_prompt(ctx, "ASK_SERVICE")
        user = f"Il cliente {ctx.name or ''} ha scelto il servizio: {ctx.slots['service']}. Proponi una consulenza specifica per questo servizio."
        log.info(f"💬 Service identified - User prompt: {user}")
        response = chat(sys, user)
        log.info(f"🤖 LLM Response: {response}")
        return response
    
    # Se lang non è italiano, traduci la lista servizi
    if ctx.lang != "it":
        try:
            from ..policy.language_support import get_service_list
            services_text = get_service_list(ctx.lang)
        except ImportError:
            services_text = "permesso di soggiorno, cittadinanza, ricongiungimento familiare"
    else:
        services_text = "permesso di soggiorno, cittadinanza, ricongiungimento familiare"
    
    sys = build_intent_specific_prompt(ctx, "ASK_SERVICE")
    user = f"Il cliente non ha ancora specificato quale servizio desidera. Presenta i servizi disponibili: {services_text}"
    log.info(f"💬 Listing services - User prompt: {user}")
    response = chat(sys, user)
    log.info(f"🤖 LLM Response: {response}")
    return response 