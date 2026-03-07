"""
Friendly error handling for Cacao.

Provides user-friendly error messages with suggestions instead of raw
tracebacks. Also includes "did you mean?" matching for typos in component
names and props.
"""

from __future__ import annotations

import difflib
import traceback
from typing import Any

# All public component/function names exposed by the simple API
_SIMPLE_API_NAMES: list[str] = [
    # Layout
    "row",
    "col",
    "grid",
    "container",
    "stack",
    "split",
    "hero",
    "card",
    "sidebar",
    "tabs",
    "tab",
    "app_shell",
    "nav_sidebar",
    "nav_group",
    "nav_item",
    "shell_content",
    "nav_panel",
    "panel",
    # Typography
    "title",
    "text",
    "html",
    "raw_html",
    "markdown",
    "code",
    "divider",
    "spacer",
    # Display
    "metric",
    "table",
    "json_view",
    "json",
    "progress",
    "badge",
    "alert",
    "accordion",
    "accordion_item",
    "steps",
    "step",
    "file_tree",
    "subnav",
    "subnav_group",
    "subnav_item",
    "link_card",
    "modal",
    "tooltip",
    "breadcrumb",
    "image",
    "timeline",
    "timeline_item",
    "video",
    "diff",
    "search_input",
    "anchor",
    # Form
    "button",
    "input",
    "input_field",
    "textarea",
    "select",
    "checkbox",
    "switch",
    "slider",
    "date",
    "date_picker",
    "chat",
    "upload",
    "file_upload",
    # Charts
    "line",
    "bar",
    "pie",
    "area",
    "scatter",
    "gauge",
    # Interface
    "interface",
    "parallel",
    "series",
    "compare",
    # AI / Agent
    "extract",
    "cost_dashboard",
    "document_upload",
    "model_picker",
    "agent",
    "multi_agent",
    "tool_timeline",
    "budget_gauge",
    "skill",
    "skill_browser",
    "chain_builder",
    "safety_policy",
    # State
    "signal",
    "computed",
    "on",
    "bind",
    "use",
    # App
    "config",
    "page",
    "layout",
    "run",
    "stream",
    "chat",
    # Data
    "load_csv",
    "load_json",
    # Notifications
    "notify",
    "emit",
    "listen",
    # Auth
    "require_auth",
    "permission",
    # Themes
    "register_theme",
]


def did_you_mean(
    name: str, candidates: list[str] | None = None, n: int = 3, cutoff: float = 0.6
) -> list[str]:
    """Find close matches for a name from a list of candidates.

    Args:
        name: The misspelled name
        candidates: List of valid names (defaults to simple API names)
        n: Maximum number of suggestions
        cutoff: Similarity threshold (0-1)

    Returns:
        List of close matches, best first
    """
    if candidates is None:
        candidates = _SIMPLE_API_NAMES
    return difflib.get_close_matches(name, candidates, n=n, cutoff=cutoff)


def format_friendly_error(exc: BaseException, *, context: str = "") -> dict[str, Any]:
    """Format an exception into a friendly error dict for the frontend.

    Args:
        exc: The exception to format
        context: Additional context (e.g., "handling event 'increment'")

    Returns:
        Dict with keys: type, title, message, suggestion, traceback
    """
    exc_type = type(exc).__name__
    exc_msg = str(exc)
    tb = traceback.format_exc()

    title, message, suggestion = _classify_error(exc, exc_type, exc_msg, context)

    return {
        "type": exc_type,
        "title": title,
        "message": message,
        "suggestion": suggestion,
        "traceback": tb,
        "context": context,
    }


def _classify_error(
    exc: BaseException, exc_type: str, exc_msg: str, context: str
) -> tuple[str, str, str]:
    """Classify an error and return (title, message, suggestion)."""

    # --- AttributeError: likely typo in c.xxx() ---
    if isinstance(exc, AttributeError):
        # Extract the attribute name from "module 'cacao' has no attribute 'xxx'"
        attr = _extract_attr_name(exc_msg)
        if attr:
            matches = did_you_mean(attr)
            if matches:
                suggestion = f"Did you mean: {', '.join(f'c.{m}()' for m in matches)}?"
            else:
                suggestion = "Check the docs for available components: https://github.com/cacao-research/Cacao"
            return (
                f"Unknown component: c.{attr}()",
                exc_msg,
                suggestion,
            )
        return ("Attribute Error", exc_msg, "")

    # --- TypeError: wrong arguments ---
    if isinstance(exc, TypeError):
        if "argument" in exc_msg or "parameter" in exc_msg:
            return (
                "Wrong Arguments",
                exc_msg,
                "Check the function signature — you may have extra or missing parameters.",
            )
        return ("Type Error", exc_msg, "")

    # --- ValueError ---
    if isinstance(exc, ValueError):
        return ("Invalid Value", exc_msg, "")

    # --- ImportError ---
    if isinstance(exc, ImportError):
        module = _extract_module_name(exc_msg)
        suggestion = f"Install it with: pip install {module}" if module else ""
        return ("Missing Dependency", exc_msg, suggestion)

    # --- KeyError ---
    if isinstance(exc, KeyError):
        return (
            "Key Not Found",
            f"Key {exc_msg} does not exist",
            "Check that the key name is spelled correctly.",
        )

    # --- ConnectionError / WebSocket issues ---
    if isinstance(exc, (ConnectionError, OSError)):
        return (
            "Connection Error",
            exc_msg,
            "Check that the server is running and the port is not in use.",
        )

    # --- Generic fallback ---
    return (
        exc_type,
        exc_msg,
        f"An error occurred while {context}." if context else "",
    )


def _extract_attr_name(msg: str) -> str | None:
    """Extract attribute name from AttributeError message."""
    # "module 'cacao' has no attribute 'titl'"
    if "has no attribute" in msg:
        parts = msg.split("'")
        if len(parts) >= 4:
            return parts[-2]
    return None


def _extract_module_name(msg: str) -> str | None:
    """Extract module name from ImportError message."""
    # "No module named 'foo'"
    if "No module named" in msg:
        parts = msg.split("'")
        if len(parts) >= 2:
            return parts[1]
    return None
