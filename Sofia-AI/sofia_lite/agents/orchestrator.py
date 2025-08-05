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
from ..middleware.memory import get_or_create_context, save_context, search_similar
from ..middleware.latency import track_latency

log = logging.getLogger("sofia.orchestrator")

class Orchestrator:
    """Main orchestrator for Sofia conversation flow"""
    
    def __init__(self):
        pass  # No initialization needed for function-based approach
    
    @track_latency("TOTAL")
    def process_message(self, phone: str, message: str, channel: str = "whatsapp") -> Dict[str, Any]:
        """Process incoming message and return response - γ5 optimization with parallel execution"""
        
        # Load or create context
        ctx = get_or_create_context(phone)
        log.info(f"📱 Context loaded/created for: {phone} (state: {ctx.state})")
        
        # γ5 optimization: Execute language-detect, RAG retrieve, name-extract in parallel
        import asyncio
        import concurrent.futures
        
        def run_parallel_tasks():
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                # Task 1: Language detection
                lang_future = executor.submit(self._detect_language, message, ctx)
                
                # Task 2: RAG search
                rag_future = executor.submit(search_similar, message, 3)
                
                # Task 3: Name extraction (if needed)
                name_future = executor.submit(self._extract_name, message, ctx)
                
                # Wait for all tasks to complete
                lang_result = lang_future.result()
                rag_result = rag_future.result()
                name_result = name_future.result()
                
                return lang_result, rag_result, name_result
        
        # Execute parallel tasks
        lang_result, rag_result, name_result = run_parallel_tasks()
        
        # Update context with results
        if lang_result:
            ctx.lang, _ = lang_result
            log.info(f"🌍 Language detected: {ctx.lang} for {phone}")
        
        if rag_result:
            ctx.rag_chunks = [r["text"] for r in rag_result]
            if ctx.rag_chunks:
                log.info(f"🔍 RAG found {len(ctx.rag_chunks)} relevant chunks")
        
        # FORCE SEQUENCE: Only extract name if we're in ASK_NAME state
        if name_result and ctx.state == "ASK_NAME":
            ctx.extracted_name = name_result
            ctx.name = name_result  # Set the name in context
            log.info(f"👤 Name extracted and set: {name_result}")
        elif name_result:
            log.info(f"👤 Name detected but IGNORED (not in ASK_NAME state): {name_result}")
            # Clear any extracted name to force sequence
            ctx.extracted_name = None
            ctx.name = None
        
        # Build system prompt (will be updated by each skill with intent-specific prompt)
        # system_prompt = build_system_prompt(ctx)  # REMOVED - each skill will use intent-specific prompt
        
        # Plan intent
        intent, reason = plan(ctx, message, chat)
        log.info(f"🎯 Intent detected: {intent} for {phone}")
        log.info(f"📝 Intent reason: {reason}")
        
        # Extract confidence from reason if available
        confidence = 1.0
        if "confidence:" in reason:
            try:
                confidence = float(reason.split("confidence:")[1].split(")")[0].strip())
            except:
                confidence = 1.0
        
        # Validate intent and state transition
        new_state, validated_intent, warning = validate(ctx, intent, confidence)
        if warning:
            log.warning(f"⚠️ Validation warning: {warning}")
        intent = validated_intent
        
        # Update state immediately
        ctx.state = new_state
        
        log.info(f"✅ Intent validated: {intent} (conf: {confidence:.2f})")
        
        # Execute skill
        response = dispatch(intent, ctx, message)
        return {
            "reply": response,
            "intent": intent,
            "state": ctx.state,
            "lang": ctx.lang,
            "phone": phone
        }
    
    def _detect_language(self, message: str, ctx) -> tuple[str, Optional[str]]:
        """Helper method for language detection - γ5 optimization"""
        if not ctx.lang or ctx.lang == "unknown":
            from ..middleware.language import detect_lang_with_heuristics
            return detect_lang_with_heuristics(message, ctx)
        return None
    
    def _extract_name(self, message: str, ctx) -> Optional[str]:
        """Helper method for name extraction - γ5 optimization"""
        try:
            from ..utils.name_extract import extract_name
            return extract_name(message, ctx.lang)
        except Exception as e:
            log.warning(f"Name extraction failed: {e}")
            return None
    
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
