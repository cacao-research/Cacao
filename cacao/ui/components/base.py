"""
Base component system for Cacao.
Provides the foundation for creating reusable UI components.
"""

from typing import Any, Dict, List, Optional, Union
from abc import ABC, abstractmethod
import json
import weakref
from dataclasses import dataclass, field

from ...core.state import StateChange

@dataclass
class ComponentProps:
    """Base class for component properties."""
    children: List[Any] = field(default_factory=list)
    className: Optional[str] = None
    style: Dict[str, str] = field(default_factory=dict)

class Component(ABC):
    """
    Base class for all Cacao components.
    
    Usage:
        class MyComponent(Component):
            def __init__(self, title: str):
                super().__init__()
                self.title = title
            
            def render(self):
                return {
                    "type": "section",
                    "props": {
                        "children": [
                            {
                                "type": "text",
                                "props": {"content": self.title}
                            }
                        ]
                    }
                }
    """
    
    def __init__(self):
        self._parent: Optional[weakref.ref] = None
        self._children: List['Component'] = []
        self._mounted = False
        
    @abstractmethod
    def render(self) -> Dict[str, Any]:
        """
        Render the component's UI definition.
        
        Returns:
            A dictionary defining the component's UI structure
        """
        raise NotImplementedError("Components must implement render()")
    
    def mount(self) -> None:
        """Called when the component is first added to the UI."""
        self._mounted = True
        
    def unmount(self) -> None:
        """Called when the component is removed from the UI."""
        self._mounted = False
        
    async def handle_state_change(self, change: StateChange) -> None:
        """
        Handle changes in state that affect this component.
        
        Args:
            change: The state change that occurred
        """
        # Default implementation triggers a re-render
        if self._mounted:
            await self.update()
    
    async def update(self) -> None:
        """Force a component update."""
        if not self._mounted:
            return
            
        # Get fresh render output
        try:
            ui = self.render()
            # Broadcast update through WebSocket (handled by server)
            await self._broadcast_update(ui)
        except Exception as e:
            print(f"Error updating component: {e}")
    
    async def _broadcast_update(self, ui: Dict[str, Any]) -> None:
        """Send UI update through WebSocket."""
        # This will be implemented by the server
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert component to dictionary representation."""
        rendered = self.render()
        if not isinstance(rendered, dict):
            raise ValueError(f"Component {self.__class__.__name__} render() must return a dictionary")
        return rendered
    
    def __call__(self) -> Dict[str, Any]:
        """Make components callable to get their rendered form."""
        return self.to_dict()
        
    def to_json(self) -> str:
        """Convert component to JSON string."""
        return json.dumps(self.to_dict())
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(mounted={self._mounted})"
