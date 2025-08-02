"""
Sofia Lite - Core Orchestrator
Manages conversation flow and state transitions
"""

import logging
from typing import Optional, Dict, Any
from .context import Context
from .planner import plan
from .executor import dispatch
from .validator import validate
from .prompt_builder import build_system_prompt
from ..middleware.llm import chat
from ..middleware.memory import load_context, save_context, search_similar

log = logging.getLogger("sofia.orchestrator")

class Orchestrator:
    """Main orchestrator for Sofia conversation flow"""
    
    def __init__(self):
        pass  # No initialization needed for function-based approach
    
    def process_message(self, phone: str, message: str, channel: str = "whatsapp") -> Dict[str, Any]:
        """Process incoming message and return response"""
        
        # Load context
        ctx = load_context(phone)
        if not ctx:
            ctx = Context(phone=phone, lang="it", state="GREETING")
            log.info(f"🆕 New user context created: {phone}")
        
        # Detect language if not set
        if not ctx.lang or ctx.lang == "unknown":
            from ..middleware.language import detect
            ctx.lang = detect(message)
            log.info(f"🌍 Language detected: {ctx.lang} for {phone}")
        
        # RAG: Search for similar context
        relevant_chunks = search_similar(message, k=3)
        ctx.rag_chunks = [r["text"] for r in relevant_chunks]
        if ctx.rag_chunks:
            log.info(f"🔍 RAG found {len(ctx.rag_chunks)} relevant chunks")
        
        # Build system prompt
        system_prompt = build_system_prompt(ctx)
        
        # Plan intent
        intent, reason = plan(ctx, message, chat)
        log.info(f"🎯 Intent detected: {intent} for {phone}")
        
        # Extract confidence from reason if available
        confidence = 1.0
        if "confidence:" in reason:
            try:
                confidence = float(reason.split("confidence:")[1].split(")")[0].strip())
            except:
                confidence = 1.0
        
        # Validate intent and state transition
        intent = validate(ctx, intent, confidence)
        log.info(f"✅ Intent validated: {intent} (conf: {confidence:.2f})")
        
        # Execute intent
        response = dispatch(intent, ctx, message)
        
        # Ensure response is a string and handle any issues
        try:
            if not isinstance(response, str):
                response = str(response) if response is not None else "Mi dispiace, c'è stato un errore nella generazione della risposta."
            
            # Clean the response
            response = response.strip()
            if not response:
                response = "Mi dispiace, non ho capito. Puoi ripetere?"
                
        except Exception as e:
            log.error(f"❌ Error processing response: {e}")
            response = "Mi dispiace, c'è stato un errore nella generazione della risposta."
        
        # Safe logging
        try:
            # Clean response for logging
            safe_response = response.replace('\n', ' ').replace('\r', ' ').strip()
            log.info(f"💬 Response generated for {phone}: {safe_response[:50]}...")
        except Exception as e:
            log.error(f"❌ Error logging response: {e}")
        
        # Update context
        ctx.history.append({"role": "user", "content": message})
        ctx.history.append({"role": "assistant", "content": response})
        
        # Save context
        save_context(ctx)
        
        return {
            "reply": response,
            "intent": intent,
            "state": ctx.state,
            "lang": ctx.lang,
            "phone": phone
        }
    
    def process_voice(self, phone: str, transcript: str) -> Dict[str, Any]:
        """Process voice transcript and return TwiML response"""
        
        # Process message normally
        result = self.process_message(phone, transcript, "voice")
        
        # Generate TwiML response
        twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Bianca" rate="medium" pitch="medium">{result["reply"]}</Say>
</Response>"""
        
        return {
            "twiml": twiml_response,
            "reply": result["reply"],
            "intent": result["intent"],
            "state": result["state"],
            "lang": result["lang"]
        }
