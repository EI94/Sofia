from ..middleware.calendar import get_three_slots
from ..policy.language_support import T
def run(ctx,text):
    slots = get_three_slots()
    ctx.slots["candidates"]=slots
    ctx.state="ASK_SLOT"
    return T("ask_slot",ctx.lang).format(opts=", ".join(f"{i+1}) {s}" for i,s in enumerate(slots))) 