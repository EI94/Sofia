"""
Sofia Lite - State Machine
Defines the essential conversation states and valid transitions.
"""

from enum import Enum, auto
from typing import List, Dict

class State(Enum):
    """Essential conversation states for Sofia Lite"""
    INITIAL = auto()
    GREETING = auto()
    ASK_NAME = auto()
    ASK_SERVICE = auto()
    PROPOSE_CONSULT = auto()
    ASK_CHANNEL = auto()
    ASK_SLOT = auto()
    ASK_PAYMENT = auto()
    CONFIRMED = auto()
    ROUTE_ACTIVE = auto()
    ASK_CLARIFICATION = auto()

class Stage(Enum):
    """Conversation stages for tracking progress"""
    DISCOVERY = auto()
    SERVICE_SELECTION = auto()
    CONSULTATION_SCHEDULED = auto()
    PAYMENT_PENDING = auto()
    COMPLETED = auto()

# Valid state transitions
TRANSITIONS: Dict[State, List[State]] = {
    State.INITIAL:         [State.GREETING, State.ASK_NAME, State.ASK_SERVICE, State.ROUTE_ACTIVE],
    State.GREETING:        [State.ASK_NAME, State.ASK_SERVICE, State.ROUTE_ACTIVE],
    State.ASK_NAME:        [State.ASK_SERVICE],
    State.ASK_SERVICE:     [State.PROPOSE_CONSULT],
    State.PROPOSE_CONSULT: [State.ASK_CHANNEL, State.ASK_SLOT],
    State.ASK_CHANNEL:     [State.ASK_SLOT],
    State.ASK_SLOT:        [State.ASK_PAYMENT],
    State.ASK_PAYMENT:     [State.CONFIRMED],
    State.CONFIRMED:       [State.ASK_SERVICE, State.ROUTE_ACTIVE],
    State.ROUTE_ACTIVE:    [State.ASK_SERVICE, State.CONFIRMED],
    State.ASK_CLARIFICATION: [State.ASK_NAME, State.ASK_SERVICE, State.PROPOSE_CONSULT, State.ROUTE_ACTIVE],
}

def can_transition(from_state: State, to_state: State) -> bool:
    """
    Check if a transition from from_state to to_state is valid.
    
    Args:
        from_state: Current state
        to_state: Target state
        
    Returns:
        True if transition is valid, False otherwise
    """
    if from_state not in TRANSITIONS:
        return False
    
    # Permetti self-transition
    if from_state == to_state:
        return True
    
    return to_state in TRANSITIONS[from_state]

def get_valid_transitions(state: State) -> List[State]:
    """
    Get all valid transitions from a given state.
    
    Args:
        state: Current state
        
    Returns:
        List of valid next states
    """
    return TRANSITIONS.get(state, [])

def is_terminal_state(state: State) -> bool:
    """
    Check if a state is terminal (no valid transitions out).
    
    Args:
        state: State to check
        
    Returns:
        True if state is terminal, False otherwise
    """
    return len(get_valid_transitions(state)) == 0

def advance_from_greeting(ctx, intent):
    """
    Auto-advance from INITIAL/GREETING state based on intent and context.
    
    Args:
        ctx: Conversation context
        intent: Detected user intent
        
    Returns:
        New state or None if no auto-advance needed
    """
    if ctx.state == "INITIAL":
        # Always go to GREETING first for sequence control
        if intent in ["GREET", "ASK_NAME", "ASK_SERVICE"]:
            return State.GREETING
    elif ctx.state == "GREETING":
        # FORCE SEQUENCE: Always go to ASK_NAME for new users, regardless of intent
        if ctx.client_type == "new":
            return State.ASK_NAME
        # For active users, only advance if we have a name
        elif intent == "GREET" and ctx.name is not None:
            return State.ASK_SERVICE
        elif intent == "ASK_NAME":
            return State.ASK_NAME
    return None

def auto_advance(current_state: str, intent: str) -> str:
    """
    Auto-advance state machine to prevent stuck states.
    
    Args:
        current_state: Current state name
        intent: Detected user intent
        
    Returns:
        New state name after auto-advance
    """
    # Mapping per auto-advance
    mapping = {
        ("INITIAL", "GREET"): "GREETING",
        ("INITIAL", "ASK_NAME"): "ASK_NAME",
        ("INITIAL", "ASK_SERVICE"): "ASK_SERVICE",
        ("GREETING", "ASK_SERVICE"): "ASK_SERVICE",
        ("GREETING", "ASK_NAME"): "ASK_NAME"
    }
    
    return mapping.get((current_state, intent), current_state)
