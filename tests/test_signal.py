"""Tests for the reactive Signal primitive."""

from cacao.server.session import Session
from cacao.server.signal import Computed, Signal


def _make_session(sid: str = "test-session") -> Session:
    return Session(id=sid)


class TestSignal:
    def setup_method(self) -> None:
        Signal._all_signals.clear()

    def test_get_returns_default(self) -> None:
        sig = Signal(42, name="count")
        session = _make_session()
        assert sig.get(session) == 42

    def test_set_and_get(self) -> None:
        sig = Signal(0, name="val")
        session = _make_session()
        sig.set(session, 10)
        assert sig.get(session) == 10

    def test_session_isolation(self) -> None:
        sig = Signal("default", name="iso")
        s1 = _make_session("s1")
        s2 = _make_session("s2")
        sig.set(s1, "alice")
        assert sig.get(s1) == "alice"
        assert sig.get(s2) == "default"

    def test_set_skips_duplicate(self) -> None:
        sig = Signal(0, name="dup")
        session = _make_session()
        sig.set(session, 5)
        sig.set(session, 5)  # same value, no change
        assert sig.get(session) == 5

    def test_update_fn(self) -> None:
        sig = Signal(10, name="upd")
        session = _make_session()
        result = sig.update(session, lambda x: x + 5)
        assert result == 15
        assert sig.get(session) == 15

    def test_clear_session(self) -> None:
        sig = Signal(0, name="clr")
        session = _make_session()
        sig.set(session, 99)
        sig.clear_session(session)
        assert sig.get(session) == 0


class TestComputed:
    def setup_method(self) -> None:
        Signal._all_signals.clear()

    def test_computed_derives_value(self) -> None:
        count = Signal(3, name="base")
        doubled = Computed(lambda s: count.get(s) * 2, name="doubled", dependencies=[count])
        session = _make_session()
        assert doubled.get(session) == 6

    def test_computed_caches_value(self) -> None:
        call_count = 0

        def compute(s: Session) -> int:
            nonlocal call_count
            call_count += 1
            return 42

        comp = Computed(compute, name="cached")
        session = _make_session()
        assert comp.get(session) == 42
        assert comp.get(session) == 42
        assert call_count == 1  # only computed once
