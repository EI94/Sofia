# Wrapper for Firestore memory
import logging
import os

from google.cloud import firestore

from .. import get_config
from ..agents.context import Context

log = logging.getLogger("sofia.memory")


class FirestoreMemoryGateway:
    def __init__(self):
        self.db = None
        self._initialized = False

    def _initialize(self):
        """Lazy initialization to avoid premature setup during imports"""
        if self._initialized:
            return

        try:
            # Check for TEST_MODE
            if os.getenv("TEST_MODE") == "true":
                # Use emulator for testing
                project_id = "test-sofia"
                self.db = firestore.Client(project=project_id)
                # Set emulator host if not already set
                if not os.getenv("FIRESTORE_EMULATOR_HOST"):
                    os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
                log.info("✅ Firestore emulator connection established")
            else:
                # Production mode
                cfg = get_config()
                credentials_path = cfg["GOOGLE_CREDENTIALS"]
                if not credentials_path:
                    raise RuntimeError("missing GOOGLE_APPLICATION_CREDENTIALS")

                project_id = cfg["GCLOUD_PROJECT"]
                if not project_id:
                    raise RuntimeError("missing GOOGLE_PROJECT_ID")

                self.db = firestore.Client(project=project_id)
                log.info("✅ Firestore connection established")

            self._initialized = True
        except Exception as e:
            log.error(f"❌ Firestore connection failed: {e}")
            if os.getenv("TEST_MODE") == "true":
                # In test mode, raise SkipTest instead of RuntimeError
                import pytest

                pytest.skip(f"Firestore emulator not available: {e}")
            else:
                raise RuntimeError(f"Firestore initialization failed: {e}")

    def get_user_context(self, phone: str):
        """Get user context from Firestore"""
        if not self._initialized:
            self._initialize()
        if not self.db:
            return None
        try:
            doc = self.db.collection("users").document(phone).get()
            return doc.to_dict() if doc.exists else None
        except Exception as e:
            log.error(f"❌ Firestore get error: {e}")
            return None

    def save_user_context(self, phone: str, user_data: dict):
        """Save user context to Firestore"""
        if not self._initialized:
            self._initialize()
        if not self.db:
            return
        try:
            self.db.collection("users").document(phone).set(user_data)
        except Exception as e:
            log.error(f"❌ Firestore save error: {e}")


# Lazy singleton pattern
_memory_gateway = None


def _get_memory_gateway():
    """Get or create memory gateway singleton"""
    global _memory_gateway
    if _memory_gateway is None:
        _memory_gateway = FirestoreMemoryGateway()
    return _memory_gateway


def load_context(phone: str) -> Context | None:
    """Load context for phone number"""
    try:
        gateway = _get_memory_gateway()
        user_data = gateway.get_user_context(phone)
        if user_data:
            return Context(
                phone=phone,
                lang=user_data.get("lang", "it"),
                name=user_data.get("name"),
                client_type=user_data.get("client_type", "new"),
                state=user_data.get("state", "GREETING"),
                asked_name=user_data.get("asked_name", False),
                slots=user_data.get("slots", {}),
                history=user_data.get("history", []),
            )
    except Exception:
        pass
    return None


def save_context(ctx: Context):
    """Save context to memory"""
    try:
        gateway = _get_memory_gateway()
        user_data = {
            "lang": ctx.lang,
            "name": ctx.name,
            "client_type": ctx.client_type,
            "state": ctx.state,
            "asked_name": ctx.asked_name,
            "slots": ctx.slots,
            "history": ctx.history,
        }
        gateway.save_user_context(ctx.phone, user_data)
    except Exception:
        pass
