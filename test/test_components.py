import pytest
from cacao import Component, State

class TestButton(Component):
    __test__ = False  # Prevent pytest from collecting this class
    def __init__(self, label: str, on_click=None):
        super().__init__()
        self.label = label
        self.on_click = on_click

    def render(self):
        return {
            "type": "button",
            "props": {
                "label": self.label,
                "onClick": self.on_click
            }
        }

def test_component_rendering():
    button = TestButton("Click me")
    rendered = button.render()
    assert rendered["type"] == "button"
    assert rendered["props"]["label"] == "Click me"

def test_component_with_state():
    counter = State(0)
    def increment():
        counter.set(counter.value + 1)
    
    button = TestButton("Increment", increment)
    increment()
    assert counter.value == 1