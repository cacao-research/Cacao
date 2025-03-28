import pytest
from cacao import State, Component, mix
from cacao.core.server import CacaoServer
from cacao.core.session import SessionManager

@pytest.fixture(scope="session")
def app_server():
    server = CacaoServer(testing=True)
    yield server
    server.shutdown()

@pytest.fixture
def test_state():
    return State(initial_value=0)

@pytest.fixture
def session_mgr():
    return SessionManager(storage_type="memory")

@pytest.fixture
def base_component():
    class TestComponent(Component):
        def render(self):
            return {
                "type": "div",
                "props": {"content": "Test"}
            }
    return TestComponent()