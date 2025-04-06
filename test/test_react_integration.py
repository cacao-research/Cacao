"""
Tests for React component integration in Cacao.
"""

import pytest
import json
from unittest.mock import patch, MagicMock, AsyncMock

from cacao.ui import ReactComponent
from cacao.extensions.react_extension import ReactExtension


def test_react_component_initialization():
    """Test that ReactComponent initializes correctly."""
    # Create a React component
    component = ReactComponent(
        package="test-package",
        component="TestComponent",
        props={"test": "value"},
        version="1.0.0",
        css=["style.css"],
        cdn="https://example.com/cdn",
        id="test-id"
    )
    
    # Check that the component has the correct attributes
    assert component.package == "test-package"
    assert component.component == "TestComponent"
    assert component.props == {"test": "value"}
    assert component.version == "1.0.0"
    assert component.css == ["style.css"]
    assert component.cdn == "https://example.com/cdn"
    assert component.id == "test-id"


def test_react_component_render():
    """Test that ReactComponent renders correctly."""
    # Create a React component
    component = ReactComponent(
        package="test-package",
        component="TestComponent",
        props={"test": "value"},
        id="test-id"
    )
    
    # Render the component
    rendered = component.render()
    
    # Check that the rendered component has the correct structure
    assert rendered["type"] == "react-component"
    assert rendered["props"]["id"] == "test-id"
    assert rendered["props"]["package"] == "test-package"
    assert rendered["props"]["component"] == "TestComponent"
    assert rendered["props"]["props"] == {"test": "value"}
    assert rendered["props"]["version"] == "latest"
    assert rendered["props"]["css"] == []
    assert rendered["props"]["cdn"] == "https://cdn.jsdelivr.net/npm"


@pytest.mark.asyncio
async def test_react_extension():
    """Test that ReactExtension modifies the HTML template correctly."""
    # Create a mock server
    server = MagicMock()
    
    # Create a mock writer with AsyncMock for drain
    writer = MagicMock()
    writer.write = MagicMock()
    writer.drain = AsyncMock()
    
    # Create a ReactExtension
    extension = ReactExtension()
    
    # Apply the extension to the server
    extension.apply(server)
    
    # Call the original _serve_html_template method
    await server._serve_html_template(writer, "test-session-id")
    
    # Check that the writer.write method was called
    assert writer.write.called


@pytest.mark.asyncio
async def test_react_extension_html_modification():
    """Test that ReactExtension modifies the HTML content correctly."""
    # Create a mock server
    server = MagicMock()
    
    # Create a mock writer with AsyncMock for drain
    writer = MagicMock()
    writer.drain = AsyncMock()
    
    # Create a ReactExtension
    extension = ReactExtension()
    
    # Create a mock HTML content
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test</title>
    </head>
    <body>
        <div id="app"></div>
    </body>
    </html>
    """
    
    # Create a mock response with the HTML content
    response = f"""
    HTTP/1.1 200 OK
    Content-Type: text/html; charset=utf-8
    Content-Length: {len(html_content)}
    
    {html_content}
    """
    
    # Mock the writer.write method to capture the modified content
    captured_content = None
    
    def mock_write(data):
        nonlocal captured_content
        captured_content = data.decode('utf-8')
    
    writer.write = mock_write
    
    # Mock the original _serve_html_template method to write the response
    async def mock_serve_html(writer, session_id):
        writer.write(response.encode('utf-8'))
    
    server._serve_html_template = mock_serve_html
    
    # Apply the extension to the server
    extension.apply(server)
    
    # Call the modified _serve_html_template method
    await server._serve_html_template(writer, "test-session-id")
    
    # Check that the captured content contains the React bridge script and CSS
    assert captured_content is not None
    assert '<link rel="stylesheet" href="/static/css/react-components.css">' in captured_content
    assert '<script src="/static/js/react-bridge.js"></script>' in captured_content


def test_react_component_with_event_handler():
    """Test that ReactComponent handles events correctly."""
    # Create a React component with an event handler
    component = ReactComponent(
        package="test-package",
        component="TestComponent",
        props={
            "onChange": {
                "type": "event",
                "name": "test_event",
                "data": {"value": "$value"}
            }
        },
        id="test-id"
    )
    
    # Render the component
    rendered = component.render()
    
    # Check that the rendered component has the correct event handler
    assert rendered["props"]["props"]["onChange"]["type"] == "event"
    assert rendered["props"]["props"]["onChange"]["name"] == "test_event"
    assert rendered["props"]["props"]["onChange"]["data"] == {"value": "$value"}