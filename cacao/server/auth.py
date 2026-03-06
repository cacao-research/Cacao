"""
Authentication system for Cacao.

Provides base AuthProvider class and a SimpleAuthProvider for
username/password authentication.
"""

from __future__ import annotations

import hmac
import secrets
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class User:
    """Authenticated user information."""

    username: str
    permissions: set[str] = field(default_factory=set)
    metadata: dict[str, Any] = field(default_factory=dict)


class AuthProvider(ABC):
    """Base class for authentication providers."""

    @abstractmethod
    async def authenticate(self, credentials: dict[str, Any]) -> User | None:
        """
        Authenticate with the given credentials.

        Args:
            credentials: Dict with provider-specific keys (e.g. username, password)

        Returns:
            User if authenticated, None otherwise
        """
        ...

    async def get_user(self, token: str) -> User | None:
        """
        Look up a user by session token.

        Override this for token-based auth flows.
        """
        return None


class SimpleAuthProvider(AuthProvider):
    """
    Simple username/password authentication.

    Users are defined as a dict of username -> {"password": "...", "permissions": [...]}.
    """

    def __init__(self, users: dict[str, dict[str, Any]]) -> None:
        self._users = users
        self._tokens: dict[str, User] = {}

    async def authenticate(self, credentials: dict[str, Any]) -> User | None:
        username = credentials.get("username", "")
        password = credentials.get("password", "")

        user_data = self._users.get(username)
        if not user_data:
            return None

        expected = user_data.get("password", "")
        if not hmac.compare_digest(password, expected):
            return None

        permissions = set(user_data.get("permissions", []))
        user = User(username=username, permissions=permissions)

        # Generate a session token
        token = secrets.token_urlsafe(32)
        self._tokens[token] = user

        return user

    async def get_user(self, token: str) -> User | None:
        return self._tokens.get(token)

    def create_token(self, user: User) -> str:
        """Create a token for an authenticated user."""
        token = secrets.token_urlsafe(32)
        self._tokens[token] = user
        return token


# Global auth provider
_auth_provider: AuthProvider | None = None
_public_events: set[str] = set()


def set_auth_provider(provider: AuthProvider, public_events: set[str] | None = None) -> None:
    """Set the global auth provider."""
    global _auth_provider, _public_events
    _auth_provider = provider
    _public_events = public_events or set()


def get_auth_provider() -> AuthProvider | None:
    """Get the global auth provider."""
    return _auth_provider


def get_public_events() -> set[str]:
    """Get events that don't require authentication."""
    return _public_events
