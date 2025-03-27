"""
Logging mixin to record activity, such as state changes and user interactions.
"""

from datetime import datetime

class LoggingMixin:
    """
    A mixin that provides basic logging functionality
    for tracking component or application events.
    """

    def log_event(self, message: str) -> None:
        """
        Logs a timestamped event message.
        """
        now = datetime.utcnow().isoformat()
        print(f"[{now}] [CacaoLog] {message}")
