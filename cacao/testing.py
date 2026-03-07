"""
Testing utilities for Cacao applications.

Provides mock sessions, signal helpers, snapshot testing, and a test runner
that discovers and executes test functions in Cacao app files.

Usage (in test files):
    import cacao as c
    from cacao.testing import MockSession, mock_signals, snapshot

    def test_counter():
        session = MockSession()
        count = c.signal(0, name="count")
        count.set(session, 5)
        assert count.get(session) == 5

Usage (CLI):
    cacao test app.py          # Run tests in app.py
    cacao test tests/          # Run all test_*.py files in directory
    cacao test app.py -v       # Verbose output
"""

from __future__ import annotations

import asyncio
import inspect
import json
import os
import sys
import time
import traceback
from collections.abc import Callable
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Generator

from .server.session import Session, SessionManager
from .server.signal import Computed, Signal


# =============================================================================
# Mock WebSocket
# =============================================================================


class MockWebSocket:
    """
    A fake WebSocket that records sent messages instead of transmitting them.

    Useful for testing event handlers that send state updates, toasts,
    or notifications back to the client.

    Example:
        ws = MockWebSocket()
        session = MockSession(websocket=ws)
        await session.send_state({"count": 5})
        assert ws.messages[-1] == {"type": "update", "changes": {"count": 5}}
    """

    def __init__(self) -> None:
        self.messages: list[dict[str, Any]] = []
        self.closed: bool = False

    async def send_json(self, data: dict[str, Any]) -> None:
        """Record a JSON message."""
        self.messages.append(data)

    async def receive_json(self) -> dict[str, Any]:
        """Simulate receiving — returns empty dict."""
        return {}

    async def close(self, code: int = 1000) -> None:
        """Mark the websocket as closed."""
        self.closed = True

    def get_state_updates(self) -> list[dict[str, Any]]:
        """Get all state update messages."""
        return [m for m in self.messages if m.get("type") == "update"]

    def get_toasts(self) -> list[dict[str, Any]]:
        """Get all toast notification messages."""
        return [m for m in self.messages if m.get("type") == "toast"]

    def get_last_state(self) -> dict[str, Any]:
        """Get the most recent state update's changes, or empty dict."""
        updates = self.get_state_updates()
        if updates:
            return updates[-1].get("changes", {})
        return {}

    def clear(self) -> None:
        """Clear all recorded messages."""
        self.messages.clear()


# =============================================================================
# Mock Session
# =============================================================================


class MockSession(Session):
    """
    A test-friendly Session that doesn't require a real WebSocket connection.

    Optionally accepts a MockWebSocket to capture outgoing messages.

    Example:
        session = MockSession()
        count = Signal(0, name="count")
        count.set(session, 10)
        assert count.get(session) == 10

        # With message capture:
        ws = MockWebSocket()
        session = MockSession(websocket=ws)
        await session.send_toast("Done!", variant="success")
        assert ws.get_toasts()[0]["message"] == "Done!"
    """

    _counter: int = 0

    def __init__(
        self,
        *,
        session_id: str | None = None,
        websocket: MockWebSocket | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        MockSession._counter += 1
        sid = session_id or f"test-session-{MockSession._counter}"
        super().__init__(
            id=sid,
            websocket=websocket,  # type: ignore[arg-type]
            metadata=metadata or {},
        )


# =============================================================================
# Signal & Session Mocking Context
# =============================================================================


@contextmanager
def mock_signals() -> Generator[MockSession, None, None]:
    """
    Context manager that provides a clean signal/session environment for testing.

    Clears all global signals on entry, creates a fresh MockSession,
    and cleans up on exit.

    Example:
        with mock_signals() as session:
            count = Signal(0, name="count")
            count.set(session, 42)
            assert count.get(session) == 42
        # Signals and session are cleaned up here
    """
    # Save and clear global state
    saved_signals = Signal._all_signals.copy()
    saved_sessions = SessionManager._all_sessions.copy()
    Signal._all_signals.clear()
    SessionManager._all_sessions.clear()

    session = MockSession()

    try:
        yield session
    finally:
        # Clean up signals for this session
        Signal.clear_all_for_session(session)
        # Restore previous state
        Signal._all_signals.clear()
        Signal._all_signals.update(saved_signals)
        SessionManager._all_sessions.clear()
        SessionManager._all_sessions.update(saved_sessions)


@contextmanager
def mock_app() -> Generator[tuple[Any, MockSession], None, None]:
    """
    Context manager that provides a clean App + MockSession for testing.

    Resets the simple API global state, creates a fresh app context,
    and cleans up on exit.

    Example:
        with mock_app() as (app, session):
            @app.on("increment")
            async def handle(s, data):
                count.set(s, count.get(s) + 1)

            await app.handle_event(session, "increment", {})
    """
    from .server.app import App

    saved_signals = Signal._all_signals.copy()
    saved_sessions = SessionManager._all_sessions.copy()
    Signal._all_signals.clear()
    SessionManager._all_sessions.clear()

    app = App()
    session = MockSession()

    try:
        yield app, session
    finally:
        Signal.clear_all_for_session(session)
        Signal._all_signals.clear()
        Signal._all_signals.update(saved_signals)
        SessionManager._all_sessions.clear()
        SessionManager._all_sessions.update(saved_sessions)


# =============================================================================
# Event Dispatch Helper
# =============================================================================


async def fire_event(
    app: Any,
    session: Session,
    event_name: str,
    data: dict[str, Any] | None = None,
) -> None:
    """
    Dispatch an event through the app's full middleware + handler chain.

    A convenience wrapper around app.handle_event for cleaner test code.

    Example:
        await fire_event(app, session, "submit", {"name": "Alice"})
    """
    await app.handle_event(session, event_name, data or {})


def fire_event_sync(
    app: Any,
    session: Session,
    event_name: str,
    data: dict[str, Any] | None = None,
) -> None:
    """
    Synchronous version of fire_event for simpler test code.

    Creates or reuses an event loop to run the async dispatch.

    Example:
        fire_event_sync(app, session, "submit", {"name": "Alice"})
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # Already in an async context — create a new task
        loop.run_until_complete(fire_event(app, session, event_name, data))
    else:
        asyncio.run(fire_event(app, session, event_name, data))


# =============================================================================
# Snapshot Testing
# =============================================================================


@dataclass
class SnapshotResult:
    """Result of a snapshot comparison."""

    passed: bool
    snapshot_path: Path
    is_new: bool = False
    diff: str | None = None


def snapshot(
    component_tree: Any,
    name: str,
    *,
    snapshot_dir: str = "__snapshots__",
    update: bool = False,
) -> SnapshotResult:
    """
    Compare a UI definition against a stored snapshot.

    On first run, creates the snapshot file. On subsequent runs, compares
    the current output against the stored snapshot.

    Args:
        component_tree: A Component, list of Components, or dict to snapshot.
        name: Unique name for this snapshot (used as filename).
        snapshot_dir: Directory to store snapshots (default: __snapshots__).
        update: If True, overwrite existing snapshot with current value.

    Returns:
        SnapshotResult with pass/fail status and optional diff.

    Example:
        tree = app.get_page_tree("/")
        result = snapshot(tree, "home_page")
        assert result.passed
    """
    # Serialize the component tree
    if hasattr(component_tree, "to_dict"):
        data = component_tree.to_dict()
    elif isinstance(component_tree, list):
        data = [c.to_dict() if hasattr(c, "to_dict") else c for c in component_tree]
    else:
        data = component_tree

    current_json = json.dumps(data, indent=2, sort_keys=True, default=str)

    # Determine snapshot file location
    # Use the caller's directory as base
    caller_frame = inspect.stack()[1]
    caller_dir = Path(caller_frame.filename).parent
    snap_dir = caller_dir / snapshot_dir
    snap_dir.mkdir(parents=True, exist_ok=True)

    snap_file = snap_dir / f"{name}.json"

    # First run or update mode — write snapshot
    if not snap_file.exists() or update:
        snap_file.write_text(current_json, encoding="utf-8")
        return SnapshotResult(passed=True, snapshot_path=snap_file, is_new=not update)

    # Compare against stored snapshot
    stored_json = snap_file.read_text(encoding="utf-8")

    if current_json == stored_json:
        return SnapshotResult(passed=True, snapshot_path=snap_file)

    # Generate a simple diff
    diff_lines: list[str] = []
    current_lines = current_json.splitlines()
    stored_lines = stored_json.splitlines()

    max_lines = max(len(current_lines), len(stored_lines))
    for i in range(max_lines):
        cur = current_lines[i] if i < len(current_lines) else ""
        sto = stored_lines[i] if i < len(stored_lines) else ""
        if cur != sto:
            diff_lines.append(f"  line {i + 1}:")
            diff_lines.append(f"    expected: {sto}")
            diff_lines.append(f"    got:      {cur}")

    diff_text = "\n".join(diff_lines) if diff_lines else "Content differs (whitespace/ordering)"

    return SnapshotResult(passed=False, snapshot_path=snap_file, diff=diff_text)


# =============================================================================
# Test Runner
# =============================================================================

# ANSI colors (matching cli/commands.py style)
_GREEN = "\033[92m"
_RED = "\033[91m"
_YELLOW = "\033[93m"
_CYAN = "\033[96m"
_DIM = "\033[2m"
_BOLD = "\033[1m"
_RESET = "\033[0m"


@dataclass
class TestResult:
    """Result of a single test function execution."""

    name: str
    passed: bool
    duration_ms: float
    error: str | None = None


@dataclass
class TestSuiteResult:
    """Aggregated results from running a test suite."""

    results: list[TestResult] = field(default_factory=list)
    total_duration_ms: float = 0.0

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if not r.passed)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def all_passed(self) -> bool:
        return self.failed == 0


def _discover_test_functions(module: Any) -> list[tuple[str, Callable[..., Any]]]:
    """Find all functions in a module whose name starts with 'test_' or 'test'."""
    tests: list[tuple[str, Callable[..., Any]]] = []

    for name in sorted(dir(module)):
        if not name.startswith("test_") and name != "test":
            continue
        obj = getattr(module, name, None)
        if obj is None or not callable(obj):
            continue
        # Skip classes (we only run functions)
        if inspect.isclass(obj):
            continue
        tests.append((name, obj))

    return tests


def _run_single_test(name: str, func: Callable[..., Any]) -> TestResult:
    """Run a single test function and return the result."""
    start = time.perf_counter()

    try:
        result = func()
        # Handle async test functions
        if asyncio.iscoroutine(result):
            asyncio.run(result)

        duration = (time.perf_counter() - start) * 1000
        return TestResult(name=name, passed=True, duration_ms=duration)

    except Exception:
        duration = (time.perf_counter() - start) * 1000
        tb = traceback.format_exc()
        return TestResult(name=name, passed=False, duration_ms=duration, error=tb)


def run_tests(
    target: str | Path,
    *,
    verbose: bool = False,
    pattern: str = "test_*.py",
    update_snapshots: bool = False,
) -> TestSuiteResult:
    """
    Discover and run tests in a file or directory.

    Test functions are any module-level function whose name starts with 'test_'.
    Both sync and async test functions are supported.

    Args:
        target: Path to a .py file or directory containing test files.
        verbose: Print detailed output for each test.
        pattern: Glob pattern for test file discovery (default: test_*.py).
        update_snapshots: If True, set environment variable to update snapshots.

    Returns:
        TestSuiteResult with all test outcomes.

    Example:
        result = run_tests("tests/")
        assert result.all_passed
    """
    import importlib.util

    if update_snapshots:
        os.environ["CACAO_UPDATE_SNAPSHOTS"] = "1"

    target_path = Path(target)
    suite = TestSuiteResult()
    suite_start = time.perf_counter()

    # Collect test files
    if target_path.is_file():
        test_files = [target_path]
    elif target_path.is_dir():
        test_files = sorted(target_path.rglob(pattern))
    else:
        print(f"{_RED}Error: '{target}' not found{_RESET}")
        return suite

    if not test_files:
        print(f"{_YELLOW}No test files found matching '{pattern}' in {target}{_RESET}")
        return suite

    for test_file in test_files:
        # Load the module
        file_label = str(test_file)
        try:
            app_dir = test_file.parent.resolve()
            if str(app_dir) not in sys.path:
                sys.path.insert(0, str(app_dir))

            spec = importlib.util.spec_from_file_location(
                f"__cacao_test_{test_file.stem}__", test_file.resolve()
            )
            if spec is None or spec.loader is None:
                print(f"{_RED}Could not load {file_label}{_RESET}")
                continue

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

        except Exception:
            tb = traceback.format_exc()
            print(f"{_RED}Error loading {file_label}:{_RESET}")
            print(tb)
            suite.results.append(
                TestResult(name=f"{file_label}::load", passed=False, duration_ms=0, error=tb)
            )
            continue

        # Discover and run tests
        tests = _discover_test_functions(module)

        if not tests:
            if verbose:
                print(f"{_DIM}  {file_label}: no tests found{_RESET}")
            continue

        if verbose or len(test_files) > 1:
            print(f"\n{_BOLD}{file_label}{_RESET}")

        for test_name, test_func in tests:
            # Reset cacao simple-mode state between tests
            try:
                from . import simple

                simple.reset()
            except Exception:
                pass

            # Clear signals between tests
            Signal._all_signals.clear()
            SessionManager._all_sessions.clear()

            result = _run_single_test(test_name, test_func)
            suite.results.append(result)

            if result.passed:
                if verbose:
                    print(
                        f"  {_GREEN}PASS{_RESET} {test_name}"
                        f"  {_DIM}({result.duration_ms:.1f}ms){_RESET}"
                    )
            else:
                print(f"  {_RED}FAIL{_RESET} {test_name}")
                if result.error:
                    # Indent the traceback
                    for line in result.error.strip().splitlines():
                        print(f"    {_DIM}{line}{_RESET}")

    suite.total_duration_ms = (time.perf_counter() - suite_start) * 1000

    # Clean up env var
    os.environ.pop("CACAO_UPDATE_SNAPSHOTS", None)

    # Print summary
    print()
    if suite.all_passed:
        print(
            f"  {_GREEN}{_BOLD}{suite.passed} passed{_RESET}"
            f"  {_DIM}({suite.total_duration_ms:.0f}ms){_RESET}"
        )
    else:
        parts: list[str] = []
        if suite.passed:
            parts.append(f"{_GREEN}{suite.passed} passed{_RESET}")
        parts.append(f"{_RED}{suite.failed} failed{_RESET}")
        print(f"  {', '.join(parts)}  {_DIM}({suite.total_duration_ms:.0f}ms){_RESET}")

    return suite
