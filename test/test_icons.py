"""Test suite for icon processing functionality."""

import pytest
from cacao.utilities.icons import icon_registry, process_icons_in_component

def test_icon_pattern_matching():
    """Test that the new icon syntax pattern is correctly matched."""
    content = "Welcome {%icon-fa-home%} {%icon-ca-user%}"
    result = process_icons_in_component({
        "type": "div",
        "props": {"content": content}
    })
    
    # Result should contain FontAwesome and SVG icon HTML
    processed = result["props"]["content"]
    assert '<i class="fa fa-home"' in processed
    assert 'class=\'cacao-icon\'' in processed
    assert 'class=\'icon-error\'>Icon not found: user' in processed  # Check for error message for unregistered icon

def test_icon_parameters():
    """Test icon parameters with new syntax."""
    content = "{%icon-fa-star color=#FFD700 size=32%}"
    result = process_icons_in_component({
        "type": "div",
        "props": {"content": content}
    })
    
    processed = result["props"]["content"]
    assert 'color:#FFD700' in processed
    assert 'font-size:32px' in processed

def test_pre_tag_skipping():
    """Test that pre tags preserve raw icon syntax."""
    content = """{%icon-ca-name%}
{%icon-ca-name color=#ff0000%}"""
    
    result = process_icons_in_component({
        "type": "pre",
        "props": {"content": content}
    })
    
    # Content should remain unchanged in pre tags
    assert result["props"]["content"] == content

def test_multiple_icons_with_parameters():
    """Test multiple icons with different parameters."""
    content = "Icons: {%icon-fa-home size=24%} {%icon-fa-user color=#333%}"
    result = process_icons_in_component({
        "type": "div",
        "props": {"content": content}
    })
    
    processed = result["props"]["content"]
    assert 'font-size:24px' in processed
    assert 'color:#333' in processed

def test_custom_svg_icon():
    """Test custom SVG icon rendering."""
    # Register a test SVG icon
    test_svg = '<svg viewBox="0 0 24 24"><path d="M12 2L2 22h20L12 2z"/></svg>'
    icon_registry.register_icon("test", test_svg)
    
    content = "{%icon-ca-test size=48 color=#ff0000%}"
    result = process_icons_in_component({
        "type": "div",
        "props": {"content": content}
    })
    
    processed = result["props"]["content"]
    assert 'width="48"' in processed
    assert 'fill="#ff0000"' in processed