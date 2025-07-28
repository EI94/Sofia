from ..policy.language_support import T

def run(ctx,text):
    lowers=text.lower()
    if any(w in lowers for w in ["online","web","zoom","video"]):
        ctx.slots["channel"]="online"
        ctx.state="ASK_PAYMENT"
        return T("ask_payment",ctx.lang)
    if any(w in lowers for w in ["presenza","office","ufficio"]):
        ctx.slots["channel"]="office"
        ctx.state="ASK_SLOT"
        return T("ask_slot",ctx.lang)
    return T("ask_channel",ctx.lang) 