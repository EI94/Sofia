from .greet_user import run as greet_user
from .ask_name import run as ask_name
from .ask_service import run as ask_service
from .propose_consult import run as propose_consult
from .ask_channel import run as ask_channel
from .ask_slot import run as ask_slot
from .ask_payment import run as ask_payment
from .confirm_booking import run as confirm_booking
from .route_active import run as route_active
from .clarify import run as clarify

_MAP = {
    "GREETING": greet_user,
    "ASK_NAME": ask_name,
    "ASK_SERVICE": ask_service,
    "PROPOSE_CONSULT": propose_consult,
    "ASK_CHANNEL": ask_channel,
    "ASK_SLOT": ask_slot,
    "ASK_PAYMENT": ask_payment,
    "CONFIRMED": confirm_booking,
    "ROUTE_ACTIVE": route_active,
    "CLARIFY": clarify,
}

def dispatch(stage: str, ctx, msg: str) -> str:
    return _MAP[stage](ctx, msg) 