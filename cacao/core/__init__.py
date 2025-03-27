"""
Core module initialization for the Cacao framework.
"""

from .decorators import mix, page, documented
from .server import CacaoServer
from .state import State, StateChange
from ..ui.components.base import Component, ComponentProps

# Initialize state
from .decorators import ROUTES, clear_routes

def run(verbose: bool = False):
    """Run the Cacao development server."""
    server = CacaoServer(verbose=verbose)
    try:
        server.run()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error running server: {str(e)}")
        raise

__all__ = [
    "mix",
    "page",
    "documented",
    "run",
    "CacaoServer",
    "ROUTES",
    "clear_routes",
    "State",
    "StateChange",
    "Component",
    "ComponentProps"
]
