# Wrapper for Firestore memory
import logging
import os
import json
import numpy as np
from typing import List, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
from google.cloud import firestore
from google.oauth2 import service_account
from ..agents.context import Context
from .. import get_config

log = logging.getLogger("sofia.memory")

class VectorStore:
    """Vector store for RAG using FAISS"""
    
    def __init__(self):
        self.index = None
        self.texts = []
        self.metadata = []
        self._initialized = False
    
    def _initialize(self):
        """Lazy initialization of FAISS index"""
        if self._initialized:
            return
            
        try:
            import faiss
            # Create FAISS index for inner product (cosine similarity)
            dimension = 1536  # OpenAI text-embedding-3-small dimension
            self.index = faiss.IndexFlatIP(dimension)
            self._initialized = True
            log.info("✅ FAISS vector store initialized")
        except ImportError:
            log.warning("⚠️ FAISS not available, using dummy vector store")
            self._initialized = True
    
    def _get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for text using OpenAI or test mode"""
        if os.getenv("TEST_MODE") == "true":
            # Test mode: return deterministic random vector
            import hashlib
            seed = int(hashlib.md5(text.encode()).hexdigest()[:8], 16)
            np.random.seed(seed)
            return np.random.normal(0, 1, 1536).astype(np.float32)
        else:
            # Production mode: use OpenAI embeddings
            return self._get_openai_embedding(text)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _get_openai_embedding(self, text: str) -> np.ndarray:
        """Get embedding from OpenAI with retry logic"""
        try:
            import openai
            cfg = get_config()
            client = openai.OpenAI(api_key=cfg["OPENAI_API_KEY"])
            
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return np.array(response.data[0].embedding, dtype=np.float32)
        except Exception as e:
            log.error(f"❌ OpenAI embedding error: {e}")
            raise
    
    def add(self, text: str, metadata: Dict[str, Any] = None) -> str:
        """Add text to vector store and return ID"""
        if not self._initialized:
            self._initialize()
        
        if not self.index:
            # Fallback if FAISS not available
            return "dummy_id"
        
        # Get embedding
        embedding = self._get_embedding(text)
        
        # Add to FAISS index
        self.index.add(embedding.reshape(1, -1))
        
        # Store text and metadata
        text_id = f"text_{len(self.texts)}"
        self.texts.append(text)
        self.metadata.append(metadata or {})
        
        log.info(f"✅ Added text to vector store: {text[:50]}...")
        return text_id
    
    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Search for similar texts"""
        if not self._initialized:
            self._initialize()
        
        if not self.index or len(self.texts) == 0:
            return []
        
        # Get query embedding
        query_embedding = self._get_embedding(query)
        
        # Search in FAISS index
        scores, indices = self.index.search(query_embedding.reshape(1, -1), k)
        
        # Return results
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < len(self.texts):
                results.append({
                    "text": self.texts[idx],
                    "score": float(score),
                    "metadata": self.metadata[idx]
                })
        
        log.info(f"🔍 Vector search returned {len(results)} results")
        return results

class FirestoreMemoryGateway:
    def __init__(self):
        self.db = None
        self._initialized = False
        self.vector_store = VectorStore()
    
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
                project_id = cfg["GCLOUD_PROJECT"]
                if not project_id:
                    raise RuntimeError("missing GOOGLE_PROJECT_ID")
                
                # Try to get credentials from environment variable first
                credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
                if credentials_json and credentials_json.startswith("{"):
                    # Credentials are provided as JSON string
                    try:
                        credentials_info = json.loads(credentials_json)
                        credentials = service_account.Credentials.from_service_account_info(credentials_info)
                        self.db = firestore.Client(project=project_id, credentials=credentials)
                        log.info("✅ Firestore connection established with JSON credentials")
                    except json.JSONDecodeError:
                        raise RuntimeError("Invalid JSON in GOOGLE_APPLICATION_CREDENTIALS")
                elif credentials_json and os.path.exists(credentials_json):
                    # Credentials are provided as file path
                    self.db = firestore.Client(project=project_id)
                    log.info("✅ Firestore connection established with file credentials")
                else:
                    # Use default credentials (Application Default Credentials)
                    self.db = firestore.Client(project=project_id)
                    log.info("✅ Firestore connection established with default credentials")
            
            self._initialized = True
        except Exception as e:
            log.error(f"❌ Firestore connection failed: {e}")
            if os.getenv("TEST_MODE") == "true":
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
            doc = self.db.collection('users').document(phone).get()
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
            self.db.collection('users').document(phone).set(user_data)
        except Exception as e:
            log.error(f"❌ Firestore save error: {e}")
    
    def add_to_vector_store(self, text: str, metadata: dict = None):
        """Add text to vector store for RAG"""
        try:
            self.vector_store.add(text, metadata)
        except Exception as e:
            log.error(f"❌ Vector store add error: {e}")
    
    def search_similar(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Search for similar texts in vector store"""
        try:
            return self.vector_store.search(query, k)
        except Exception as e:
            log.error(f"❌ Vector store search error: {e}")
            return []

# Lazy singleton pattern
_memory_gateway = None

def _get_memory_gateway():
    """Get or create memory gateway singleton"""
    global _memory_gateway
    if _memory_gateway is None:
        _memory_gateway = FirestoreMemoryGateway()
    return _memory_gateway

def get_or_create_context(phone: str) -> Context:
    """Get or create context for phone number"""
    try:
        gateway = _get_memory_gateway()
        user_data = gateway.get_user_context(phone)
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
        else:
            # Create new context with GREETING state
            return Context(
                phone=phone,
                lang='it',
                name=None,
                client_type='new',
                state='GREETING',
                asked_name=False,
                slots={},
                history=[]
            )
    except Exception as e:
        log.error(f"❌ Context creation error: {e}")
        # Fallback: create new context
        return Context(
            phone=phone,
            lang='it',
            name=None,
            client_type='new',
            state='GREETING',
            asked_name=False,
            slots={},
            history=[]
        )

def load_context(phone: str) -> Context | None:
    """Load context for phone number (legacy function)"""
    return get_or_create_context(phone)

def save_context(ctx: Context):
    """Save context to memory"""
    try:
        if not ctx.phone:
            log.error("Missing phone in context, skip save")
            return
            
        gateway = _get_memory_gateway()
        user_data = {
            'lang': ctx.lang,
            'name': ctx.name,
            'client_type': ctx.client_type,
            'state': ctx.state,
            'asked_name': ctx.asked_name,
            'slots': ctx.slots,
            'history': ctx.history
        }
        gateway.save_user_context(ctx.phone, user_data)
        
        # Add recent messages to vector store for RAG
        if ctx.history and len(ctx.history) > 0:
            # Add the last message to vector store
            last_message = ctx.history[-1]
            if isinstance(last_message, dict) and 'text' in last_message:
                metadata = {
                    'phone': ctx.phone,
                    'timestamp': last_message.get('timestamp'),
                    'role': last_message.get('role', 'user')
                }
                gateway.add_to_vector_store(last_message['text'], metadata)
    except Exception as e:
        log.error(f"❌ Save context error: {e}")
        pass

def search_similar(query: str, k: int = 3) -> List[Dict[str, Any]]:
    """Search for similar texts in vector store"""
    try:
        gateway = _get_memory_gateway()
        return gateway.search_similar(query, k)
    except Exception as e:
        log.error(f"❌ Search similar error: {e}")
        return [] 