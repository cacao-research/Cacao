"""
Logging mixin to record activity, such as state changes and user interactions.
"""

from datetime import datetime
import colorama
import sys
import os

# Check if we should use ASCII mode (Windows or explicit setting)
def _should_use_ascii():
    """Determine if ASCII mode should be used."""
    # Check environment variable
    if os.environ.get("CACAO_ASCII_MODE", "").lower() in ("1", "true", "yes"):
        return True
    # Check if running on Windows with non-UTF8 console
    if sys.platform == "win32":
        try:
            # Test if console can handle unicode
            sys.stdout.write("\u2713")
            sys.stdout.write("\b \b")  # Erase it
            return False
        except (UnicodeEncodeError, UnicodeDecodeError):
            return True
    return False

ASCII_DEBUG_MODE = _should_use_ascii()

# Initialize colorama for Windows support
colorama.init()

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class LoggingMixin:
    """
    A mixin that provides logging functionality for tracking
    component or application events with different log levels and formatting.
    """

    def log_event(self, message: str) -> None:
        """
        Logs a timestamped event message.
        
        Args:
            message: The message to log.
        """
        now = datetime.utcnow().isoformat()
        print(f"[{now}] [CacaoLog] {message}")

    def log(self, message: str, level: str = "info", emoji: str = "") -> None:
        """
        Logs a formatted message with timestamp, color, and emoji.
        
        Args:
            message: The message to log.
            level: Log level (debug, info, warning, error).
            emoji: Optional emoji to prefix the message.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = {
            "debug": Colors.BLUE,
            "info": Colors.GREEN,
            "warning": Colors.YELLOW,
            "error": Colors.RED
        }.get(level, Colors.ENDC)
        
        # Set the display emoji
        display_emoji = ""
        if emoji:
            if ASCII_DEBUG_MODE:
                # When ASCII debug mode is ON, replace emojis with ASCII alternatives
                emoji_replacements = {
                    "🍫": "C", "🌎": "W", "🔌": "*", "📡": "*", "👀": "*", 
                    "🔄": "*", "🌟": "*", "📂": "*", "🎯": "*", "🕒": "*",
                    "🔢": "*", "⚠️": "!", "❌": "X", "💥": "!", "👋": "*",
                    "📢": "*", "🔥": "*", "❓": "?", "⏰": "*", "🔁": "*",
                }
                
                # If emoji isn't in our mapping, default to "*"
                display_emoji = emoji_replacements.get(emoji, "*")
            else:
                # When ASCII debug mode is OFF, use the actual emoji
                display_emoji = emoji
                
        formatted_message = f"{color}{timestamp} {display_emoji}  {message}{Colors.ENDC}"
        try:
            print(formatted_message)
        except UnicodeEncodeError:
            # Fallback to ASCII-safe message
            safe_message = formatted_message.encode('ascii', 'replace').decode('ascii')
            print(safe_message)