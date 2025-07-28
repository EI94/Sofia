# Thin wrapper around OpenAI
from ..gateways.llm import OpenAIGateway

# Create singleton instance
_llm_gateway = OpenAIGateway()

def chat_completion(messages, model="gpt-4o-mini"):
    """Wrapper for OpenAI chat completion"""
    return _llm_gateway.generate_response_with_system(messages, model) 