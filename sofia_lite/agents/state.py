"""
Sofia Lite - State Machine
Defines the essential conversation states and valid transitions.
"""

from enum import Enum, auto
from typing import Dict, List


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
    State.INITIAL: [
        State.GREETING,
        State.ASK_NAME,
        State.ASK_SERVICE,
        State.ROUTE_ACTIVE,
    ],
    State.GREETING: [State.ASK_NAME, State.ASK_SERVICE, State.ROUTE_ACTIVE],
    State.ASK_NAME: [State.ASK_SERVICE],
    State.ASK_SERVICE: [State.PROPOSE_CONSULT],
    State.PROPOSE_CONSULT: [State.ASK_CHANNEL, State.ASK_SLOT],
    State.ASK_CHANNEL: [State.ASK_SLOT],
    State.ASK_SLOT: [State.ASK_PAYMENT],
    State.ASK_PAYMENT: [State.CONFIRMED],
    State.CONFIRMED: [State.ASK_SERVICE, State.ROUTE_ACTIVE],
    State.ROUTE_ACTIVE: [State.ASK_SERVICE, State.CONFIRMED],
    State.ASK_CLARIFICATION: [
        State.ASK_NAME,
        State.ASK_SERVICE,
        State.PROPOSE_CONSULT,
        State.ROUTE_ACTIVE,
    ],
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


# Allowed state transitions
ALLOWED_TRANSITIONS = {
    ("INITIAL", "GREET"): "ASK_NAME",
    ("INITIAL", "ASK_NAME"): "ASK_NAME",
    ("INITIAL", "ASK_SERVICE"): "ASK_SERVICE",
    ("INITIAL", "ROUTE_ACTIVE"): "ROUTE_ACTIVE",
    ("GREETING", "GREET"): "ASK_NAME",
    ("GREETING", "ASK_NAME"): "ASK_NAME",
    ("GREETING", "ASK_SERVICE"): "ASK_SERVICE",
    ("ASK_NAME", "ASK_NAME"): "ASK_NAME",
    ("ASK_NAME", "ASK_SERVICE"): "ASK_SERVICE",
    ("ASK_SERVICE", "ASK_SERVICE"): "ASK_SERVICE",
    ("ASK_SERVICE", "PROPOSE_CONSULT"): "PROPOSE_CONSULT",
    ("PROPOSE_CONSULT", "ASK_CHANNEL"): "ASK_CHANNEL",
    ("PROPOSE_CONSULT", "ASK_SLOT"): "ASK_SLOT",
    ("ASK_CHANNEL", "ASK_SLOT"): "ASK_SLOT",
    ("ASK_SLOT", "ASK_PAYMENT"): "ASK_PAYMENT",
    ("ASK_PAYMENT", "CONFIRM_BOOKING"): "CONFIRMED",
    ("CONFIRMED", "ASK_SERVICE"): "ASK_SERVICE",
    ("CONFIRMED", "ROUTE_ACTIVE"): "ROUTE_ACTIVE",
    ("ROUTE_ACTIVE", "ASK_SERVICE"): "ASK_SERVICE",
    ("ROUTE_ACTIVE", "CONFIRM_BOOKING"): "CONFIRMED",
    ("ASK_CLARIFICATION", "GREET"): "ASK_NAME",
    ("ASK_CLARIFICATION", "ASK_NAME"): "ASK_NAME",
    ("ASK_CLARIFICATION", "ASK_SERVICE"): "ASK_SERVICE",
    ("ASK_CLARIFICATION", "PROPOSE_CONSULT"): "PROPOSE_CONSULT",
    ("ASK_CLARIFICATION", "ROUTE_ACTIVE"): "ROUTE_ACTIVE",
}
