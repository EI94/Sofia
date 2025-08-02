"""
Test RAG memory functionality
"""

import pytest
import os
from sofia_lite.agents.context import Context
from sofia_lite.middleware.memory import save_context, search_similar

@pytest.fixture
def test_context():
    """Create a test context"""
    return Context(
        phone="+393001234567",
        lang="it",
        name="Test User",
        state="GREETING"
    )

def test_rag_memory_functionality(test_context):
    """Test RAG memory with 5 messages and similarity search"""
    
    # Set test mode
    os.environ["TEST_MODE"] = "true"
    
    # Import and test vector store directly
    from sofia_lite.middleware.memory import VectorStore
    
    # Create vector store
    vs = VectorStore()
    
    # Create 5 test messages
    messages = [
        "Ciao, mi chiamo Mario",
        "Voglio una consulenza per permesso di soggiorno",
        "Il costo è 60 euro per la consulenza",
        "Preferisco online",
        "Quando hai disponibilità?"
    ]
    
    # Add messages directly to vector store
    for i, msg in enumerate(messages):
        metadata = {"phone": test_context.phone, "timestamp": f"2025-08-02T{i:02d}:00:00Z"}
        vs.add(msg, metadata)
    
    # Test search with word present in message[2]
    query = "costo"
    results = vs.search(query, k=3)
    
    # Assert that message[2] (containing "costo") is in results
    assert len(results) > 0, "Search should return results"
    
    # Check if the message with "costo" is found
    found_costo = False
    for result in results:
        if "costo" in result["text"].lower():
            found_costo = True
            break
    
    assert found_costo, "Message containing 'costo' should be found in search results"
    
    # Test search with different query
    query2 = "consulenza"
    results2 = vs.search(query2, k=3)
    
    assert len(results2) > 0, "Second search should return results"
    
    # Check if messages with "consulenza" are found
    found_consulenza = False
    for result in results2:
        if "consulenza" in result["text"].lower():
            found_consulenza = True
            break
    
    assert found_consulenza, "Message containing 'consulenza' should be found"

def test_rag_empty_search():
    """Test RAG search with empty vector store"""
    os.environ["TEST_MODE"] = "true"
    
    # Search with empty vector store
    results = search_similar("test query", k=3)
    
    # Should return empty list
    assert results == [], "Empty vector store should return empty results"

def test_rag_metadata():
    """Test that metadata is preserved in vector store"""
    os.environ["TEST_MODE"] = "true"
    
    # Import and test vector store directly
    from sofia_lite.middleware.memory import VectorStore
    
    # Create vector store
    vs = VectorStore()
    
    # Add message with metadata
    metadata = {"phone": "+393001234567", "timestamp": "2025-08-02T10:00:00Z"}
    vs.add("Test message with metadata", metadata)
    
    # Search for the message
    results = vs.search("test message", k=1)
    
    assert len(results) > 0, "Should find the test message"
    assert "metadata" in results[0], "Result should contain metadata"
    assert results[0]["metadata"]["phone"] == "+393001234567", "Phone should be preserved in metadata" 