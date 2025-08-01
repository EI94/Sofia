import json
from .prompt_builder import build_system_prompt
from .context import Context
from .state import State

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

def next_state(current_state: State, intent: str) -> State:
    """
    Determine the next state based on current state and intent.
    
    Args:
        current_state: Current conversation state
        intent: Detected user intent
        
    Returns:
        Next state to transition to
    """
    # Intent to state mapping
    intent_to_state = {
        "GREET": State.ASK_NAME,
        "ASK_NAME": State.ASK_SERVICE,
        "ASK_SERVICE": State.PROPOSE_CONSULT,
        "PROPOSE_CONSULT": State.WAIT_SLOT,
        "ASK_CHANNEL": State.WAIT_SLOT,
        "ASK_SLOT": State.WAIT_PAYMENT,
        "ASK_PAYMENT": State.CONFIRMED,
        "CONFIRM": State.CONFIRMED,
        "ROUTE_ACTIVE": State.ASK_SERVICE,
        "CLARIFY": State.ASK_CLARIFICATION,
        "UNKNOWN": State.ASK_CLARIFICATION,
    }
    
    # Get target state from intent
    target_state = intent_to_state.get(intent, State.ASK_CLARIFICATION)
    
    # Validate transition
    from .state import can_transition
    if can_transition(current_state, target_state):
        return target_state
    else:
        # Fallback to clarification if transition is invalid
        return State.ASK_CLARIFICATION 