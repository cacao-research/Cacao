"""
Middleware system for Cacao v2 events.

Middleware allows intercepting and modifying events before they
reach handlers. This is useful for logging, authentication,
rate limiting, validation, and more.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Awaitable, TypeVar
from dataclasses import dataclass, field
from functools import wraps
import asyncio
import time

if TYPE_CHECKING:
    from .session import Session

T = TypeVar("T")


@dataclass
class EventContext:
    """
    Context passed through middleware chain.

    Contains the event data and allows middleware to modify it
    or stop processing.
    """

    session: "Session"
    event_name: str
    data: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)
    _stopped: bool = field(default=False, repr=False)

    def stop(self) -> None:
        """Stop the event from being processed further."""
        self._stopped = True

    @property
    def stopped(self) -> bool:
        """Whether the event has been stopped."""
        return self._stopped


# Middleware function type
MiddlewareFunc = Callable[
    [EventContext, Callable[[EventContext], Awaitable[None]]],
    Awaitable[None],
]


class MiddlewareChain:
    """
    Chain of middleware functions.

    Middleware is executed in order, each calling the next.
    Any middleware can stop the chain by not calling next.

    Example:
        chain = MiddlewareChain()

        @chain.use
        async def logging_middleware(ctx, next):
            print(f"Event: {ctx.event_name}")
            await next(ctx)
            print(f"Event processed")

        @chain.use
        async def auth_middleware(ctx, next):
            if not ctx.session.authenticated:
                ctx.stop()
                return
            await next(ctx)
    """

    def __init__(self) -> None:
        self._middleware: list[MiddlewareFunc] = []

    def use(
        self,
        middleware: MiddlewareFunc | None = None,
    ) -> MiddlewareFunc | Callable[[MiddlewareFunc], MiddlewareFunc]:
        """
        Add middleware to the chain.

        Can be used as a decorator or called directly.

        Args:
            middleware: The middleware function

        Returns:
            The middleware function (for decorator use)
        """
        if middleware is None:
            # Used as decorator without arguments
            def decorator(fn: MiddlewareFunc) -> MiddlewareFunc:
                self._middleware.append(fn)
                return fn
            return decorator

        self._middleware.append(middleware)
        return middleware

    async def execute(
        self,
        ctx: EventContext,
        handler: Callable[[EventContext], Awaitable[None]],
    ) -> None:
        """
        Execute the middleware chain and then the handler.

        Args:
            ctx: The event context
            handler: The final handler to call
        """
        if ctx.stopped:
            return

        async def run_chain(
            middlewares: list[MiddlewareFunc],
            ctx: EventContext,
        ) -> None:
            if ctx.stopped:
                return

            if not middlewares:
                # End of chain, call the handler
                await handler(ctx)
                return

            # Get next middleware
            current = middlewares[0]
            remaining = middlewares[1:]

            # Create next function
            async def next_fn(ctx: EventContext) -> None:
                await run_chain(remaining, ctx)

            # Call current middleware
            await current(ctx, next_fn)

        await run_chain(self._middleware, ctx)

    def clear(self) -> None:
        """Remove all middleware."""
        self._middleware.clear()


# Built-in middleware


def logging_middleware(
    log_fn: Callable[[str], None] = print,
) -> MiddlewareFunc:
    """
    Create a logging middleware.

    Args:
        log_fn: Function to call with log messages

    Returns:
        Middleware function
    """
    async def middleware(
        ctx: EventContext,
        next: Callable[[EventContext], Awaitable[None]],
    ) -> None:
        start = time.time()
        log_fn(f"[{ctx.session.id[:8]}] Event: {ctx.event_name}")
        await next(ctx)
        elapsed = (time.time() - start) * 1000
        log_fn(f"[{ctx.session.id[:8]}] Completed in {elapsed:.2f}ms")

    return middleware


def rate_limit_middleware(
    max_requests: int = 100,
    window_seconds: float = 60.0,
    key_fn: Callable[[EventContext], str] | None = None,
) -> MiddlewareFunc:
    """
    Create a rate limiting middleware.

    Args:
        max_requests: Maximum requests per window
        window_seconds: Time window in seconds
        key_fn: Function to generate rate limit key (default: session ID)

    Returns:
        Middleware function
    """
    # Track requests: key -> list of timestamps
    requests: dict[str, list[float]] = {}

    def default_key(ctx: EventContext) -> str:
        return ctx.session.id

    get_key = key_fn or default_key

    async def middleware(
        ctx: EventContext,
        next: Callable[[EventContext], Awaitable[None]],
    ) -> None:
        key = get_key(ctx)
        now = time.time()
        cutoff = now - window_seconds

        # Get or create request list
        if key not in requests:
            requests[key] = []

        # Remove old requests
        requests[key] = [t for t in requests[key] if t > cutoff]

        # Check rate limit
        if len(requests[key]) >= max_requests:
            ctx.metadata["rate_limited"] = True
            ctx.stop()
            # Send error to client
            await ctx.session.send({
                "type": "error",
                "message": "Rate limit exceeded",
                "code": "RATE_LIMIT",
            })
            return

        # Record this request
        requests[key].append(now)
        await next(ctx)

    return middleware


def validation_middleware(
    validators: dict[str, Callable[[dict[str, Any]], bool | str]],
) -> MiddlewareFunc:
    """
    Create a validation middleware.

    Args:
        validators: Dict mapping event names to validator functions.
                   Validators return True if valid, or an error message.

    Returns:
        Middleware function
    """
    async def middleware(
        ctx: EventContext,
        next: Callable[[EventContext], Awaitable[None]],
    ) -> None:
        validator = validators.get(ctx.event_name)
        if validator:
            result = validator(ctx.data)
            if result is not True:
                error_msg = result if isinstance(result, str) else "Validation failed"
                ctx.stop()
                await ctx.session.send({
                    "type": "error",
                    "message": error_msg,
                    "code": "VALIDATION_ERROR",
                })
                return

        await next(ctx)

    return middleware


def auth_middleware(
    check_auth: Callable[["Session"], bool | Awaitable[bool]],
    public_events: set[str] | None = None,
) -> MiddlewareFunc:
    """
    Create an authentication middleware.

    Args:
        check_auth: Function to check if session is authenticated
        public_events: Event names that don't require auth

    Returns:
        Middleware function
    """
    public = public_events or set()

    async def middleware(
        ctx: EventContext,
        next: Callable[[EventContext], Awaitable[None]],
    ) -> None:
        # Skip auth for public events
        if ctx.event_name in public:
            await next(ctx)
            return

        # Check authentication
        result = check_auth(ctx.session)
        if asyncio.iscoroutine(result):
            result = await result

        if not result:
            ctx.stop()
            await ctx.session.send({
                "type": "error",
                "message": "Authentication required",
                "code": "AUTH_REQUIRED",
            })
            return

        await next(ctx)

    return middleware


def transform_middleware(
    transformers: dict[str, Callable[[dict[str, Any]], dict[str, Any]]],
) -> MiddlewareFunc:
    """
    Create a data transformation middleware.

    Args:
        transformers: Dict mapping event names to transform functions

    Returns:
        Middleware function
    """
    async def middleware(
        ctx: EventContext,
        next: Callable[[EventContext], Awaitable[None]],
    ) -> None:
        transformer = transformers.get(ctx.event_name)
        if transformer:
            ctx.data = transformer(ctx.data)

        await next(ctx)

    return middleware


def timeout_middleware(timeout_seconds: float = 30.0) -> MiddlewareFunc:
    """
    Create a timeout middleware.

    Args:
        timeout_seconds: Maximum time for handler execution

    Returns:
        Middleware function
    """
    async def middleware(
        ctx: EventContext,
        next: Callable[[EventContext], Awaitable[None]],
    ) -> None:
        try:
            await asyncio.wait_for(next(ctx), timeout=timeout_seconds)
        except asyncio.TimeoutError:
            await ctx.session.send({
                "type": "error",
                "message": "Request timed out",
                "code": "TIMEOUT",
            })

    return middleware
