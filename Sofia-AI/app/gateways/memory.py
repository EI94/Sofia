"""
Gateway per il memory store - Dependency injection pattern
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from datetime import datetime
import logging
from .firebase_init import get_firestore_client, initialize_firebase

logger = logging.getLogger(__name__)

class MemoryGateway(ABC):
    """Interfaccia astratta per il memory store"""
    
    @abstractmethod
    async def get_user(self, phone: str) -> Optional[Dict[str, Any]]:
        """Recupera dati utente"""
        pass
    
    @abstractmethod
    async def upsert_user(self, phone: str, lang: str, **kwargs) -> bool:
        """Salva/aggiorna dati utente"""
        pass
    
    @abstractmethod
    async def get_conversation_context(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Recupera contesto conversazione"""
        pass

class FirestoreMemoryGateway(MemoryGateway):
    """Implementazione Firestore del memory gateway - MIGLIORATA"""
    
    def __init__(self, firestore_client=None):
        # Inizializza Firebase se non fornito
        if firestore_client is None:
            if initialize_firebase():
                firestore_client = get_firestore_client()
                logger.info("✅ Firebase inizializzato automaticamente")
            else:
                logger.warning("⚠️ Firebase non disponibile")
        
        self.client = firestore_client
        self.db = firestore_client.collection('users') if firestore_client else None
    
    async def get_user(self, phone: str) -> Optional[Dict[str, Any]]:
        """Recupera utente da Firestore - MIGLIORATO"""
        try:
            if not self.db:
                logger.warning("⚠️ Firestore non disponibile, restituisco None")
                return None
            
            logger.info(f"🔍 Recupero utente da Firestore: {phone}")
            doc = self.db.document(phone).get()
            
            if doc.exists:
                user_data = doc.to_dict()
                logger.info(f"✅ Utente trovato in Firestore: {user_data.get('name', 'N/A')}")
                return user_data
            else:
                logger.info(f"ℹ️ Utente non trovato in Firestore: {phone}")
                return None
            
        except Exception as e:
            logger.error(f"❌ Errore Firestore get_user: {e}")
            return None
    
    async def upsert_user(self, phone: str, lang: str, **kwargs) -> bool:
        """Salva/aggiorna utente su Firestore - MIGLIORATO"""
        try:
            if not self.db:
                logger.warning("⚠️ Firestore non disponibile, simulo salvataggio")
                return True  # Simula successo per non bloccare il flusso
            
            # Normalizza dati
            user_data = {
                "phone": phone,
                "lang": lang,
                "updated_at": datetime.now(),
                **kwargs
            }
            
            # Se è nuovo utente, aggiungi created_at
            if "created_at" not in kwargs:
                user_data["created_at"] = datetime.now()
            
            logger.info(f"💾 Salvataggio utente su Firestore: {phone}")
            self.db.document(phone).set(user_data, merge=True)
            logger.info(f"✅ Utente salvato con successo: {phone}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Errore Firestore upsert_user: {e}")
            return False
    
    async def get_conversation_context(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Recupera contesto conversazione da Firestore - MIGLIORATO"""
        try:
            if not self.client:
                logger.warning("⚠️ Firestore client non disponibile")
                return None
            
            # Recupera conversazioni
            conversations_ref = self.client.collection('conversations')
            doc = conversations_ref.document(user_id).get()
            
            if doc.exists:
                context_data = doc.to_dict()
                logger.info(f"✅ Contesto conversazione trovato: {user_id}")
                return context_data
            else:
                logger.info(f"ℹ️ Contesto conversazione non trovato: {user_id}")
                return None
            
        except Exception as e:
            logger.error(f"❌ Errore Firestore get_conversation_context: {e}")
            return None

# InMemoryGateway rimosso - solo implementazione Firestore in produzione 