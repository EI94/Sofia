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
        
        if name_result:
            ctx.extracted_name = name_result
            log.info(f"👤 Name extracted: {name_result}")
        
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
        validated_intent, validated_state, warning = validate(ctx, intent, confidence)
        if warning:
            log.warning(f"⚠️ Validation warning: {warning}")
        intent = validated_intent
        log.info(f"✅ Intent validated: {intent} (conf: {confidence:.2f})")
        
        # Short-circuit for predictable responses in GREETING state
        from . import state
        if intent in {"GREET", "ASK_NAME", "ASK_SERVICE"} and ctx.state in {"GREETING", "ASK_CLARIFICATION"}:
            log.info(f"⚡ Short-circuit for {intent} in {ctx.state} state")
            
            # Force GREETING state for new users to avoid ASK_CLARIFICATION issues
            if ctx.client_type == "new" and ctx.state == "ASK_CLARIFICATION":
                log.info(f"🔄 Forcing GREETING state for new user")
                ctx.state = "GREETING"
            
            from .executor import _ROUTE
            from importlib import import_module
            skill_module = _ROUTE.get(intent, "clarify")
            mod = import_module(f"sofia_lite.skills.{skill_module}")
            response = mod.run(ctx, message)
            
            # Update state after short-circuit
            old_state = ctx.state
            from .planner import next_state
            from .state import State
            current_state = State[ctx.state]
            new_state = next_state(current_state, intent, ctx)
            if new_state.name != old_state:
                log.info(f"🔄 State transition {old_state} ➜ {new_state.name}")
                ctx.state = new_state.name
            
            # Save context after state update in short-circuit
            save_context(ctx)
        else:
            # Execute intent normally
            log.info(f"🚀 Dispatching intent: {intent} to skill")
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
        
        # Optimistic save - save context before LLM call (only for non-short-circuit)
        if not (intent in {"GREET", "ASK_NAME", "ASK_SERVICE"} and ctx.state in {"GREETING", "ASK_CLARIFICATION"}):
            old_state = ctx.state
            
            # Force GREETING state for new users to avoid ASK_CLARIFICATION issues
            if ctx.client_type == "new" and ctx.state == "ASK_CLARIFICATION":
                log.info(f"🔄 Forcing GREETING state for new user before save")
                ctx.state = "GREETING"
            
            save_context(ctx)
        
        # Update context
        ctx.history.append({"role": "user", "content": message})
        ctx.history.append({"role": "assistant", "content": response})
        
        # Save context again with updated history
        # Force correct state for new users
        if ctx.client_type == "new" and ctx.state == "ASK_CLARIFICATION":
            log.info(f"🔄 Forcing ASK_NAME state for new user after skill execution")
            ctx.state = "ASK_NAME"
        
        save_context(ctx)
        
        # Force correct state for new users in response
        final_state = ctx.state
        if ctx.client_type == "new" and final_state == "ASK_CLARIFICATION":
            log.info(f"🔄 Forcing ASK_NAME state in response for new user")
            final_state = "ASK_NAME"
        print(f"[DEBUG] orchestrator return: ctx.state={ctx.state}, final_state={final_state}, phone={phone}")
        return {
            "reply": response,
            "intent": intent,
            "state": final_state,
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
