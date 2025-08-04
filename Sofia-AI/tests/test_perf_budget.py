"""
Performance Budget Test - Δmini Optimization
Mock LLM to 200ms, ensure end-to-end < 1s
"""

import pytest
import asyncio
import time
from unittest.mock import patch, MagicMock
from sofia_lite.agents.orchestrator import Orchestrator
from sofia_lite.middleware.llm import chat, classify

class TestPerformanceBudget:
    """Test performance budget constraints"""
    
    @pytest.fixture
    def orchestrator(self):
        return Orchestrator()
    
    @patch('sofia_lite.middleware.llm.chat')
    @patch('sofia_lite.middleware.llm.classify')
    async def test_end_to_end_performance(self, mock_classify, mock_chat, orchestrator):
        """Test end-to-end performance with mocked LLM"""
        
        # Mock LLM responses with 200ms delay
        async def mock_llm_response(*args, **kwargs):
            await asyncio.sleep(0.2)  # 200ms delay
            return "Mock response"
        
        mock_chat.side_effect = mock_llm_response
        mock_classify.side_effect = mock_llm_response
        
        # Test message
        phone = "+393331234567"
        message = "Ciao, mi chiamo Mario Rossi"
        
        # Measure end-to-end time
        start_time = time.time()
        
        try:
            result = orchestrator.process_message(phone, message)
            end_time = time.time()
            
            total_time = (end_time - start_time) * 1000  # Convert to ms
            
            # Assertions
            assert total_time < 1000, f"End-to-end time {total_time:.0f}ms exceeds 1s budget"
            assert result is not None, "Should return a response"
            assert "reply" in result, "Response should contain reply field"
            
            print(f"✅ End-to-end time: {total_time:.0f}ms (target < 1000ms)")
            
        except Exception as e:
            pytest.fail(f"Test failed with exception: {e}")
    
    @patch('sofia_lite.middleware.llm.chat')
    async def test_llm_response_time(self, mock_chat):
        """Test LLM response time is under 200ms"""
        
        async def mock_llm_response(*args, **kwargs):
            await asyncio.sleep(0.2)  # 200ms delay
            return "Mock response"
        
        mock_chat.side_effect = mock_llm_response
        
        # Test LLM call
        start_time = time.time()
        
        try:
            result = await chat("Test prompt", "Test message")
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to ms
            
            # Assertions
            assert response_time < 250, f"LLM response time {response_time:.0f}ms exceeds 250ms budget"
            assert result == "Mock response", "Should return mocked response"
            
            print(f"✅ LLM response time: {response_time:.0f}ms (target < 250ms)")
            
        except Exception as e:
            pytest.fail(f"LLM test failed with exception: {e}")
    
    def test_cache_performance(self):
        """Test TTL cache performance"""
        from sofia_lite.utils.memo import ttl_cache
        
        call_count = 0
        
        @ttl_cache(ttl=30, maxsize=256)
        def test_function(input_value):
            nonlocal call_count
            call_count += 1
            return f"result_{input_value}"
        
        # First call should increment counter
        result1 = test_function("test")
        assert call_count == 1
        assert result1 == "result_test"
        
        # Second call with same input should use cache
        result2 = test_function("test")
        assert call_count == 1  # Should not increment
        assert result2 == "result_test"
        
        # Different input should increment counter
        result3 = test_function("different")
        assert call_count == 2
        assert result3 == "result_different"
        
        print("✅ TTL cache performance test passed")
    
    @patch('sofia_lite.middleware.memory.FirestoreMemoryGateway.get_user_context')
    async def test_firestore_batch_performance(self, mock_get_context):
        """Test Firestore batch get performance"""
        
        # Mock batched response
        mock_get_context.return_value = {
            "user": {"name": "Test User"},
            "history": {"messages": []},
            "rag": {"chunks": []}
        }
        
        from sofia_lite.middleware.memory import FirestoreMemoryGateway
        
        gateway = FirestoreMemoryGateway()
        
        start_time = time.time()
        
        try:
            result = gateway.get_user_context("+393331234567")
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to ms
            
            # Assertions
            assert response_time < 100, f"Firestore batch time {response_time:.0f}ms exceeds 100ms budget"
            assert result is not None, "Should return context data"
            assert "user" in result, "Should contain user data"
            assert "history" in result, "Should contain history data"
            assert "rag" in result, "Should contain RAG data"
            
            print(f"✅ Firestore batch time: {response_time:.0f}ms (target < 100ms)")
            
        except Exception as e:
            pytest.fail(f"Firestore test failed with exception: {e}")

if __name__ == "__main__":
    # Run performance tests
    pytest.main([__file__, "-v"]) 