#!/usr/bin/env python3
"""
Script per pulire completamente il database Firebase Firestore in produzione.
Elimina tutti i documenti da tutte le collezioni per avere un'esperienza pulita.
"""

import os
import logging
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_firebase_production():
    """Pulisce completamente il database Firebase Firestore in produzione."""
    
    try:
        # Inizializza il client Firestore
        logger.info("🔧 Inizializzazione client Firestore...")
        db = firestore.Client()
        logger.info("✅ Client Firestore inizializzato")
        
        # Lista delle collezioni principali da pulire
        collections_to_clean = [
            'users',
            'conversations', 
            'conversation_summaries',
            'appointments',
            'documents',
            'notifications',
            'sessions',
            'analytics',
            'logs',
            'temp_data',
            'cache',
            'user_sessions',
            'chat_history',
            'booking_requests',
            'payment_records',
            'service_requests',
            'feedback',
            'system_logs',
            'error_logs',
            'user_preferences',
            'case_status',
            'consultation_requests',
            'payment_confirmations',
            'appointment_confirmations',
            'service_inquiries',
            'client_data',
            'legal_documents',
            'case_files',
            'communication_logs',
            'billing_records'
        ]
        
        total_deleted = 0
        
        # Pulisci collezioni principali
        for collection_name in collections_to_clean:
            try:
                logger.info(f"🧹 Pulizia collezione: {collection_name}")
                collection_ref = db.collection(collection_name)
                
                # Ottieni tutti i documenti
                docs = collection_ref.stream()
                doc_count = 0
                
                for doc in docs:
                    doc.reference.delete()
                    doc_count += 1
                
                total_deleted += doc_count
                logger.info(f"✅ {collection_name}: {doc_count} documenti eliminati")
                
            except Exception as e:
                logger.error(f"❌ Errore pulizia {collection_name}: {e}")
        
        # Ricerca automatica di altre collezioni
        logger.info("🔍 Ricerca collezioni aggiuntive...")
        try:
            collections = db.collections()
            for collection in collections:
                collection_name = collection.id
                if collection_name not in collections_to_clean:
                    logger.info(f"🧹 Pulizia collezione aggiuntiva: {collection_name}")
                    
                    docs = collection.stream()
                    doc_count = 0
                    
                    for doc in docs:
                        doc.reference.delete()
                        doc_count += 1
                    
                    total_deleted += doc_count
                    logger.info(f"✅ {collection_name}: {doc_count} documenti eliminati")
                    
        except Exception as e:
            logger.error(f"❌ Errore ricerca collezioni aggiuntive: {e}")
        
        logger.info(f"🎉 PULIZIA COMPLETATA! Totale documenti eliminati: {total_deleted}")
        logger.info("✅ Database Firebase Firestore completamente pulito")
        logger.info("✨ Esperienza utente pronta per produzione pulita")
        
        return total_deleted
        
    except Exception as e:
        logger.error(f"❌ Errore generale: {e}")
        return 0

if __name__ == "__main__":
    logger.info("🚀 Avvio pulizia database Firebase Firestore in produzione...")
    logger.info("🎯 Obiettivo: Esperienza utente completamente pulita")
    deleted_count = clean_firebase_production()
    logger.info(f"🏁 Pulizia completata. Documenti eliminati: {deleted_count}")
    logger.info("🎉 Database pronto per esperienza utente pulita in produzione!") 