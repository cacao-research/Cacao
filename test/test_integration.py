import pytest
from cacao import Component, State, mix

class CounterComponent(Component):
    """Test component that uses state for a counter."""
    
    def __init__(self):
        super().__init__()
        self.count = State(0)
    
    def increment(self):
        self.count.set(self.count.value + 1)
    
    def decrement(self):
        self.count.set(self.count.value - 1)
    
    def render(self):
        return {
            "type": "div",
            "props": {
                "className": "counter",
                "children": [
                    {
                        "type": "button", 
                        "props": {
                            "onClick": self.decrement,
                            "text": "-"
                        }
                    },
                    {
                        "type": "span",
                        "props": {
                            "text": str(self.count.value)
                        }
                    },
                    {
                        "type": "button",
                        "props": {
                            "onClick": self.increment,
                            "text": "+"
                        }
                    }
                ]
            }
        }

def test_component_with_state_updates():
    counter = CounterComponent()
    initial_render = counter.render()
    
    # Verify initial state
    assert initial_render["props"]["children"][1]["props"]["text"] == "0"
    
    # Update state and re-render
    counter.increment()
    updated_render = counter.render()
    
    # Verify updated state
    assert updated_render["props"]["children"][1]["props"]["text"] == "1"
    
    # Multiple updates
    counter.increment()
    counter.increment()
    counter.decrement()
    final_render = counter.render()
    
    # Verify final state
    assert final_render["props"]["children"][1]["props"]["text"] == "2"

def test_route_with_component():
    # Register a route that uses a component
    @mix("/counter")
    def counter_route():
        return CounterComponent().render()
    
    # Test that the route function returns the expected component structure
    route_result = counter_route()
    assert route_result["type"] == "div"
    assert route_result["props"]["className"] == "counter"
    assert len(route_result["props"]["children"]) == 3