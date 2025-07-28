# Wrapper for Firestore memory
from ..gateways.memory import FirestoreMemoryGateway
from ..agents.context import Context

# Create singleton instance
_memory_gateway = FirestoreMemoryGateway()

def load_context(phone: str) -> Context | None:
    """Load context for phone number"""
    try:
        user_data = _memory_gateway.get_user_context(phone)
        if user_data:
            return Context(
                phone=phone,
                lang=user_data.get('lang', 'it'),
                name=user_data.get('name'),
                client_type=user_data.get('client_type', 'new'),
                state=user_data.get('state', 'GREETING'),
                slots=user_data.get('slots', {}),
                history=user_data.get('history', [])
            )
    except Exception:
        pass
    return None

def save_context(ctx: Context):
    """Save context to memory"""
    try:
        user_data = {
            'lang': ctx.lang,
            'name': ctx.name,
            'client_type': ctx.client_type,
            'state': ctx.state,
            'slots': ctx.slots,
            'history': ctx.history
        }
        _memory_gateway.save_user_context(ctx.phone, user_data)
    except Exception:
        pass 