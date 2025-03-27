from cacao import mix, run, State, Component
from cacao.core.server import CacaoServer
from datetime import datetime

# Create separate reactive states for each component
counter_state = State(0)
timestamp_state = State(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Create a counter component
class Counter(Component):
    def __init__(self):
        super().__init__()
        self.id = id(self)  # For demonstration of hot reload
        self.component_type = "counter"  # Add component type for identification
        
    def render(self, ui_state=None):
        """
        Render the counter component.
        
        Args:
            ui_state: Optional state from the UI definition
        """
        # Get the counter value from UI state or local state
        counter_value = self._get_counter_value(ui_state)
        
        return {
            "type": "section",
            "component_type": self.component_type,  # Add component type for identification
            "props": {
                "children": [
                    {
                        "type": "text",
                        "props": {
                            "content": f"Counter value: {counter_value} (Component ID: {self.id})"
                        }
                    },
                    {
                        "type": "button",
                        "props": {
                            "label": "Increment",
                            "action": "increment_counter"  # Use string identifier
                        }
                    }
                ]
            }
        }
    
    def _get_counter_value(self, ui_state=None):
        """
        Get counter value from UI state or local state.
        
        Args:
            ui_state: Optional state from the UI definition
        """
        # First try to get from UI state
        if ui_state and isinstance(ui_state, dict) and 'counter' in ui_state:
            return ui_state['counter']
        
        # Fallback to local state
        return counter_state.value

# Create a timer component
class Timer(Component):
    def __init__(self):
        super().__init__()
        self.id = id(self)  # For demonstration of hot reload
        self.component_type = "timer"  # Add component type for identification
        
    def render(self, ui_state=None):
        """
        Render the timer component.
        
        Args:
            ui_state: Optional state from the UI definition
        """
        # Get the timestamp from UI state or current time
        timestamp = self._get_timestamp(ui_state)
        
        return {
            "type": "section",
            "component_type": self.component_type,  # Add component type for identification
            "props": {
                "children": [
                    {
                        "type": "text",
                        "props": {
                            "content": f"Current Time: {timestamp} (Component ID: {self.id})"
                        }
                    },
                    {
                        "type": "button",
                        "props": {
                            "label": "Update Time",
                            "action": "update_timestamp"  # Use string identifier
                        }
                    }
                ]
            }
        }
    
    def _get_timestamp(self, ui_state=None):
        """
        Get timestamp from UI state or current time.
        
        Args:
            ui_state: Optional state from the UI definition
        """
        # First try to get from UI state
        if ui_state and isinstance(ui_state, dict) and 'timestamp' in ui_state:
            return ui_state['timestamp']
        
        # Fallback to local state
        return timestamp_state.value

# Subscribe to counter changes
@counter_state.subscribe
def on_counter_change(new_value):
    print(f"Counter changed to: {new_value}")

# Subscribe to timestamp changes
@timestamp_state.subscribe
def on_timestamp_change(new_value):
    print(f"Timestamp changed to: {new_value}")

@mix("/")
def home():
    """
    Main page handler.
    
    The server injects _state into the returned dictionary,
    which is then passed to the component's render method.
    """
    # Create components
    counter_component = Counter()
    timer_component = Timer()
    
    # Get UI state from globals if available (for testing)
    ui_state = globals().get('_state', {})
    
    # Build the UI definition
    ui_def = {
        "layout": "column",
        "children": [
            {
                "type": "navbar",
                "props": {
                    "brand": "Cacao Demo",
                    "links": [
                        {"name": "Home", "url": "/"},
                        {"name": "About", "url": "/about"},
                        {"name": "Docs", "url": "/docs"}
                    ]
                }
            },
            {
                "type": "hero",
                "props": {
                    "title": "Cacao with State Management",
                    "subtitle": "Edit this file to see hot reload in action. The components below use reactive state!",
                    "backgroundImage": "/static/images/hero.jpg"
                }
            },
            # Call render() with the UI state
            counter_component.render(ui_state),
            timer_component.render(ui_state),
            {
                "type": "section",
                "props": {
                    "children": [
                        {
                            "type": "text",
                            "props": {
                                "content": "Try editing this text or removing elements to test hot reload."
                            }
                        }
                    ]
                }
            },
            {
                "type": "footer",
                "props": {
                    "text": "© 2025 Cacao Framework - Last Update: " + str(id(home))
                }
            }
        ]
    }
    
    return ui_def

if __name__ == "__main__":
    # Run with verbose=True to see detailed logs
    server = CacaoServer(verbose=True)
    server.run()
