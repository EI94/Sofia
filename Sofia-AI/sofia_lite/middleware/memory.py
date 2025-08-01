# Wrapper for Firestore memory
import logging
from google.cloud import firestore
from ..agents.context import Context
from .. import get_config

log = logging.getLogger("sofia.memory")

class FirestoreMemoryGateway:
    def __init__(self):
        try:
            # Check for required credentials
            cfg = get_config()
            credentials_path = cfg["GOOGLE_CREDENTIALS"]
            if not credentials_path:
                raise RuntimeError("missing GOOGLE_APPLICATION_CREDENTIALS")
            
            project_id = cfg["GCLOUD_PROJECT"]
            if not project_id:
                raise RuntimeError("missing GOOGLE_PROJECT_ID")
            
            self.db = firestore.Client(project=project_id)
            log.info("✅ Firestore connection established")
        except Exception as e:
            log.error(f"❌ Firestore connection failed: {e}")
            raise RuntimeError(f"Firestore initialization failed: {e}")
    
    def get_user_context(self, phone: str):
        """Get user context from Firestore"""
        if not self.db:
            return None
        try:
            doc = self.db.collection('users').document(phone).get()
            return doc.to_dict() if doc.exists else None
        except Exception as e:
            log.error(f"❌ Firestore get error: {e}")
            return None
    
    def save_user_context(self, phone: str, user_data: dict):
        """Save user context to Firestore"""
        if not self.db:
            return
        try:
            self.db.collection('users').document(phone).set(user_data)
        except Exception as e:
            log.error(f"❌ Firestore save error: {e}")

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
                asked_name=user_data.get('asked_name', False),
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
            'asked_name': ctx.asked_name,
            'slots': ctx.slots,
            'history': ctx.history
        }
        _memory_gateway.save_user_context(ctx.phone, user_data)
    except Exception:
        pass 