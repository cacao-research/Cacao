"""Tests for session management."""

from cacao.server.session import Session, SessionManager
from cacao.server.signal import Signal


class TestSessionManager:
    def setup_method(self) -> None:
        Signal._all_signals.clear()
        SessionManager._all_sessions.clear()

    def test_create_and_get(self) -> None:
        mgr = SessionManager()
        session = mgr.create()
        assert isinstance(session, Session)
        assert SessionManager.get(session.id) is session

    def test_remove_cleans_up(self) -> None:
        mgr = SessionManager()
        session = mgr.create()
        sid = session.id
        mgr.remove(sid)
        assert SessionManager.get(sid) is None
        assert mgr.count == 0

    def test_count(self) -> None:
        mgr = SessionManager()
        mgr.create()
        mgr.create()
        assert mgr.count == 2
