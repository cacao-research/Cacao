from cacao import mix, run, State, Component, run_desktop
from cacao.core.server import CacaoServer
from cacao.core.pwa import PWASupport
from datetime import datetime

# Create separate reactive states for each component
counter_state = State(0)
timestamp_state = State(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
online_state = State(True)  # New state for online/offline status

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
    """Main page handler with PWA support."""
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
                    "brand": "Cacao PWA Demo",
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
                    "title": "Cacao Progressive Web App 2",
                    "subtitle": "This app works offline! Try turning off your network connection.",
                    "backgroundImage": "/static/images/hero.jpg"
                }
            },
            counter_component.render(ui_state),
            timer_component.render(ui_state),
            {
                "type": "section",
                "props": {
                    "children": [
                        {
                            "type": "text",
                            "props": {
                                "content": "This app can be installed on your device! Look for the install prompt in your browser."
                            }
                        }
                    ]
                }
            },
            {
                "type": "footer",
                "props": {
                    "text": "© 2025 Cacao Framework - PWA Enabled"
                }
            }
        ]
    }
    
    return ui_def

if __name__ == "__main__":
    # Run with PWA support enabled

    run_desktop(
        title="Cacao Desktop App",
        width=1024,
        height=768,
        resizable=True,
        fullscreen=False
    )