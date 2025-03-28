import pytest
from cacao import mix
from cacao.core.server import CacaoServer
from cacao.core.decorators import ROUTES

@pytest.fixture
def test_server():
    server = CacaoServer()
    yield server
    # No explicit shutdown method needed

def test_server_initialization(test_server):
    assert test_server is not None
    assert hasattr(test_server, '_handle_websocket')
    assert test_server.http_port == 1634
    assert test_server.ws_port == 1633

def test_route_registration():
    # Store original routes dictionary
    original_routes = ROUTES.copy()
    try:
        # Clear existing routes
        ROUTES.clear()
        
        # Register a route and check if it's added
        @mix("/test")
        def test_route():
            return {"type": "div", "props": {"content": "Test Route"}}
        
        # Check that the route has been registered
        assert "/test" in ROUTES
        assert callable(ROUTES["/test"])
        # Test that the function's original name is preserved (instead of being 'wrapper')
        assert ROUTES["/test"].__name__ == "test_route"
    finally:
        # Restore original routes
        ROUTES.clear()
        ROUTES.update(original_routes)

def test_websocket_handler(test_server):
    assert hasattr(test_server, '_handle_websocket')
    assert callable(test_server._handle_websocket)