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
from ..middleware.memory import load_context, save_context

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
        
        # Build system prompt
        system_prompt = build_system_prompt(ctx)
        
        # Plan intent
        intent, reason = plan(ctx, message, chat)
        log.info(f"🎯 Intent detected: {intent} for {phone}")
        
        # Validate intent and state transition
        intent = validate(ctx, intent)
        log.info(f"✅ Intent validated: {intent}")
        
        # Execute intent
        response = dispatch(intent, ctx, message)
        log.info(f"💬 Response generated for {phone}: {response[:50]}...")
        
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
