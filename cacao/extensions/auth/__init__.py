"""
Authentication module for the Cacao framework.
Provides basic authentication functionalities.
"""

from typing import Optional

class Authenticator:
    """
    Basic authenticator for handling user authentication.
    """
    def __init__(self):
        self._users = {"admin": "password"}  # Placeholder user store

    def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticates a user given a username and password.
        """
        return self._users.get(username) == password

    def add_user(self, username: str, password: str) -> None:
        """
        Adds a new user to the authentication store.
        """
        self._users[username] = password

authenticator = Authenticator()
