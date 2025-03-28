import pytest
from cacao import State

def test_state_initialization():
    state = State(initial_value=42)
    assert state.value == 42

def test_state_update():
    state = State(initial_value=0)
    state.set(10)
    assert state.value == 10

def test_state_subscription():
    state = State(initial_value=0)
    callback_called = False
    
    def on_change(new_value):
        nonlocal callback_called
        callback_called = True
        assert new_value == 5
    
    state.subscribe(on_change)
    state.set(5)
    assert callback_called