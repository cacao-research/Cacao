"""Tests for the cacao.testing module — validates the testing framework itself."""

import asyncio

from cacao.server.signal import Signal
from cacao.testing import (
    MockSession,
    MockWebSocket,
    fire_event_sync,
    mock_app,
    mock_signals,
    snapshot,
)


def test_mock_session_creates_unique_ids():
    s1 = MockSession()
    s2 = MockSession()
    assert s1.id != s2.id


def test_mock_session_custom_id():
    s = MockSession(session_id="custom-123")
    assert s.id == "custom-123"


def test_mock_websocket_records_messages():
    async def _run():
        ws = MockWebSocket()
        session = MockSession(websocket=ws)
        await session.send_state({"count": 5})
        assert len(ws.messages) == 1
        assert ws.messages[0]["type"] == "update"
        assert ws.messages[0]["changes"] == {"count": 5}

    asyncio.run(_run())


def test_mock_websocket_get_toasts():
    async def _run():
        ws = MockWebSocket()
        session = MockSession(websocket=ws)
        await session.send_toast("Hello!", variant="success")
        toasts = ws.get_toasts()
        assert len(toasts) == 1
        assert toasts[0]["message"] == "Hello!"
        assert toasts[0]["variant"] == "success"

    asyncio.run(_run())


def test_mock_signals_context():
    with mock_signals() as session:
        sig = Signal(0, name="test_val")
        sig.set(session, 42)
        assert sig.get(session) == 42

    # Signal should be cleaned up
    assert "test_val" not in Signal._all_signals


def test_mock_app_context():
    with mock_app() as (app, session):
        count = Signal(0, name="counter")

        @app.on("increment")
        async def handle(s, data):
            count.set(s, count.get(s) + 1)

        fire_event_sync(app, session, "increment")
        assert count.get(session) == 1


def test_snapshot_creates_and_compares():
    import tempfile
    import os
    import json

    with tempfile.TemporaryDirectory() as tmpdir:
        snap_dir = os.path.join(tmpdir, "snaps")

        data = {"type": "Title", "props": {"text": "Hello"}}

        # First call — creates snapshot
        result = snapshot(data, "test_snap", snapshot_dir=snap_dir)
        assert result.passed
        assert result.is_new

        # Second call — matches
        result = snapshot(data, "test_snap", snapshot_dir=snap_dir)
        assert result.passed
        assert not result.is_new

        # Modified data — should fail
        modified = {"type": "Title", "props": {"text": "Changed"}}
        result = snapshot(modified, "test_snap", snapshot_dir=snap_dir)
        assert not result.passed
        assert result.diff is not None


def test_session_without_websocket_is_silent():
    """Sending to a session with no websocket should not raise."""
    async def _run():
        session = MockSession()
        await session.send_state({"x": 1})
        await session.send_toast("hi")

    asyncio.run(_run())


def test_signal_isolation_between_sessions():
    with mock_signals() as s1:
        sig = Signal("default", name="iso")
        s2 = MockSession()
        sig.set(s1, "alice")
        sig.set(s2, "bob")
        assert sig.get(s1) == "alice"
        assert sig.get(s2) == "bob"
