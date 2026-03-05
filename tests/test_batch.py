"""Tests for the Batch update system."""

from cacao.server.batch import Batch, BatchContext, get_current_batch, is_batching
from cacao.server.session import Session
from cacao.server.signal import Signal


def _make_session(sid: str = "test") -> Session:
    return Session(id=sid)


class TestBatchContext:
    def test_add_update(self) -> None:
        session = _make_session()
        ctx = BatchContext(session)
        ctx.add_update("count", 5)
        ctx.add_update("name", "test")
        assert ctx.updates == {"count": 5, "name": "test"}

    def test_add_update_overwrites(self) -> None:
        session = _make_session()
        ctx = BatchContext(session)
        ctx.add_update("x", 1)
        ctx.add_update("x", 2)
        assert ctx.updates["x"] == 2


class TestBatch:
    def setup_method(self) -> None:
        Signal._all_signals.clear()

    def test_set_and_len(self) -> None:
        session = _make_session()
        sig = Signal(0, name="count")
        b = Batch(session)
        b.set(sig, 10)
        assert len(b) == 1
        assert sig._values[session.id] == 10

    def test_chaining(self) -> None:
        session = _make_session()
        a = Signal(0, name="a")
        b_sig = Signal("", name="b")
        batch = Batch(session)
        batch.set(a, 5).set(b_sig, "hello")
        assert len(batch) == 2

    def test_update_with_fn(self) -> None:
        session = _make_session()
        sig = Signal(10, name="val")
        b = Batch(session)
        b.update(sig, lambda x: x + 5)
        assert sig._values[session.id] == 15

    def test_bool(self) -> None:
        session = _make_session()
        b = Batch(session)
        assert not b
        b.set(Signal(0, name="x"), 1)
        assert b


class TestBatchHelpers:
    def test_is_batching_false(self) -> None:
        assert not is_batching("nonexistent")

    def test_get_current_batch_none(self) -> None:
        assert get_current_batch("nonexistent") is None
