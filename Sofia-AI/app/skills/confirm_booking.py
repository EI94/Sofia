from ..middleware.calendar import book
from ..policy.language_support import T
def run(ctx,text):
    # TODO: extract slot choice from text
    slot = ctx.slots.get("selected_slot", "default")
    success = book(ctx.phone, ctx.name, slot)
    if success:
        ctx.state="CONFIRMED"
    return T("confirm_booking",ctx.lang) 