"""
FirestoreMemory class per gestione memoria utenti.
"""

from google.cloud.firestore import AsyncClient
from google.cloud import firestore
import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timezone
import asyncio

logger = logging.getLogger(__name__)


class FirestoreMemory:
    """
    Classe per gestire la memoria degli utenti usando Firestore.
    """
    
    def __init__(self):
        """Inizializza il client Firestore con gestione errori"""
        self.project_id = "sofia-ai-464215"
        self.collection_name = "users"
        self.client = None
        
        # Fallback in-memory per testing
        self._memory_store = {}
        
        # Per il testing, usiamo solo memoria locale
        # TODO: Riabilitare Firestore quando le credenziali sono configurate
        logger.info("🧪 Modalità test: uso memoria locale invece di Firestore")
        
        # try:
        #     self.client = AsyncClient(project=self.project_id)
        #     logger.info("✅ Firestore client inizializzato correttamente")
        # except Exception as e:
        #     logger.warning(f"⚠️ Firestore non disponibile, uso memoria locale: {e}")
        #     self.client = None
    
    async def save_user(self, user_id: str, user_data: Dict[str, Any]) -> bool:
        """
        Salva i dati dell'utente in Firestore.
        
        Args:
            user_id: ID univoco dell'utente (es. numero telefono)
            user_data: Dati dell'utente da salvare
        
        Returns:
            bool: True se salvato con successo
        """
        try:
            doc_ref = self.client.collection(self.collection_name).document(user_id)
            
            # Aggiungi timestamp di aggiornamento
            user_data["updated_at"] = firestore.SERVER_TIMESTAMP
            
            await doc_ref.set(user_data, merge=True)
            
            logger.info(f"Dati utente salvati per {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Errore salvataggio utente {user_id}: {e}")
            return False
    
    async def get_user(self, phone: str) -> Optional[Dict[str, Any]]:
        """
        Recupera i dati di un utente
        """
        try:
            if self.client:
                # Usa Firestore se disponibile
                doc_ref = self.client.collection(self.collection_name).document(phone)
                doc = await doc_ref.get()
                
                if doc.exists:
                    user_data = doc.to_dict()
                    logger.info(f"✅ Utente {phone} trovato in Firestore")
                    return user_data
                else:
                    logger.info(f"ℹ️ Utente {phone} non trovato in Firestore")
                    return None
            else:
                # Fallback in memoria
                user_data = self._memory_store.get(phone)
                if user_data:
                    logger.info(f"✅ Utente {phone} trovato in memoria locale")
                    return user_data
                else:
                    logger.info(f"ℹ️ Utente {phone} non trovato in memoria locale")
                    return None
                    
        except Exception as e:
            logger.error(f"❌ Errore recupero utente {phone}: {e}")
            return None
    
    async def update_user_conversation(self, user_id: str, message: str, response: str) -> bool:
        """
        Aggiorna la cronologia conversazione dell'utente.
        
        Args:
            user_id: ID utente
            message: Messaggio ricevuto
            response: Risposta inviata
        
        Returns:
            bool: True se aggiornato con successo
        """
        try:
            doc_ref = self.client.collection(self.collection_name).document(user_id)
            
            # Aggiungi nuovo scambio di messaggi
            conversation_entry = {
                "timestamp": firestore.SERVER_TIMESTAMP,
                "message": message,
                "response": response
            }
            
            await doc_ref.update({
                "last_conversation": conversation_entry,
                "message_count": firestore.Increment(1)
            })
            
            logger.info(f"Conversazione aggiornata per utente {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Errore aggiornamento conversazione {user_id}: {e}")
            return False
    
    async def upsert_user(self, phone: str, lang: str, case_topic: str = "", payment_status: str = "unpaid") -> bool:
        """
        Inserisce o aggiorna un utente nel database
        """
        try:
            user_data = {
                "phone": phone,
                "lang": lang,
                "case_topic": case_topic,
                "payment_status": payment_status,
                "last_seen": datetime.now(timezone.utc),
                "created_at": datetime.now(timezone.utc)
            }
            
            if self.client:
                # Usa Firestore se disponibile
                doc_ref = self.client.collection(self.collection_name).document(phone)
                await doc_ref.set(user_data, merge=True)
                logger.info(f"✅ Utente {phone} salvato in Firestore")
            else:
                # Fallback in memoria
                self._memory_store[phone] = user_data
                logger.info(f"✅ Utente {phone} salvato in memoria locale")
                
            return True
            
        except Exception as e:
            logger.error(f"❌ Errore salvataggio utente {phone}: {e}")
            return False
    
    async def update_payment(self, phone: str, status: str) -> bool:
        """
        Aggiorna lo stato del pagamento per un utente
        """
        try:
            if self.client:
                # Usa Firestore se disponibile
                doc_ref = self.client.collection(self.collection_name).document(phone)
                await doc_ref.update({
                    "payment_status": status,
                    "payment_updated_at": datetime.now(timezone.utc)
                })
                logger.info(f"✅ Pagamento utente {phone} aggiornato a {status} in Firestore")
            else:
                # Fallback in memoria
                if phone in self._memory_store:
                    self._memory_store[phone]["payment_status"] = status
                    self._memory_store[phone]["payment_updated_at"] = datetime.now(timezone.utc)
                    logger.info(f"✅ Pagamento utente {phone} aggiornato a {status} in memoria locale")
                else:
                    logger.warning(f"⚠️ Utente {phone} non trovato per aggiornamento pagamento")
                    return False
                    
            return True
            
        except Exception as e:
            logger.error(f"❌ Errore aggiornamento pagamento {phone}: {e}")
            return False
    
    async def close(self):
        """Chiude la connessione al client Firestore."""
        if hasattr(self.client, 'close'):
            await self.client.close()
            logger.info("Connessione Firestore chiusa")


# Funzioni di compatibilità per il codice esistente
async def save_message(phone: str, message: str, status: str = "normal") -> bool:
    """Salva un messaggio (stub per compatibilità)"""
    logger.info(f"📝 Messaggio da {phone}: {message} (status: {status})")
    return True 