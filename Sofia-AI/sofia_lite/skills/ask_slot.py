from sofia_lite.agents.prompt_builder import build_intent_specific_prompt
from sofia_lite.middleware.llm import chat
from ..middleware.calendar import get_three_slots

def run(ctx, text):
    slots = get_three_slots()
    ctx.slots["candidates"] = slots
    ctx.state = "ASK_SLOT"
    sys = build_intent_specific_prompt(ctx, "ASK_SLOT")
    user = f"Il cliente ha scelto consulenza in presenza. Proponi questi slot orari: {', '.join(f'{i+1}) {s}' for i,s in enumerate(slots))}"
    return chat(sys, user) 