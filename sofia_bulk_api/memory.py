"""
Memory layer per Sofia Bulk API
Default: TinyDB (file JSON locale)
Fallback: Google Firestore se FIRESTORE_PROJECT presente
"""

import os
import json
from typing import Dict, Optional
from pathlib import Path

# TinyDB per storage locale
try:
    from tinydb import TinyDB, Query
    TINYDB_AVAILABLE = True
except ImportError:
    TINYDB_AVAILABLE = False

# Firestore per storage cloud
try:
    from google.cloud import firestore
    FIRESTORE_AVAILABLE = True
except ImportError:
    FIRESTORE_AVAILABLE = False


class MemoryBackend:
    """Abstract base class per memory backends"""
    
    def get_conv(self, cid: str) -> Optional[Dict]:
        """Get conversation by ID"""
        raise NotImplementedError
    
    def upsert_conv(self, cid: str, data: Dict) -> None:
        """Insert or update conversation"""
        raise NotImplementedError


class TinyDBBackend(MemoryBackend):
    """TinyDB backend per storage locale"""
    
    def __init__(self, db_path: str = "./data/conversations.json"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        if TINYDB_AVAILABLE:
            self.db = TinyDB(str(self.db_path))
            self.table = self.db.table('conversations')
        else:
            raise ImportError("TinyDB non disponibile. Installa con: pip install tinydb")
    
    def get_conv(self, cid: str) -> Optional[Dict]:
        """Get conversation by ID"""
        if not TINYDB_AVAILABLE:
            return None
            
        Conversation = Query()
        result = self.table.search(Conversation.conversation_id == cid)
        return result[0] if result else None
    
    def upsert_conv(self, cid: str, data: Dict) -> None:
        """Insert or update conversation"""
        if not TINYDB_AVAILABLE:
            return
            
        Conversation = Query()
        self.table.upsert(data, Conversation.conversation_id == cid)


class FirestoreBackend(MemoryBackend):
    """Firestore backend per storage cloud"""
    
    def __init__(self, project_id: str):
        if not FIRESTORE_AVAILABLE:
            raise ImportError("Firestore non disponibile. Installa con: pip install google-cloud-firestore")
            
        self.db = firestore.Client(project=project_id)
        self.collection = self.db.collection('conversations')
    
    def get_conv(self, cid: str) -> Optional[Dict]:
        """Get conversation by ID"""
        if not FIRESTORE_AVAILABLE:
            return None
            
        doc = self.collection.document(cid).get()
        return doc.to_dict() if doc.exists else None
    
    def upsert_conv(self, cid: str, data: Dict) -> None:
        """Insert or update conversation"""
        if not FIRESTORE_AVAILABLE:
            return
            
        self.collection.document(cid).set(data, merge=True)


def get_memory_backend() -> MemoryBackend:
    """Factory function per creare il backend appropriato"""
    
    # Se FIRESTORE_PROJECT è configurato, usa Firestore
    firestore_project = os.getenv('FIRESTORE_PROJECT')
    if firestore_project and FIRESTORE_AVAILABLE:
        return FirestoreBackend(firestore_project)
    
    # Altrimenti usa TinyDB
    return TinyDBBackend()


# Convenience functions
def get_conv(cid: str) -> Optional[Dict]:
    """Get conversation by ID"""
    backend = get_memory_backend()
    return backend.get_conv(cid)


def upsert_conv(cid: str, data: Dict) -> None:
    """Insert or update conversation"""
    backend = get_memory_backend()
    backend.upsert_conv(cid, data)
