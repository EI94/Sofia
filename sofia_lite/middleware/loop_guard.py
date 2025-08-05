"""
Sofia Lite - Loop Guard Middleware
Prevents conversation loops and escalates to human when needed
"""

import logging
from typing import Dict, Any
from ..agents.context import Context

log = logging.getLogger("sofia.loop_guard")

class LoopGuard:
    """Prevents conversation loops and escalates when necessary"""
    
    def __init__(self):
        self.clarification_count = 0
        self.max_clarifications = 3
        self.escalation_threshold = 5
    
    def check_loop(self, ctx: Context, intent: str, response: str) -> Dict[str, Any]:
        """Check for conversation loops and return escalation decision"""
        
        # Reset clarification count if intent is not clarify
        if intent != "CLARIFY":
            self.clarification_count = 0
        else:
            self.clarification_count += 1
        
        # Check if we're in a clarification loop
        if self.clarification_count >= self.max_clarifications:
            log.warning(f"🔄 Clarification loop detected for {ctx.phone}, escalating to human")
            return {
                "escalate": True,
                "reason": "clarification_loop",
                "message": "Mi dispiace, ma sembra che ci siano difficoltà di comunicazione. Ti metto in contatto con un nostro consulente umano che potrà aiutarti meglio."
            }
        
        # Check for repeated responses
        if len(ctx.history) > 0:
            recent_responses = [msg["content"] for msg in ctx.history[-3:] if msg["role"] == "assistant"]
            if len(recent_responses) >= 2 and recent_responses[-1] == recent_responses[-2]:
                log.warning(f"🔄 Repeated response detected for {ctx.phone}, escalating to human")
                return {
                    "escalate": True,
                    "reason": "repeated_response",
                    "message": "Mi dispiace, ma sembra che ci sia un problema tecnico. Ti metto in contatto con un nostro consulente umano."
                }
        
        # Check for too many messages in session
        if len(ctx.history) > self.escalation_threshold * 2:
            log.info(f"📊 Long conversation detected for {ctx.phone}, considering escalation")
            return {
                "escalate": True,
                "reason": "long_conversation",
                "message": "Vedo che la conversazione si sta prolungando. Ti metto in contatto con un nostro consulente umano per un'assistenza più diretta."
            }
        
        # No escalation needed
        return {
            "escalate": False,
            "reason": None,
            "message": None
        }
    
    def should_escalate(self, ctx: Context, intent: str, response: str) -> bool:
        """Quick check if escalation is needed"""
        result = self.check_loop(ctx, intent, response)
        return result["escalate"]
    
    def get_escalation_message(self, ctx: Context, intent: str, response: str) -> str:
        """Get escalation message if needed"""
        result = self.check_loop(ctx, intent, response)
        return result.get("message", "Mi dispiace, ti metto in contatto con un consulente umano.") 