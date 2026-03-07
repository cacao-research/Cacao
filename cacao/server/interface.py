"""
Interface component for Cacao — wraps any Python function into a full UI.

Inspects function signatures (type hints, defaults, docstrings) to auto-generate
input/output components. Supports sync/async execution, progress callbacks,
generator streaming, caching, examples, and flagging.

Example:
    import cacao as c

    def greet(name: str, excited: bool = False) -> str:
        greeting = f"Hello, {name}!"
        return greeting.upper() if excited else greeting

    c.interface(greet)
"""

from __future__ import annotations

import asyncio
import inspect
import re
import traceback
import uuid
from collections.abc import Callable
from typing import (
    Any,
    Literal,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from .session import Session
from .signal import Signal
from .ui import Component, _add_to_current_container, _container_context


# =============================================================================
# I/O Marker Types (lightweight, for type hints only)
# =============================================================================


class IOType:
    """Base class for Cacao I/O marker types used in function signatures."""

    pass


class Image(IOType):
    """Marker type for image data in function signatures."""

    pass


class Audio(IOType):
    """Marker type for audio data in function signatures."""

    pass


class Video(IOType):
    """Marker type for video data in function signatures."""

    pass


class Code(IOType):
    """Marker type for code/source text in function signatures."""

    pass


class Markdown(IOType):
    """Marker type for markdown content in function signatures."""

    pass


class Plot(IOType):
    """Marker type for chart/plot objects in function signatures."""

    pass


class File(IOType):
    """Marker type for file data in function signatures."""

    pass


class DataFrame(IOType):
    """Marker type for DataFrame data in function signatures."""

    pass


# =============================================================================
# Type Introspection Engine
# =============================================================================


def _inspect_function(fn: Callable[..., Any]) -> dict[str, Any]:
    """Extract parameters, types, defaults, and return type from a function."""
    sig = inspect.signature(fn)

    try:
        hints = get_type_hints(fn, include_extras=True)
    except Exception:
        hints = {}

    params: list[dict[str, Any]] = []
    has_progress = False

    for name, param in sig.parameters.items():
        # Skip 'progress' parameter — it's injected by the execution engine
        if name == "progress":
            has_progress = True
            continue

        type_hint = hints.get(name, str)
        default = param.default if param.default is not inspect.Parameter.empty else None
        has_default = param.default is not inspect.Parameter.empty

        params.append(
            {
                "name": name,
                "type": type_hint,
                "default": default,
                "has_default": has_default,
            }
        )

    return_type = hints.get("return", str)

    return {
        "params": params,
        "return_type": return_type,
        "has_progress": has_progress,
        "is_generator": inspect.isgeneratorfunction(fn),
        "is_async_generator": inspect.isasyncgenfunction(fn),
        "is_async": inspect.iscoroutinefunction(fn),
    }


def _parse_docstring(fn: Callable[..., Any]) -> dict[str, str]:
    """Parse Google-style docstring for Args: descriptions."""
    doc = inspect.getdoc(fn)
    if not doc:
        return {}

    descriptions: dict[str, str] = {}
    in_args = False

    for line in doc.split("\n"):
        stripped = line.strip()

        if stripped.lower().startswith("args:"):
            in_args = True
            continue

        if in_args:
            # End of Args section
            if stripped and not stripped.startswith(" ") and ":" not in stripped[:20]:
                if stripped.lower().startswith(("returns:", "raises:", "example:", "note:")):
                    break

            # Parse "param_name: description" or "param_name (type): description"
            match = re.match(r"(\w+)(?:\s*\([^)]*\))?\s*:\s*(.+)", stripped)
            if match:
                descriptions[match.group(1)] = match.group(2).strip()

    return descriptions


def _type_to_input(
    type_hint: Any, param_name: str, default: Any, description: str
) -> dict[str, Any]:
    """Map a type hint to an input component spec."""
    origin = get_origin(type_hint)
    args = get_args(type_hint)

    label = param_name.replace("_", " ").title()

    # Handle Annotated[T, component_override]
    if origin is not None and _is_annotated(type_hint):
        # Annotated — the second arg might be a component spec override
        actual_type = args[0] if args else str
        if len(args) > 1 and isinstance(args[1], dict):
            spec = {"label": label, "description": description, **args[1]}
            if default is not None:
                spec.setdefault("default", default)
            return spec
        return _type_to_input(actual_type, param_name, default, description)

    # Literal["a", "b"] → select
    if origin is Literal:
        return {
            "component": "Select",
            "label": label,
            "description": description,
            "options": list(args),
            "default": default if default is not None else (args[0] if args else None),
        }

    # Optional[T] → unwrap to T with nullable flag
    if origin is Union:
        non_none = [a for a in args if a is not type(None)]
        if len(non_none) == 1:
            spec = _type_to_input(non_none[0], param_name, default, description)
            spec["optional"] = True
            return spec

    # list[str] → textarea
    if origin is list:
        return {
            "component": "Textarea",
            "label": label,
            "description": description,
            "placeholder": "One item per line",
            "default": default,
        }

    # Core Python types
    if type_hint is bool:
        return {
            "component": "Checkbox",
            "label": label,
            "description": description,
            "default": default if default is not None else False,
        }

    if type_hint is int:
        return {
            "component": "Input",
            "label": label,
            "description": description,
            "type": "number",
            "default": default,
        }

    if type_hint is float:
        return {
            "component": "Slider",
            "label": label,
            "description": description,
            "min": 0,
            "max": 1,
            "step": 0.01,
            "default": default if default is not None else 0.5,
        }

    if type_hint is bytes or type_hint is File:
        return {
            "component": "FileUpload",
            "label": label,
            "description": description,
        }

    if type_hint is Image:
        return {
            "component": "FileUpload",
            "label": label,
            "description": description,
            "accept": "image/*",
        }

    if type_hint is Audio:
        return {
            "component": "FileUpload",
            "label": label,
            "description": description,
            "accept": "audio/*",
        }

    if type_hint is Video:
        return {
            "component": "FileUpload",
            "label": label,
            "description": description,
            "accept": "video/*",
        }

    if type_hint is Code:
        return {
            "component": "Textarea",
            "label": label,
            "description": description,
            "monospace": True,
            "default": default,
        }

    if type_hint is DataFrame:
        return {
            "component": "EditableTable",
            "label": label,
            "description": description,
        }

    # Default: text input
    return {
        "component": "Input",
        "label": label,
        "description": description,
        "type": "text",
        "default": str(default) if default is not None else "",
    }


def _type_to_output(type_hint: Any) -> str:
    """Map a return type to an output display mode."""
    origin = get_origin(type_hint)
    args = get_args(type_hint)

    if type_hint is bool:
        return "badge"
    if type_hint in (int, float):
        return "metric"
    if type_hint is dict:
        return "json"
    if type_hint is Markdown:
        return "markdown"
    if type_hint is Code:
        return "code"
    if type_hint is Image:
        return "image"
    if type_hint is Audio:
        return "audio"
    if type_hint is Video:
        return "video"
    if type_hint is Plot:
        return "chart"
    if type_hint is File or type_hint is bytes:
        return "file"
    if type_hint is DataFrame:
        return "table"

    # list[dict] → table, list → json
    if type_hint is list or origin is list:
        if args and args[0] is dict:
            return "table"
        return "json"

    # Default: text
    return "text"


def _is_annotated(type_hint: Any) -> bool:
    """Check if a type hint is typing.Annotated."""
    try:
        from typing import Annotated

        return get_origin(type_hint) is Annotated
    except ImportError:
        return False


def _fn_title(fn: Callable[..., Any]) -> str:
    """Derive a human-readable title from function name."""
    name = fn.__name__
    # snake_case → Title Case
    return name.replace("_", " ").title()


def _fn_description(fn: Callable[..., Any]) -> str:
    """Extract first line of docstring as description."""
    doc = inspect.getdoc(fn)
    if not doc:
        return ""
    return doc.split("\n")[0].strip()


# =============================================================================
# Interface Component
# =============================================================================

# Global counter for unique interface IDs
_interface_counter = 0


def interface(
    fn: Callable[..., Any],
    *,
    title: str | None = None,
    description: str | None = None,
    submit_label: str = "Submit",
    layout: Literal["auto", "horizontal", "vertical"] = "auto",
    examples: list[list[Any]] | None = None,
    cache: bool = False,
    flagging: bool = False,
    flagging_dir: str = "./flags/",
    live: bool = False,
    timeout: float = 60.0,
) -> Component:
    """
    Wrap a Python function into a full interactive UI component.

    Inspects the function's type hints, defaults, and docstring to auto-generate
    input fields and output displays. Fully composable — works inside c.row(),
    c.card(), etc.

    Args:
        fn: The function to wrap
        title: Display title (default: derived from function name)
        description: Description text (default: from docstring)
        submit_label: Text for the submit button
        layout: Layout mode — "auto" (responsive), "horizontal", or "vertical"
        examples: List of example input lists (clickable presets)
        cache: Enable LRU caching of results per session
        flagging: Enable flagging button for collecting feedback
        flagging_dir: Directory for flagged data (when flagging=True)
        live: Auto-submit on input change (debounced)
        timeout: Max execution time in seconds

    Returns:
        The Interface component

    Example:
        def greet(name: str, excited: bool = False) -> str:
            greeting = f"Hello, {name}!"
            return greeting.upper() if excited else greeting

        c.interface(greet)
    """
    global _interface_counter
    _interface_counter += 1
    iface_id = f"iface_{_interface_counter}"

    # Introspect function
    info = _inspect_function(fn)
    docstring_descriptions = _parse_docstring(fn)

    # Build input specs
    inputs: list[dict[str, Any]] = []
    for param in info["params"]:
        desc = docstring_descriptions.get(param["name"], "")
        spec = _type_to_input(param["type"], param["name"], param["default"], desc)
        spec["param_name"] = param["name"]
        spec["has_default"] = param["has_default"]
        inputs.append(spec)

    # Build output spec
    output_mode = _type_to_output(info["return_type"])

    # Determine execution mode
    if info["is_generator"] or info["is_async_generator"]:
        exec_mode = "stream"
    elif info["has_progress"]:
        exec_mode = "progress"
    else:
        exec_mode = "simple"

    # Derive metadata
    iface_title = title or _fn_title(fn)
    iface_description = description or _fn_description(fn)

    # Register the event handler for this interface
    _register_interface_handler(iface_id, fn, info, cache, timeout)

    # Build example param names for the frontend
    param_names = [p["name"] for p in info["params"]]

    return _add_to_current_container(
        Component(
            type="Interface",
            props={
                "id": iface_id,
                "title": iface_title,
                "description": iface_description,
                "submit_label": submit_label,
                "layout": layout,
                "inputs": inputs,
                "output_mode": output_mode,
                "exec_mode": exec_mode,
                "examples": examples,
                "param_names": param_names,
                "live": live,
                "flagging": flagging,
                "flagging_dir": flagging_dir,
            },
        )
    )


# =============================================================================
# Execution Engine
# =============================================================================

# Per-session caches: { session_id: { iface_id: { input_hash: output } } }
_cache_store: dict[str, dict[str, dict[str, Any]]] = {}


def _register_interface_handler(
    iface_id: str,
    fn: Callable[..., Any],
    info: dict[str, Any],
    cache: bool,
    timeout: float,
) -> None:
    """Register the server-side event handler for an interface."""
    from .app import App

    # We need to lazily register on the app. The event system is global.
    # The handler will be registered when the first event arrives (or we can
    # hook into the simple API's _get_app flow).
    # For now, store it globally and register lazily.
    _pending_handlers[iface_id] = {
        "fn": fn,
        "info": info,
        "cache": cache,
        "timeout": timeout,
    }


# Pending handlers waiting to be registered on the app
_pending_handlers: dict[str, dict[str, Any]] = {}


async def handle_interface_event(
    session: Session, iface_id: str, input_values: dict[str, Any]
) -> None:
    """Execute an interface function and send results back to the client."""
    handler_info = _pending_handlers.get(iface_id)
    if not handler_info:
        await session.send(
            {
                "type": "interface:error",
                "id": iface_id,
                "error": "NotFound",
                "message": f"Interface '{iface_id}' not found",
                "traceback": "",
            }
        )
        return

    fn = handler_info["fn"]
    info = handler_info["info"]
    use_cache = handler_info["cache"]
    timeout = handler_info["timeout"]

    # Check cache
    if use_cache:
        cache_key = str(sorted(input_values.items()))
        session_cache = _cache_store.setdefault(session.id, {})
        iface_cache = session_cache.setdefault(iface_id, {})
        if cache_key in iface_cache:
            await session.send(
                {
                    "type": "interface:result",
                    "id": iface_id,
                    "output": iface_cache[cache_key],
                    "cached": True,
                }
            )
            return

    # Convert input values to proper types
    kwargs = _coerce_inputs(input_values, info["params"])

    # Execute based on mode
    try:
        if info["is_generator"]:
            await _execute_streaming(session, iface_id, fn, kwargs, timeout)
        elif info["is_async_generator"]:
            await _execute_async_streaming(session, iface_id, fn, kwargs, timeout)
        elif info["has_progress"]:
            await _execute_with_progress(session, iface_id, fn, kwargs, timeout)
        elif info["is_async"]:
            result = await asyncio.wait_for(fn(**kwargs), timeout=timeout)
            output = _serialize_output(result)
            await session.send(
                {"type": "interface:result", "id": iface_id, "output": output}
            )
        else:
            # Run sync function in thread pool
            result = await asyncio.wait_for(
                asyncio.to_thread(fn, **kwargs), timeout=timeout
            )
            output = _serialize_output(result)
            await session.send(
                {"type": "interface:result", "id": iface_id, "output": output}
            )

        # Cache result
        if use_cache and not info["is_generator"] and not info["is_async_generator"]:
            cache_key = str(sorted(input_values.items()))
            session_cache = _cache_store.setdefault(session.id, {})
            iface_cache = session_cache.setdefault(iface_id, {})
            iface_cache[cache_key] = output  # type: ignore[possibly-undefined]

    except asyncio.TimeoutError:
        await session.send(
            {
                "type": "interface:error",
                "id": iface_id,
                "error": "TimeoutError",
                "message": f"Function timed out after {timeout}s",
                "traceback": "",
            }
        )
    except Exception as e:
        tb = traceback.format_exc()
        await session.send(
            {
                "type": "interface:error",
                "id": iface_id,
                "error": type(e).__name__,
                "message": str(e),
                "traceback": tb,
            }
        )


async def _execute_streaming(
    session: Session,
    iface_id: str,
    fn: Callable[..., Any],
    kwargs: dict[str, Any],
    timeout: float,
) -> None:
    """Execute a sync generator function and stream tokens to client."""
    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[str | None] = asyncio.Queue()

    def _run_generator() -> None:
        try:
            for token in fn(**kwargs):
                asyncio.run_coroutine_threadsafe(queue.put(str(token)), loop).result()
        finally:
            asyncio.run_coroutine_threadsafe(queue.put(None), loop).result()

    # Run generator in thread, stream tokens as they arrive
    thread_future = loop.run_in_executor(None, _run_generator)

    async def _stream() -> None:
        while True:
            token = await queue.get()
            if token is None:
                break
            await session.send(
                {"type": "interface:stream", "id": iface_id, "token": token}
            )
        await session.send({"type": "interface:stream_done", "id": iface_id})

    await asyncio.wait_for(_stream(), timeout=timeout)
    await thread_future  # Ensure thread cleanup


async def _execute_async_streaming(
    session: Session,
    iface_id: str,
    fn: Callable[..., Any],
    kwargs: dict[str, Any],
    timeout: float,
) -> None:
    """Execute an async generator function and stream tokens to client."""

    async def _run() -> None:
        async for token in fn(**kwargs):
            await session.send(
                {
                    "type": "interface:stream",
                    "id": iface_id,
                    "token": str(token),
                }
            )
        await session.send(
            {"type": "interface:stream_done", "id": iface_id}
        )

    await asyncio.wait_for(_run(), timeout=timeout)


async def _execute_with_progress(
    session: Session,
    iface_id: str,
    fn: Callable[..., Any],
    kwargs: dict[str, Any],
    timeout: float,
) -> None:
    """Execute a function with progress callback."""
    loop = asyncio.get_running_loop()

    async def progress_callback(value: float) -> None:
        await session.send(
            {
                "type": "interface:progress",
                "id": iface_id,
                "value": max(0.0, min(1.0, float(value))),
            }
        )

    def sync_progress(value: float) -> None:
        """Sync wrapper that schedules the async send on the event loop."""
        asyncio.run_coroutine_threadsafe(progress_callback(value), loop)

    kwargs["progress"] = sync_progress

    if inspect.iscoroutinefunction(fn):
        # For async functions with progress, pass the async callback directly
        kwargs["progress"] = progress_callback
        result = await asyncio.wait_for(fn(**kwargs), timeout=timeout)
    else:
        result = await asyncio.wait_for(
            asyncio.to_thread(fn, **kwargs), timeout=timeout
        )

    output = _serialize_output(result)
    await session.send(
        {"type": "interface:result", "id": iface_id, "output": output}
    )


def _coerce_inputs(
    values: dict[str, Any], params: list[dict[str, Any]]
) -> dict[str, Any]:
    """Coerce string input values to their expected types."""
    result: dict[str, Any] = {}
    param_map = {p["name"]: p for p in params}

    for name, value in values.items():
        param = param_map.get(name)
        if not param:
            continue

        type_hint = param["type"]

        try:
            if type_hint is int:
                result[name] = int(value) if value != "" else 0
            elif type_hint is float:
                result[name] = float(value) if value != "" else 0.0
            elif type_hint is bool:
                result[name] = bool(value)
            elif get_origin(type_hint) is list:
                # Textarea → split by lines
                if isinstance(value, str):
                    result[name] = [line.strip() for line in value.split("\n") if line.strip()]
                else:
                    result[name] = value
            else:
                result[name] = value
        except (ValueError, TypeError):
            result[name] = value

    return result


def _serialize_output(result: Any) -> Any:
    """Serialize a function result for sending to the client."""
    if result is None:
        return {"type": "text", "value": "None"}

    # PIL Image → base64 PNG
    try:
        import PIL.Image
        if isinstance(result, PIL.Image.Image):
            import base64
            import io
            buf = io.BytesIO()
            fmt = "PNG" if result.mode == "RGBA" else "JPEG"
            result.save(buf, format=fmt)
            b64 = base64.b64encode(buf.getvalue()).decode("ascii")
            mime = "image/png" if fmt == "PNG" else "image/jpeg"
            return {"type": "image", "value": f"data:{mime};base64,{b64}"}
    except ImportError:
        pass

    # Matplotlib figure → base64 PNG
    try:
        import matplotlib.figure
        if isinstance(result, matplotlib.figure.Figure):
            import base64
            import io
            buf = io.BytesIO()
            result.savefig(buf, format="png", bbox_inches="tight", dpi=150)
            buf.seek(0)
            b64 = base64.b64encode(buf.getvalue()).decode("ascii")
            import matplotlib.pyplot as plt
            plt.close(result)
            return {"type": "image", "value": f"data:image/png;base64,{b64}"}
    except ImportError:
        pass

    # Plotly figure → JSON
    try:
        import plotly.graph_objects
        if isinstance(result, plotly.graph_objects.Figure):
            return {"type": "plotly", "value": result.to_json()}
    except ImportError:
        pass

    # Pandas DataFrame → table
    try:
        import pandas
        if isinstance(result, pandas.DataFrame):
            records = result.head(500).to_dict("records")
            return {"type": "table", "value": records}
    except ImportError:
        pass

    # Polars DataFrame → table
    try:
        import polars
        if isinstance(result, polars.DataFrame):
            records = result.head(500).to_dicts()
            return {"type": "table", "value": records}
    except ImportError:
        pass

    # bytes → file download (base64)
    if isinstance(result, bytes):
        import base64
        b64 = base64.b64encode(result).decode("ascii")
        return {"type": "file", "value": f"data:application/octet-stream;base64,{b64}"}

    # tuple → multiple outputs
    if isinstance(result, tuple):
        return {"type": "multi", "value": [_serialize_output(item) for item in result]}

    if isinstance(result, bool):
        return {"type": "badge", "value": "Yes" if result else "No"}

    if isinstance(result, (int, float)):
        return {"type": "metric", "value": result}

    if isinstance(result, dict):
        return {"type": "json", "value": result}

    if isinstance(result, list):
        if result and isinstance(result[0], dict):
            return {"type": "table", "value": result}
        return {"type": "json", "value": result}

    if isinstance(result, str):
        # Check if it looks like a data URL (image/audio/video)
        if result.startswith("data:image/"):
            return {"type": "image", "value": result}
        if result.startswith("data:audio/"):
            return {"type": "audio", "value": result}
        if result.startswith("data:video/"):
            return {"type": "video", "value": result}
        return {"type": "text", "value": result}

    # Fallback: convert to string
    return {"type": "text", "value": str(result)}


# =============================================================================
# Flagging
# =============================================================================


async def handle_interface_flag(
    session: Session,
    iface_id: str,
    input_values: dict[str, Any],
    output_value: Any,
    note: str = "",
) -> None:
    """Save flagged input/output to CSV."""
    import csv
    import os
    from datetime import datetime

    handler_info = _pending_handlers.get(iface_id)
    if not handler_info:
        return

    flagging_dir = "./flags/"
    os.makedirs(flagging_dir, exist_ok=True)
    filepath = os.path.join(flagging_dir, f"{iface_id}.csv")

    file_exists = os.path.exists(filepath)
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "inputs", "output", "note"])
        writer.writerow(
            [
                datetime.now().isoformat(),
                str(input_values),
                str(output_value),
                note,
            ]
        )

    await session.send(
        {
            "type": "interface:flagged",
            "id": iface_id,
        }
    )


# =============================================================================
# Composable Interfaces
# =============================================================================


def parallel(
    *fns: Callable[..., Any],
    titles: list[str] | None = None,
    **kwargs: Any,
) -> Component:
    """Run multiple functions side-by-side in a row layout."""
    with _container_context(Component(type="Row", props={"gap": 4, "align": "stretch"})) as container:
        for i, fn in enumerate(fns):
            title = titles[i] if titles and i < len(titles) else None
            interface(fn, title=title, **kwargs)

    return _add_to_current_container(container)


def series(
    *fns: Callable[..., Any],
    titles: list[str] | None = None,
    **kwargs: Any,
) -> Component:
    """Chain functions — output of each feeds into the next."""
    global _interface_counter

    interfaces = []
    for i, fn in enumerate(fns):
        _interface_counter += 1
        iface_id = f"iface_{_interface_counter}"

        info = _inspect_function(fn)
        docstring_descriptions = _parse_docstring(fn)

        inputs = []
        for param in info["params"]:
            desc = docstring_descriptions.get(param["name"], "")
            spec = _type_to_input(param["type"], param["name"], param["default"], desc)
            spec["param_name"] = param["name"]
            spec["has_default"] = param["has_default"]
            inputs.append(spec)

        output_mode = _type_to_output(info["return_type"])
        exec_mode = "stream" if (info["is_generator"] or info["is_async_generator"]) else ("progress" if info["has_progress"] else "simple")

        title = titles[i] if titles and i < len(titles) else _fn_title(fn)

        _register_interface_handler(iface_id, fn, info, kwargs.get("cache", False), kwargs.get("timeout", 60.0))

        interfaces.append({
            "id": iface_id,
            "title": title,
            "description": _fn_description(fn),
            "inputs": inputs,
            "output_mode": output_mode,
            "exec_mode": exec_mode,
            "param_names": [p["name"] for p in info["params"]],
        })

    return _add_to_current_container(
        Component(
            type="Series",
            props={
                "interfaces": interfaces,
                "submit_label": kwargs.get("submit_label", "Run"),
            },
        )
    )


def compare(
    *fns: Callable[..., Any],
    titles: list[str] | None = None,
    **kwargs: Any,
) -> Component:
    """Run same inputs through multiple functions, compare outputs side-by-side."""
    global _interface_counter

    if not fns:
        raise ValueError("compare() requires at least one function")

    # Use first function's signature for shared inputs
    primary_info = _inspect_function(fns[0])
    docstring_descriptions = _parse_docstring(fns[0])

    shared_inputs = []
    for param in primary_info["params"]:
        desc = docstring_descriptions.get(param["name"], "")
        spec = _type_to_input(param["type"], param["name"], param["default"], desc)
        spec["param_name"] = param["name"]
        spec["has_default"] = param["has_default"]
        shared_inputs.append(spec)

    # Register each function
    fn_specs = []
    for i, fn in enumerate(fns):
        _interface_counter += 1
        iface_id = f"iface_{_interface_counter}"

        info = _inspect_function(fn)
        output_mode = _type_to_output(info["return_type"])
        exec_mode = "stream" if (info["is_generator"] or info["is_async_generator"]) else ("progress" if info["has_progress"] else "simple")

        title = titles[i] if titles and i < len(titles) else _fn_title(fn)

        _register_interface_handler(iface_id, fn, info, kwargs.get("cache", False), kwargs.get("timeout", 60.0))

        fn_specs.append({
            "id": iface_id,
            "title": title,
            "output_mode": output_mode,
            "exec_mode": exec_mode,
        })

    return _add_to_current_container(
        Component(
            type="Compare",
            props={
                "functions": fn_specs,
                "inputs": shared_inputs,
                "param_names": [p["name"] for p in primary_info["params"]],
                "submit_label": kwargs.get("submit_label", "Compare"),
            },
        )
    )
