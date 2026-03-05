"""Tests for UI component serialization and tree building."""

from cacao.server.signal import Signal
from cacao.server.ui import (
    App,
    Component,
    _current_container,
    metric,
    row,
    title,
)


class TestComponent:
    def setup_method(self) -> None:
        Signal._all_signals.clear()

    def test_to_dict_basic(self) -> None:
        comp = Component(type="Button", props={"label": "Click"})
        d = comp.to_dict()
        assert d["type"] == "Button"
        assert d["props"]["label"] == "Click"
        assert "children" not in d

    def test_to_dict_with_children(self) -> None:
        child = Component(type="Text", props={"value": "hi"})
        parent = Component(type="Row", children=[child])
        d = parent.to_dict()
        assert len(d["children"]) == 1
        assert d["children"][0]["type"] == "Text"

    def test_signal_prop_serialization(self) -> None:
        sig = Signal(0, name="counter")
        comp = Component(type="Metric", props={"value": sig})
        d = comp.to_dict()
        assert d["props"]["value"] == {"__signal__": "counter"}

    def test_event_handler_serialization(self) -> None:
        comp = Component(type="Button", props={"on_click": lambda: None})
        d = comp.to_dict()
        assert d["props"]["on_click"] == {"__event__": "Button:on_click"}

    def test_nested_children(self) -> None:
        inner = Component(type="Text", props={"value": "hi"})
        mid = Component(type="Card", children=[inner])
        outer = Component(type="Row", children=[mid])
        d = outer.to_dict()
        assert d["children"][0]["children"][0]["type"] == "Text"


class TestAppPageTree:
    def setup_method(self) -> None:
        Signal._all_signals.clear()

    def test_page_collects_components(self) -> None:
        app = App(title="Test")
        with app.page("/"):
            title("Hello")
            metric("Users", 42)
        tree = app.get_page_tree("/")
        assert len(tree) == 2
        assert tree[0]["type"] == "Title"
        assert tree[1]["type"] == "Metric"

    def test_nested_layout(self) -> None:
        app = App(title="Test")
        with app.page("/"):
            with row():
                metric("A", 1)
                metric("B", 2)
        tree = app.get_page_tree("/")
        assert len(tree) == 1
        assert tree[0]["type"] == "Row"
        assert len(tree[0]["children"]) == 2

    def test_multiple_pages(self) -> None:
        app = App(title="Test")
        with app.page("/"):
            title("Home")
        with app.page("/about"):
            title("About")
        pages = app.get_all_pages()
        assert "/" in pages
        assert "/about" in pages
        assert pages["/"][0]["props"]["text"] == "Home"
        assert pages["/about"][0]["props"]["text"] == "About"
