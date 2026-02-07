"""
Main App class for Cacao v2.

The App class is the entry point for building Cacao applications. It provides
decorators for registering event handlers and manages the server lifecycle.
"""

from __future__ import annotations

from typing import Callable, Any, Awaitable, TypeVar
from functools import wraps

from .signal import Signal
from .session import Session, SessionManager
from .events import EventRegistry, EventHandler

T = TypeVar("T")


class App:
    """
    The main Cacao application class.

    Provides decorators for event handlers and manages the server lifecycle.

    Example:
        app = App()
        count = Signal(0, name="count")

        @app.on("increment")
        async def increment(session, event):
            count.set(session, count.get(session) + 1)

        app.run()
    """

    def __init__(self, *, debug: bool = False) -> None:
        """
        Create a new Cacao application.

        Args:
            debug: Enable debug mode with verbose logging
        """
        self.debug = debug
        self.sessions = SessionManager()
        self.events = EventRegistry()
        self._routes: dict[str, Callable[[Session], dict[str, Any]]] = {}
        self._server: Any = None

    def on(
        self, event_name: str
    ) -> Callable[[Callable[..., Awaitable[None]]], EventHandler]:
        """
        Decorator to register an event handler.

        The handler receives (session, event_data) and should be async.

        Args:
            event_name: The event to handle (e.g., "increment", "submit")

        Returns:
            Decorator function

        Example:
            @app.on("increment")
            async def handle_increment(session, event):
                count.set(session, count.get(session) + 1)
        """

        def decorator(
            func: Callable[..., Awaitable[None]]
        ) -> EventHandler:
            @wraps(func)
            async def wrapper(session: Session, data: dict[str, Any]) -> None:
                await func(session, data)

            self.events.register(event_name, wrapper)
            return wrapper

        return decorator

    def route(
        self, path: str
    ) -> Callable[[Callable[[Session], dict[str, Any]]], Callable[[Session], dict[str, Any]]]:
        """
        Decorator to register a route handler.

        Route handlers return the initial state for a session.

        Args:
            path: The route path (e.g., "/", "/dashboard")

        Returns:
            Decorator function

        Example:
            @app.route("/")
            def home(session):
                return {"count": count.get(session)}
        """

        def decorator(
            func: Callable[[Session], dict[str, Any]]
        ) -> Callable[[Session], dict[str, Any]]:
            self._routes[path] = func
            return func

        return decorator

    def bind(self, event_name: str, signal: Signal[T]) -> None:
        """
        Bind an event to a signal for automatic updates.

        When the named event is received, the signal is automatically
        updated with the event's 'value' field. This eliminates boilerplate
        for form inputs.

        Args:
            event_name: The event name (e.g., "name:input")
            signal: The signal to update

        Example:
            name = Signal("", name="name")
            app.bind("name:input", name)

            # Client sends: { type: "event", name: "name:input", data: { value: "John" } }
            # Signal is automatically updated, no handler needed
        """
        self.events.bind(event_name, signal)

    def get_initial_state(self, session: Session, path: str = "/") -> dict[str, Any]:
        """
        Get the initial state for a session.

        If a route handler is registered for the path, it's called.
        Otherwise, returns all signal values for the session.

        Args:
            session: The session to get state for
            path: The route path

        Returns:
            The initial state dict
        """
        if path in self._routes:
            return self._routes[path](session)

        # Default: return all signals
        return Signal.get_all_signals().copy()

    async def handle_event(
        self, session: Session, event_name: str, data: dict[str, Any]
    ) -> None:
        """
        Handle an incoming event from a client.

        Args:
            session: The session that sent the event
            event_name: The event name
            data: The event data
        """
        from .events import Event

        event = Event(name=event_name, data=data)
        await self.events.dispatch(session, event)

    def run(
        self,
        *,
        host: str = "0.0.0.0",
        port: int = 8000,
        reload: bool = False,
    ) -> None:
        """
        Run the Cacao server.

        Args:
            host: Host to bind to
            port: Port to listen on
            reload: Enable auto-reload on code changes
        """
        from .server import run_server

        run_server(self, host=host, port=port, reload=reload)

    async def startup(self) -> None:
        """Called when the server starts. Override for custom startup logic."""
        pass

    async def shutdown(self) -> None:
        """Called when the server stops. Override for custom shutdown logic."""
        pass


# Convenience function to create an app
def create_app(*, debug: bool = False) -> App:
    """
    Create a new Cacao application.

    Args:
        debug: Enable debug mode

    Returns:
        The new App instance
    """
    return App(debug=debug)
