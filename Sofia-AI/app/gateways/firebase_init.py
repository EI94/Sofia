"""
Inizializzazione Firebase per Sofia AI
Configurazione completa per Firestore e autenticazione
"""

import os
import logging
from typing import Optional
from google.cloud import firestore
from google.auth import default
from google.auth.exceptions import DefaultCredentialsError

logger = logging.getLogger(__name__)

class FirebaseInitializer:
    """Inizializzatore Firebase per Sofia AI"""
    
    def __init__(self):
        self.client: Optional[firestore.Client] = None
        self.project_id: Optional[str] = None
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """Inizializza Firebase Firestore"""
        
        try:
            logger.info("🔧 Inizializzazione Firebase Firestore...")
            
            # 1. Verifica variabili d'ambiente
            self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT') or os.getenv('FIRESTORE_PROJECT_ID')
            
            if not self.project_id:
                logger.warning("⚠️ GOOGLE_CLOUD_PROJECT non trovato, uso default")
                self.project_id = "sofia-ai-464215"  # Default dal progetto
            
            logger.info(f"📋 Project ID: {self.project_id}")
            
            # 2. Inizializza credenziali
            try:
                # In Cloud Run, usa le credenziali del servizio
                credentials, project = default()
                logger.info(f"✅ Credenziali Google Cloud caricate per progetto: {project}")
            except Exception as e:
                logger.error(f"❌ Errore credenziali Google Cloud: {e}")
                logger.info("💡 Assicurati che il servizio abbia le credenziali corrette")
                return False
            
            # 3. Crea client Firestore
            self.client = firestore.Client(project=self.project_id)
            
            # 4. Test connessione
            test_doc = self.client.collection('test').document('connection_test')
            test_doc.set({'timestamp': firestore.SERVER_TIMESTAMP})
            test_doc.delete()  # Pulisci test
            
            self.is_initialized = True
            logger.info("✅ Firebase Firestore inizializzato con successo!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Errore inizializzazione Firebase: {e}")
            self.is_initialized = False
            return False
    
    def get_client(self) -> Optional[firestore.Client]:
        """Restituisce il client Firestore inizializzato"""
        if not self.is_initialized:
            logger.warning("⚠️ Firebase non inizializzato, chiama initialize() prima")
            return None
        return self.client
    
    def is_ready(self) -> bool:
        """Verifica se Firebase è pronto"""
        return self.is_initialized and self.client is not None

# Istanza globale
firebase_initializer = FirebaseInitializer()

def initialize_firebase() -> bool:
    """Funzione helper per inizializzare Firebase"""
    return firebase_initializer.initialize()

def get_firestore_client() -> Optional[firestore.Client]:
    """Funzione helper per ottenere il client Firestore"""
    return firebase_initializer.get_client()

def is_firebase_ready() -> bool:
    """Funzione helper per verificare se Firebase è pronto"""
    return firebase_initializer.is_ready() 