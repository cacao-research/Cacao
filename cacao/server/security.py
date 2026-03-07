"""
Security module for Cacao.

Provides:
    - CSRF protection (token generation, validation middleware)
    - Input sanitization framework (HTML, SQL, path traversal)
    - OAuth2 / OIDC provider support
    - Role-based access control (RBAC)
    - Audit logging
"""

from __future__ import annotations

import hmac
import html
import logging
import re
import secrets
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from .log import get_logger
from .middleware import EventContext, MiddlewareFunc

logger = get_logger("cacao.security")


# =============================================================================
# CSRF Protection
# =============================================================================


class CSRFProtection:
    """
    CSRF token management.

    Generates per-session tokens and validates them on state-changing requests.
    WebSocket connections use a token validated at connection time.
    HTTP POST/PUT/DELETE endpoints validate via header or form field.
    """

    def __init__(self, secret: str | None = None, token_length: int = 32) -> None:
        self._secret = secret or secrets.token_urlsafe(64)
        self._token_length = token_length
        self._session_tokens: dict[str, str] = {}

    def generate_token(self, session_id: str) -> str:
        """Generate a CSRF token bound to a session."""
        token = secrets.token_urlsafe(self._token_length)
        self._session_tokens[session_id] = token
        return token

    def validate_token(self, session_id: str, token: str) -> bool:
        """Validate a CSRF token for a session."""
        expected = self._session_tokens.get(session_id)
        if not expected:
            return False
        return hmac.compare_digest(expected, token)

    def revoke_token(self, session_id: str) -> None:
        """Revoke a session's CSRF token."""
        self._session_tokens.pop(session_id, None)


# Global CSRF instance
_csrf: CSRFProtection | None = None


def enable_csrf(secret: str | None = None) -> CSRFProtection:
    """Enable CSRF protection globally.

    Args:
        secret: Optional secret key. Auto-generated if not provided.

    Returns:
        The CSRFProtection instance.
    """
    global _csrf
    _csrf = CSRFProtection(secret=secret)
    return _csrf


def get_csrf() -> CSRFProtection | None:
    """Get the global CSRF protection instance."""
    return _csrf


def csrf_middleware(
    exempt_events: set[str] | None = None,
) -> MiddlewareFunc:
    """
    Create a CSRF validation middleware for WebSocket events.

    Events in exempt_events skip validation. The token is expected in
    ``ctx.data["_csrf_token"]``.

    Args:
        exempt_events: Event names that skip CSRF checks.

    Returns:
        Middleware function.
    """
    exempt = exempt_events or set()

    async def middleware(
        ctx: EventContext,
        next: Callable[[EventContext], Awaitable[None]],
    ) -> None:
        csrf = get_csrf()
        if not csrf or ctx.event_name in exempt:
            await next(ctx)
            return

        token = ctx.data.pop("_csrf_token", "")
        if not csrf.validate_token(ctx.session.id, token):
            ctx.stop()
            await ctx.session.send(
                {
                    "type": "error",
                    "message": "CSRF validation failed",
                    "code": "CSRF_ERROR",
                }
            )
            _audit_log(
                "csrf_failure",
                session_id=ctx.session.id,
                event=ctx.event_name,
            )
            return

        await next(ctx)

    return middleware


# =============================================================================
# Input Sanitization
# =============================================================================


class Sanitizer:
    """
    Input sanitization framework.

    Provides methods to sanitize user input against common injection attacks:
    HTML/XSS, SQL injection patterns, and path traversal.
    """

    # Patterns that suggest SQL injection attempts
    _SQL_PATTERNS = re.compile(
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|EXEC|UNION|"
        r"TRUNCATE|GRANT|REVOKE)\b\s)"
        r"|(-{2})"  # SQL comment
        r"|(;\s*\b(DROP|DELETE|INSERT|UPDATE)\b)",
        re.IGNORECASE,
    )

    # Path traversal patterns
    _PATH_TRAVERSAL = re.compile(r"(\.\.[\\/])|(%2e%2e[\\/])", re.IGNORECASE)

    # Script tags and event handlers
    _XSS_PATTERNS = re.compile(
        r"<\s*script|javascript\s*:|on\w+\s*=|<\s*iframe|<\s*object|<\s*embed",
        re.IGNORECASE,
    )

    @staticmethod
    def html(value: str) -> str:
        """Escape HTML entities to prevent XSS.

        Args:
            value: Raw user input.

        Returns:
            HTML-escaped string.
        """
        return html.escape(value, quote=True)

    @staticmethod
    def strip_tags(value: str) -> str:
        """Remove all HTML tags from input.

        Args:
            value: Raw user input.

        Returns:
            String with tags removed.
        """
        return re.sub(r"<[^>]*>", "", value)

    @classmethod
    def check_sql_injection(cls, value: str) -> bool:
        """Check if a string contains SQL injection patterns.

        Args:
            value: Input to check.

        Returns:
            True if suspicious patterns are found.
        """
        return bool(cls._SQL_PATTERNS.search(value))

    @classmethod
    def check_path_traversal(cls, value: str) -> bool:
        """Check if a string contains path traversal patterns.

        Args:
            value: Input to check.

        Returns:
            True if path traversal is detected.
        """
        return bool(cls._PATH_TRAVERSAL.search(value))

    @classmethod
    def check_xss(cls, value: str) -> bool:
        """Check if a string contains XSS patterns.

        Args:
            value: Input to check.

        Returns:
            True if XSS patterns are detected.
        """
        return bool(cls._XSS_PATTERNS.search(value))

    @classmethod
    def sanitize(cls, value: str, *, allow_html: bool = False) -> str:
        """Sanitize a string value.

        Escapes HTML (unless allow_html=True) and rejects dangerous patterns.

        Args:
            value: Raw user input.
            allow_html: If True, skip HTML escaping.

        Returns:
            Sanitized string.

        Raises:
            ValueError: If SQL injection or path traversal is detected.
        """
        if cls.check_sql_injection(value):
            raise ValueError("Input contains potentially dangerous SQL patterns")
        if cls.check_path_traversal(value):
            raise ValueError("Input contains path traversal patterns")
        if not allow_html:
            value = cls.html(value)
        return value

    @classmethod
    def sanitize_dict(
        cls,
        data: dict[str, Any],
        *,
        allow_html_fields: set[str] | None = None,
        skip_fields: set[str] | None = None,
    ) -> dict[str, Any]:
        """Sanitize all string values in a dictionary.

        Args:
            data: Dictionary of event data.
            allow_html_fields: Field names where HTML is allowed.
            skip_fields: Field names to skip entirely.

        Returns:
            Sanitized copy of the dictionary.
        """
        allow_html = allow_html_fields or set()
        skip = skip_fields or set()
        result: dict[str, Any] = {}
        for key, value in data.items():
            if key in skip:
                result[key] = value
            elif isinstance(value, str):
                result[key] = cls.sanitize(value, allow_html=key in allow_html)
            elif isinstance(value, dict):
                result[key] = cls.sanitize_dict(
                    value, allow_html_fields=allow_html, skip_fields=skip
                )
            else:
                result[key] = value
        return result


def sanitization_middleware(
    allow_html_fields: set[str] | None = None,
    skip_fields: set[str] | None = None,
    skip_events: set[str] | None = None,
) -> MiddlewareFunc:
    """
    Create an input sanitization middleware.

    Sanitizes all string values in event data before they reach handlers.

    Args:
        allow_html_fields: Field names where HTML content is allowed.
        skip_fields: Field names to skip sanitization on.
        skip_events: Event names to skip entirely.

    Returns:
        Middleware function.
    """
    _skip_events = skip_events or set()

    async def middleware(
        ctx: EventContext,
        next: Callable[[EventContext], Awaitable[None]],
    ) -> None:
        if ctx.event_name in _skip_events:
            await next(ctx)
            return

        try:
            ctx.data = Sanitizer.sanitize_dict(
                ctx.data,
                allow_html_fields=allow_html_fields,
                skip_fields=skip_fields,
            )
        except ValueError as e:
            ctx.stop()
            await ctx.session.send(
                {
                    "type": "error",
                    "message": str(e),
                    "code": "SANITIZATION_ERROR",
                }
            )
            _audit_log(
                "sanitization_block",
                session_id=ctx.session.id,
                event=ctx.event_name,
                reason=str(e),
            )
            return

        await next(ctx)

    return middleware


# =============================================================================
# OAuth2 / OIDC Provider Support
# =============================================================================


@dataclass
class OAuth2Config:
    """Configuration for an OAuth2 / OIDC provider.

    Attributes:
        provider_name: Human-readable provider name (e.g. "Google", "GitHub").
        client_id: OAuth2 client ID.
        client_secret: OAuth2 client secret.
        authorize_url: Authorization endpoint URL.
        token_url: Token endpoint URL.
        userinfo_url: UserInfo endpoint URL (OIDC).
        scopes: Requested scopes.
        redirect_uri: Redirect URI after authorization.
        extra_params: Additional parameters for the authorization request.
    """

    provider_name: str
    client_id: str
    client_secret: str
    authorize_url: str
    token_url: str
    userinfo_url: str = ""
    scopes: list[str] = field(default_factory=lambda: ["openid", "profile", "email"])
    redirect_uri: str = ""
    extra_params: dict[str, str] = field(default_factory=dict)


# Pre-configured provider templates
OAUTH2_PROVIDERS: dict[str, dict[str, str]] = {
    "google": {
        "authorize_url": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "userinfo_url": "https://openidconnect.googleapis.com/v1/userinfo",
    },
    "github": {
        "authorize_url": "https://github.com/login/oauth/authorize",
        "token_url": "https://github.com/login/oauth/access_token",
        "userinfo_url": "https://api.github.com/user",
    },
    "microsoft": {
        "authorize_url": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
        "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
        "userinfo_url": "https://graph.microsoft.com/oidc/userinfo",
    },
}


class OAuth2Provider:
    """
    OAuth2 / OIDC authentication provider for Cacao.

    Handles the OAuth2 authorization code flow:
    1. Generate authorization URL -> redirect user
    2. Handle callback with authorization code
    3. Exchange code for tokens
    4. Fetch user info from provider

    Integrates with Cacao's AuthProvider system.
    """

    def __init__(self, config: OAuth2Config) -> None:
        self.config = config
        self._states: dict[str, float] = {}  # state -> timestamp

    @classmethod
    def from_preset(
        cls,
        provider: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str = "",
        scopes: list[str] | None = None,
    ) -> OAuth2Provider:
        """Create an OAuth2Provider from a preset (google, github, microsoft).

        Args:
            provider: Provider name (google, github, microsoft).
            client_id: OAuth2 client ID.
            client_secret: OAuth2 client secret.
            redirect_uri: Redirect URI.
            scopes: Override default scopes.

        Returns:
            Configured OAuth2Provider.

        Raises:
            ValueError: If provider name is not recognized.
        """
        preset = OAUTH2_PROVIDERS.get(provider.lower())
        if not preset:
            raise ValueError(
                f"Unknown provider '{provider}'. Available: {', '.join(OAUTH2_PROVIDERS)}"
            )

        config = OAuth2Config(
            provider_name=provider.capitalize(),
            client_id=client_id,
            client_secret=client_secret,
            authorize_url=preset["authorize_url"],
            token_url=preset["token_url"],
            userinfo_url=preset.get("userinfo_url", ""),
            redirect_uri=redirect_uri,
            scopes=scopes or ["openid", "profile", "email"],
        )
        return cls(config)

    def get_authorization_url(self, session_id: str = "") -> str:
        """Generate the authorization URL for the OAuth2 flow.

        Args:
            session_id: Optional session ID to bind the state to.

        Returns:
            Authorization URL to redirect the user to.
        """
        state = secrets.token_urlsafe(32)
        self._states[state] = time.time()
        self._cleanup_states()

        params = {
            "client_id": self.config.client_id,
            "response_type": "code",
            "scope": " ".join(self.config.scopes),
            "state": state,
        }
        if self.config.redirect_uri:
            params["redirect_uri"] = self.config.redirect_uri
        params.update(self.config.extra_params)

        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.config.authorize_url}?{query}"

    def validate_state(self, state: str) -> bool:
        """Validate an OAuth2 state parameter.

        Args:
            state: The state value from the callback.

        Returns:
            True if the state is valid and not expired.
        """
        ts = self._states.pop(state, None)
        if ts is None:
            return False
        # States expire after 10 minutes
        return (time.time() - ts) < 600

    async def exchange_code(self, code: str) -> dict[str, Any]:
        """Exchange an authorization code for tokens.

        Requires httpx or aiohttp to be installed. Returns the token response
        as a dictionary.

        Args:
            code: The authorization code from the callback.

        Returns:
            Token response dict with access_token, etc.

        Raises:
            RuntimeError: If no HTTP client library is available.
        """
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
        }
        if self.config.redirect_uri:
            data["redirect_uri"] = self.config.redirect_uri

        try:
            import httpx

            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    self.config.token_url,
                    data=data,
                    headers={"Accept": "application/json"},
                )
                result: dict[str, Any] = resp.json()
                return result
        except ImportError:
            pass

        try:
            import aiohttp

            async with aiohttp.ClientSession() as client_session:
                async with client_session.post(
                    self.config.token_url,
                    data=data,
                    headers={"Accept": "application/json"},
                ) as aio_resp:
                    return await aio_resp.json()  # type: ignore[no-any-return]
        except ImportError:
            raise RuntimeError(
                "OAuth2 code exchange requires 'httpx' or 'aiohttp'. Install one: pip install httpx"
            )

    async def get_userinfo(self, access_token: str) -> dict[str, Any]:
        """Fetch user info from the provider.

        Args:
            access_token: The OAuth2 access token.

        Returns:
            User info dictionary from the provider.

        Raises:
            RuntimeError: If no HTTP client library is available.
        """
        if not self.config.userinfo_url:
            return {}

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

        try:
            import httpx

            async with httpx.AsyncClient() as client:
                resp = await client.get(self.config.userinfo_url, headers=headers)
                info: dict[str, Any] = resp.json()
                return info
        except ImportError:
            pass

        try:
            import aiohttp

            async with aiohttp.ClientSession() as client_session:
                async with client_session.get(
                    self.config.userinfo_url, headers=headers
                ) as aio_resp:
                    return await aio_resp.json()  # type: ignore[no-any-return]
        except ImportError:
            raise RuntimeError(
                "OAuth2 userinfo fetch requires 'httpx' or 'aiohttp'. "
                "Install one: pip install httpx"
            )

    def _cleanup_states(self, max_age: float = 600) -> None:
        """Remove expired states."""
        now = time.time()
        expired = [s for s, ts in self._states.items() if (now - ts) > max_age]
        for s in expired:
            del self._states[s]


# Global OAuth2 providers registry
_oauth2_providers: dict[str, OAuth2Provider] = {}


def register_oauth2(name: str, provider: OAuth2Provider) -> None:
    """Register an OAuth2 provider.

    Args:
        name: Provider key (e.g. "google").
        provider: OAuth2Provider instance.
    """
    _oauth2_providers[name] = provider
    _audit_log("oauth2_registered", provider=name)


def get_oauth2(name: str) -> OAuth2Provider | None:
    """Get a registered OAuth2 provider by name."""
    return _oauth2_providers.get(name)


def get_all_oauth2() -> dict[str, OAuth2Provider]:
    """Get all registered OAuth2 providers."""
    return dict(_oauth2_providers)


# =============================================================================
# Role-Based Access Control (RBAC)
# =============================================================================


@dataclass
class Role:
    """
    A role with a set of permissions.

    Attributes:
        name: Role name (e.g. "admin", "editor", "viewer").
        permissions: Set of permission strings this role grants.
        description: Human-readable description.
        inherits: Roles this role inherits permissions from.
    """

    name: str
    permissions: set[str] = field(default_factory=set)
    description: str = ""
    inherits: list[str] = field(default_factory=list)


class RBAC:
    """
    Role-Based Access Control system.

    Manages roles with permission inheritance and provides
    middleware for enforcing access control on events.

    Example:
        rbac = RBAC()
        rbac.add_role("viewer", permissions={"read"})
        rbac.add_role("editor", permissions={"write"}, inherits=["viewer"])
        rbac.add_role("admin", permissions={"delete", "manage"}, inherits=["editor"])

        # Check permissions
        rbac.has_permission("admin", "read")   # True (inherited from viewer)
        rbac.has_permission("editor", "delete") # False
    """

    def __init__(self) -> None:
        self._roles: dict[str, Role] = {}
        self._user_roles: dict[str, set[str]] = {}  # username -> role names

    def add_role(
        self,
        name: str,
        *,
        permissions: set[str] | None = None,
        description: str = "",
        inherits: list[str] | None = None,
    ) -> Role:
        """Add a role to the RBAC system.

        Args:
            name: Role name.
            permissions: Permissions granted by this role.
            description: Human-readable description.
            inherits: Roles to inherit permissions from.

        Returns:
            The created Role.
        """
        role = Role(
            name=name,
            permissions=permissions or set(),
            description=description,
            inherits=inherits or [],
        )
        self._roles[name] = role
        _audit_log("rbac_role_added", role=name, permissions=list(role.permissions))
        return role

    def remove_role(self, name: str) -> None:
        """Remove a role from the RBAC system."""
        self._roles.pop(name, None)
        # Remove role from all users
        for roles in self._user_roles.values():
            roles.discard(name)

    def get_role(self, name: str) -> Role | None:
        """Get a role by name."""
        return self._roles.get(name)

    def get_all_roles(self) -> dict[str, Role]:
        """Get all defined roles."""
        return dict(self._roles)

    def get_role_permissions(self, role_name: str) -> set[str]:
        """Get all permissions for a role, including inherited ones.

        Args:
            role_name: The role to resolve permissions for.

        Returns:
            Complete set of permissions including inherited ones.
        """
        visited: set[str] = set()
        return self._resolve_permissions(role_name, visited)

    def _resolve_permissions(self, role_name: str, visited: set[str]) -> set[str]:
        """Recursively resolve permissions with cycle detection."""
        if role_name in visited:
            return set()
        visited.add(role_name)

        role = self._roles.get(role_name)
        if not role:
            return set()

        perms = set(role.permissions)
        for parent in role.inherits:
            perms |= self._resolve_permissions(parent, visited)
        return perms

    def has_permission(self, role_name: str, permission: str) -> bool:
        """Check if a role has a specific permission.

        Args:
            role_name: The role to check.
            permission: The permission to look for.

        Returns:
            True if the role (or its parents) has the permission.
        """
        return permission in self.get_role_permissions(role_name)

    def assign_role(self, username: str, role_name: str) -> None:
        """Assign a role to a user.

        Args:
            username: The user to assign the role to.
            role_name: The role to assign.
        """
        if username not in self._user_roles:
            self._user_roles[username] = set()
        self._user_roles[username].add(role_name)
        _audit_log("rbac_role_assigned", username=username, role=role_name)

    def revoke_role(self, username: str, role_name: str) -> None:
        """Revoke a role from a user."""
        if username in self._user_roles:
            self._user_roles[username].discard(role_name)
            _audit_log("rbac_role_revoked", username=username, role=role_name)

    def get_user_roles(self, username: str) -> set[str]:
        """Get all roles assigned to a user."""
        return set(self._user_roles.get(username, set()))

    def get_user_permissions(self, username: str) -> set[str]:
        """Get all permissions for a user across all their roles.

        Args:
            username: The user to check.

        Returns:
            Combined permissions from all assigned roles.
        """
        perms: set[str] = set()
        for role_name in self.get_user_roles(username):
            perms |= self.get_role_permissions(role_name)
        return perms

    def user_has_permission(self, username: str, permission: str) -> bool:
        """Check if a user has a specific permission through any of their roles.

        Args:
            username: The user to check.
            permission: The permission to look for.

        Returns:
            True if any of the user's roles grants the permission.
        """
        return permission in self.get_user_permissions(username)


# Global RBAC instance
_rbac: RBAC | None = None


def get_rbac() -> RBAC:
    """Get the global RBAC instance, creating it if needed."""
    global _rbac
    if _rbac is None:
        _rbac = RBAC()
    return _rbac


def set_rbac(rbac: RBAC) -> None:
    """Set the global RBAC instance."""
    global _rbac
    _rbac = rbac


def rbac_middleware(
    event_permissions: dict[str, str | list[str]],
    *,
    public_events: set[str] | None = None,
) -> MiddlewareFunc:
    """
    Create RBAC enforcement middleware.

    Maps event names to required permissions. The user's roles are checked
    against the required permissions via the global RBAC instance.

    Args:
        event_permissions: Dict mapping event names to required permission(s).
            A string means one permission required; a list means ANY of them.
        public_events: Events that skip permission checks.

    Returns:
        Middleware function.
    """
    public = public_events or set()

    async def middleware(
        ctx: EventContext,
        next: Callable[[EventContext], Awaitable[None]],
    ) -> None:
        if ctx.event_name in public:
            await next(ctx)
            return

        required = event_permissions.get(ctx.event_name)
        if not required:
            # No permission requirement for this event
            await next(ctx)
            return

        # Get username from session
        user = ctx.session.user
        if not user:
            ctx.stop()
            await ctx.session.send(
                {
                    "type": "error",
                    "message": "Authentication required",
                    "code": "AUTH_REQUIRED",
                }
            )
            return

        username = user.username if hasattr(user, "username") else str(user)
        rbac = get_rbac()

        # Check permissions
        if isinstance(required, str):
            required_perms = [required]
        else:
            required_perms = list(required)

        has_any = any(rbac.user_has_permission(username, p) for p in required_perms)
        if not has_any:
            ctx.stop()
            await ctx.session.send(
                {
                    "type": "error",
                    "message": f"Permission denied. Required: {', '.join(required_perms)}",
                    "code": "PERMISSION_DENIED",
                }
            )
            _audit_log(
                "rbac_denied",
                username=username,
                event=ctx.event_name,
                required=required_perms,
            )
            return

        _audit_log(
            "rbac_allowed",
            username=username,
            event=ctx.event_name,
            level="DEBUG",
        )
        await next(ctx)

    return middleware


def require_role(*roles: str) -> Callable[..., Any]:
    """
    Decorator to require specific role(s) on an event handler.

    The user must have at least one of the specified roles.

    Args:
        roles: Required role name(s).

    Example:
        @c.on("delete_user")
        @require_role("admin")
        async def delete_user(session, data):
            ...
    """
    from functools import wraps

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(session: Any, data: dict[str, Any]) -> None:
            user = session.user
            if not user:
                await session.send(
                    {
                        "type": "error",
                        "message": "Authentication required",
                        "code": "AUTH_REQUIRED",
                    }
                )
                return

            username = user.username if hasattr(user, "username") else str(user)
            rbac = get_rbac()
            user_roles = rbac.get_user_roles(username)

            if not user_roles.intersection(set(roles)):
                await session.send(
                    {
                        "type": "error",
                        "message": f"Role required: {', '.join(roles)}",
                        "code": "ROLE_DENIED",
                    }
                )
                _audit_log(
                    "role_denied",
                    username=username,
                    required_roles=list(roles),
                )
                return

            await func(session, data)

        return wrapper

    return decorator


# =============================================================================
# Audit Logging
# =============================================================================


class AuditEventType(str, Enum):
    """Standard audit event types."""

    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    LOGOUT = "logout"
    SESSION_START = "session_start"
    SESSION_END = "session_end"
    PERMISSION_DENIED = "permission_denied"
    CSRF_FAILURE = "csrf_failure"
    SANITIZATION_BLOCK = "sanitization_block"
    RBAC_DENIED = "rbac_denied"
    RBAC_ALLOWED = "rbac_allowed"
    ROLE_ASSIGNED = "rbac_role_assigned"
    ROLE_REVOKED = "rbac_role_revoked"
    OAUTH2_REGISTERED = "oauth2_registered"
    CUSTOM = "custom"


@dataclass
class AuditEntry:
    """A single audit log entry.

    Attributes:
        timestamp: When the event occurred.
        event_type: Type of audit event.
        details: Additional details.
        session_id: Associated session ID.
        username: Associated username.
        ip_address: Client IP address.
    """

    timestamp: datetime
    event_type: str
    details: dict[str, Any]
    session_id: str = ""
    username: str = ""
    ip_address: str = ""


class AuditLogger:
    """
    Structured audit logging for security events.

    Writes audit entries to both the standard logging system and
    an in-memory buffer that can be queried or exported.

    The logger can be extended with custom handlers for external
    systems (databases, SIEM, etc.).
    """

    def __init__(self, max_entries: int = 10000) -> None:
        self._entries: list[AuditEntry] = []
        self._max_entries = max_entries
        self._handlers: list[Callable[[AuditEntry], Any]] = []
        self._logger = get_logger("cacao.audit")

    def log(
        self,
        event_type: str,
        *,
        session_id: str = "",
        username: str = "",
        ip_address: str = "",
        level: str = "INFO",
        **details: Any,
    ) -> AuditEntry:
        """Record an audit event.

        Args:
            event_type: Type of security event.
            session_id: Associated session.
            username: Associated user.
            ip_address: Client IP.
            level: Log level (DEBUG, INFO, WARNING, ERROR).
            **details: Additional event details.

        Returns:
            The created AuditEntry.
        """
        entry = AuditEntry(
            timestamp=datetime.now(),
            event_type=event_type,
            details=details,
            session_id=session_id,
            username=username,
            ip_address=ip_address,
        )

        # Add to buffer (ring buffer behavior)
        self._entries.append(entry)
        if len(self._entries) > self._max_entries:
            self._entries = self._entries[-self._max_entries :]

        # Log to standard logger
        log_level = getattr(logging, level.upper(), logging.INFO)
        detail_str = " ".join(f"{k}={v}" for k, v in details.items())
        msg = f"[audit] {event_type}"
        if session_id:
            msg += f" session={session_id[:8]}"
        if username:
            msg += f" user={username}"
        if detail_str:
            msg += f" {detail_str}"
        self._logger.log(log_level, msg, extra={"label": "audit"})

        # Call custom handlers
        for handler in self._handlers:
            try:
                handler(entry)
            except Exception:
                self._logger.exception("Audit handler error")

        return entry

    def add_handler(self, handler: Callable[[AuditEntry], Any]) -> None:
        """Add a custom audit handler.

        Handlers are called synchronously for each audit event.
        For async operations, use a queue or background task.

        Args:
            handler: Callable that receives an AuditEntry.
        """
        self._handlers.append(handler)

    def get_entries(
        self,
        *,
        event_type: str | None = None,
        username: str | None = None,
        session_id: str | None = None,
        since: datetime | None = None,
        limit: int = 100,
    ) -> list[AuditEntry]:
        """Query audit entries with optional filters.

        Args:
            event_type: Filter by event type.
            username: Filter by username.
            session_id: Filter by session ID.
            since: Only entries after this time.
            limit: Maximum entries to return.

        Returns:
            Matching audit entries, most recent first.
        """
        results = self._entries
        if event_type:
            results = [e for e in results if e.event_type == event_type]
        if username:
            results = [e for e in results if e.username == username]
        if session_id:
            results = [e for e in results if e.session_id == session_id]
        if since:
            results = [e for e in results if e.timestamp >= since]
        return list(reversed(results[-limit:]))

    def clear(self) -> None:
        """Clear all audit entries."""
        self._entries.clear()

    def export(self) -> list[dict[str, Any]]:
        """Export all audit entries as serializable dicts."""
        return [
            {
                "timestamp": e.timestamp.isoformat(),
                "event_type": e.event_type,
                "session_id": e.session_id,
                "username": e.username,
                "ip_address": e.ip_address,
                "details": e.details,
            }
            for e in self._entries
        ]


# Global audit logger
_audit_logger: AuditLogger | None = None


def get_audit_logger() -> AuditLogger:
    """Get the global audit logger, creating it if needed."""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger


def set_audit_logger(audit_logger: AuditLogger) -> None:
    """Set the global audit logger."""
    global _audit_logger
    _audit_logger = audit_logger


def _audit_log(event_type: str, **kwargs: Any) -> None:
    """Convenience function to log an audit event."""
    get_audit_logger().log(event_type, **kwargs)


def audit_middleware() -> MiddlewareFunc:
    """
    Create an audit logging middleware.

    Logs all events with session and user context.

    Returns:
        Middleware function.
    """

    async def middleware(
        ctx: EventContext,
        next: Callable[[EventContext], Awaitable[None]],
    ) -> None:
        user = ctx.session.user
        username = ""
        if user:
            username = user.username if hasattr(user, "username") else str(user)

        _audit_log(
            "event",
            session_id=ctx.session.id,
            username=username,
            event=ctx.event_name,
            level="DEBUG",
        )

        await next(ctx)

    return middleware
