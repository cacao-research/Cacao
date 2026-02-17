"""
Unified logging for Cacao.

Provides a single, clean log format across all output — both Cacao's own
messages and uvicorn's access / lifecycle logs.

Format:  ``  HH:MM:SS  label   message``

Normal mode shows INFO+ only.  ``--verbose`` lowers the level to DEBUG so
that ws/event details appear.
"""

from __future__ import annotations

import logging
from datetime import datetime

# ANSI helpers (same palette as cli/commands.py)
BROWN = "\033[38;5;130m"
DIM = "\033[2m"
RESET = "\033[0m"

# Label column width (padded with spaces)
_LABEL_WIDTH = 8


# ---------------------------------------------------------------------------
# Filters
# ---------------------------------------------------------------------------

class UvicornStartupFilter(logging.Filter):
    """Suppress uvicorn lifecycle messages that the banner already covers."""

    _SUPPRESSED_PREFIXES = (
        "Started server process",
        "Waiting for application startup",
        "Uvicorn running on",
        "Application startup complete",
    )

    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        return not any(msg.startswith(p) for p in self._SUPPRESSED_PREFIXES)


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------

class CacaoFormatter(logging.Formatter):
    """Format general logs as ``  HH:MM:SS  label   message``."""

    def format(self, record: logging.LogRecord) -> str:
        ts = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
        label: str = getattr(record, "label", "log")
        msg = record.getMessage()

        # If an exception is attached, append it
        if record.exc_info and record.exc_info[0] is not None:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
            if record.exc_text:
                msg = f"{msg}\n{record.exc_text}"

        return f"  {DIM}{ts}{RESET}  {BROWN}{label:<{_LABEL_WIDTH}}{RESET}{msg}"


class CacaoAccessFormatter(logging.Formatter):
    """Format uvicorn access logs as ``  HH:MM:SS  GET     /path 200``.

    Uvicorn passes access-log args as a tuple:
      ``(client_addr, method, full_path, http_version, status_code)``
    """

    def format(self, record: logging.LogRecord) -> str:
        ts = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")

        # Uvicorn access log args: (client, method, path, http_ver, status)
        if record.args and isinstance(record.args, tuple) and len(record.args) >= 5:
            _client, method, path, _http_ver, status = record.args[:5]
            return (
                f"  {DIM}{ts}{RESET}  "
                f"{BROWN}{method:<{_LABEL_WIDTH}}{RESET}"
                f"{path} {status}"
            )

        # Fallback for unexpected format
        msg = record.getMessage()
        return f"  {DIM}{ts}{RESET}  {BROWN}{'http':<{_LABEL_WIDTH}}{RESET}{msg}"


# ---------------------------------------------------------------------------
# Log config for uvicorn
# ---------------------------------------------------------------------------

def get_uvicorn_log_config(debug: bool = False) -> dict:
    """Return a ``logging.config.dictConfig`` dict for ``uvicorn.run(log_config=...)``.

    Wires both :class:`CacaoFormatter` and :class:`CacaoAccessFormatter`,
    applies :class:`UvicornStartupFilter`, and sets the cacao logger to
    DEBUG when *debug* is True.
    """
    cacao_level = "DEBUG" if debug else "INFO"

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "startup_filter": {
                "()": "cacao.server.log.UvicornStartupFilter",
            },
        },
        "formatters": {
            "cacao": {
                "()": "cacao.server.log.CacaoFormatter",
            },
            "access": {
                "()": "cacao.server.log.CacaoAccessFormatter",
            },
        },
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "formatter": "cacao",
                "stream": "ext://sys.stderr",
                "filters": ["startup_filter"],
            },
            "access": {
                "class": "logging.StreamHandler",
                "formatter": "access",
                "stream": "ext://sys.stderr",
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["access"],
                "level": "INFO",
                "propagate": False,
            },
            "cacao": {
                "handlers": ["default"],
                "level": cacao_level,
                "propagate": False,
            },
        },
    }


# ---------------------------------------------------------------------------
# Public helper
# ---------------------------------------------------------------------------

def _ensure_cacao_handler() -> None:
    """Attach a default handler to the ``cacao`` root logger if none exists.

    This allows ``logger.info(...)`` calls that happen *before*
    ``uvicorn.run()`` applies the dictConfig to still produce output
    in the unified format.
    """
    root = logging.getLogger("cacao")
    if not root.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(CacaoFormatter())
        root.addHandler(handler)
        root.setLevel(logging.INFO)


def get_logger(name: str = "cacao") -> logging.Logger:
    """Return a logger under the ``cacao`` namespace."""
    _ensure_cacao_handler()
    return logging.getLogger(name)
