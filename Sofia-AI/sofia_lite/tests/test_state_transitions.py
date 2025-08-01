"""
Sofia Lite - State Machine Tests
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from sofia_lite.agents.state import State, can_transition, get_valid_transitions, is_terminal_state
from sofia_lite.agents.planner import next_state

# Test data for valid transitions
VALID_TRANSITIONS = [
    (State.GREETING, State.ASK_NAME),
    (State.GREETING, State.ASK_SERVICE),
    (State.ASK_NAME, State.ASK_SERVICE),
    (State.ASK_SERVICE, State.PROPOSE_CONSULT),
    (State.PROPOSE_CONSULT, State.WAIT_SLOT),
    (State.PROPOSE_CONSULT, State.WAIT_PAYMENT),
    (State.WAIT_SLOT, State.CONFIRMED),
    (State.WAIT_PAYMENT, State.CONFIRMED),
    (State.CONFIRMED, State.ASK_SERVICE),
    (State.ASK_CLARIFICATION, State.ASK_NAME),
    (State.ASK_CLARIFICATION, State.ASK_SERVICE),
    (State.ASK_CLARIFICATION, State.PROPOSE_CONSULT),
]

# Test data for invalid transitions
INVALID_TRANSITIONS = [
    (State.GREETING, State.CONFIRMED),
    (State.ASK_NAME, State.GREETING),
    (State.ASK_SERVICE, State.ASK_NAME),
    (State.PROPOSE_CONSULT, State.GREETING),
    (State.WAIT_SLOT, State.ASK_SERVICE),
    (State.WAIT_PAYMENT, State.WAIT_SLOT),
    (State.CONFIRMED, State.WAIT_PAYMENT),
    (State.ASK_CLARIFICATION, State.CONFIRMED),
]

@pytest.mark.parametrize("from_state,to_state", VALID_TRANSITIONS)
def test_valid_transitions(from_state, to_state):
    """Test that valid transitions return True"""
    assert can_transition(from_state, to_state) == True

@pytest.mark.parametrize("from_state,to_state", INVALID_TRANSITIONS)
def test_invalid_transitions(from_state, to_state):
    """Test that invalid transitions return False"""
    assert can_transition(from_state, to_state) == False

def test_get_valid_transitions():
    """Test getting valid transitions for each state"""
    # Test GREETING state
    transitions = get_valid_transitions(State.GREETING)
    assert State.ASK_NAME in transitions
    assert State.ASK_SERVICE in transitions
    assert len(transitions) == 2
    
    # Test ASK_NAME state
    transitions = get_valid_transitions(State.ASK_NAME)
    assert State.ASK_SERVICE in transitions
    assert len(transitions) == 1
    
    # Test CONFIRMED state
    transitions = get_valid_transitions(State.CONFIRMED)
    assert State.ASK_SERVICE in transitions
    assert len(transitions) == 1

def test_is_terminal_state():
    """Test terminal state detection"""
    # No states should be terminal in our FSM
    for state in State:
        assert is_terminal_state(state) == False

def test_next_state_mapping():
    """Test intent to state mapping"""
    # Test basic intent mappings
    assert next_state(State.GREETING, "GREET") == State.ASK_NAME
    assert next_state(State.ASK_NAME, "ASK_NAME") == State.ASK_SERVICE
    assert next_state(State.ASK_SERVICE, "ASK_SERVICE") == State.PROPOSE_CONSULT
    
    # Test fallback for unknown intent
    assert next_state(State.GREETING, "UNKNOWN") == State.ASK_CLARIFICATION
    assert next_state(State.ASK_NAME, "INVALID_INTENT") == State.ASK_CLARIFICATION

def test_next_state_validation():
    """Test that next_state respects transition rules"""
    # This should be invalid: GREETING -> CONFIRMED
    # But next_state should handle it gracefully
    result = next_state(State.GREETING, "CONFIRM")
    # Should fallback to clarification since GREETING -> CONFIRMED is invalid
    assert result == State.ASK_CLARIFICATION

def test_all_states_have_transitions():
    """Test that all states have defined transitions"""
    from sofia_lite.agents.state import TRANSITIONS
    
    for state in State:
        assert state in TRANSITIONS, f"State {state} has no transitions defined"

if __name__ == "__main__":
    pytest.main([__file__])
