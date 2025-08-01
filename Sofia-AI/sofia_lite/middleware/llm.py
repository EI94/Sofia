# Thin wrapper around OpenAI
import openai
import os
import logging

log = logging.getLogger("sofia.llm")

class OpenAIGateway:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = openai.OpenAI(api_key=api_key)
        else:
            self.client = None
            log.warning("⚠️ OPENAI_API_KEY not set, LLM will return fallback responses")
    
    def generate_response_with_system(self, messages, model="gpt-4o-mini"):
        """Generate response using OpenAI API"""
        if not self.client:
            return "Mi dispiace, il servizio non è disponibile al momento."
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            log.error(f"❌ OpenAI API error: {e}")
            return "Mi dispiace, c'è stato un errore tecnico."

# Create singleton instance
_llm_gateway = OpenAIGateway()

def chat_completion(messages, model="gpt-4o-mini"):
    """Wrapper for OpenAI chat completion"""
    return _llm_gateway.generate_response_with_system(messages, model) 