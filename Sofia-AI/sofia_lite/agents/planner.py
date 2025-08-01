import json
from .prompt_builder import build_system_prompt
from .context import Context

INTENTS = ["GREET","ASK_NAME","ASK_SERVICE","PROPOSE_CONSULT",
           "ASK_CHANNEL","ASK_SLOT","ASK_PAYMENT","CONFIRM",
           "ROUTE_ACTIVE","CLARIFY","UNKNOWN"]

def plan(ctx: Context, user_msg: str, llm) -> tuple[str, str]:
    """
    Returns (intent:str, rationale:str)
    """
    sys_prompt = build_system_prompt(ctx)
    plan_prompt = f"""{sys_prompt}

You must answer with strict JSON:
{{"intent": "<one_of_{INTENTS}>", "reason": "<short why>"}}

User: \"{user_msg}\"
"""
    
    try:
        rsp = llm.chat_completion([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": plan_prompt}
        ], model="gpt-4o-mini")
        
        data = json.loads(rsp)
        return data["intent"], data["reason"]
    except Exception as e:
        # Fallback to UNKNOWN if parsing fails
        return "UNKNOWN", f"Error parsing response: {str(e)}" 