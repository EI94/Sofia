"""
Sofia Lite - State Machine
Defines the essential conversation states and valid transitions.
"""

from enum import Enum, auto
from typing import Dict, List


class State(Enum):
    """Essential conversation states for Sofia Lite"""

    GREETING = auto()
    ASK_NAME = auto()
    ASK_SERVICE = auto()
    PROPOSE_CONSULT = auto()
    WAIT_SLOT = auto()
    WAIT_PAYMENT = auto()
    CONFIRMED = auto()
    ASK_CLARIFICATION = auto()


# Valid state transitions
TRANSITIONS: Dict[State, List[State]] = {
    State.GREETING: [State.ASK_NAME, State.ASK_SERVICE],
    State.ASK_NAME: [State.ASK_SERVICE],
    State.ASK_SERVICE: [State.PROPOSE_CONSULT],
    State.PROPOSE_CONSULT: [State.WAIT_SLOT, State.WAIT_PAYMENT],
    State.WAIT_SLOT: [State.CONFIRMED],
    State.WAIT_PAYMENT: [State.CONFIRMED],
    State.CONFIRMED: [State.ASK_SERVICE],
    State.ASK_CLARIFICATION: [State.ASK_NAME, State.ASK_SERVICE, State.PROPOSE_CONSULT],
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
