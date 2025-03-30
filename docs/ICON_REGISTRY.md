# Cacao Icon Registry System

The Icon Registry system for Cacao enables templated icon insertion using a simple syntax like `{%icon-ca-home%}` for custom icons and `{%icon-fa-heart%}` for FontAwesome icons.

## Features

- Centralized `IconRegistry` class that stores and manages both custom SVG icons and FontAwesome references
- Pattern matching to detect and replace icon placeholders in content strings
- Simple APIs for registering custom icons through SVG content or files
- Automatic loading of icon sets from configured directories
- Icon usage in any text content without requiring direct imports
- Configuration options in cacao.json for icon paths and FontAwesome versions
- Caching of processed icons for better performance

## Configuration

Add the following to your `cacao.json` file:

```json
"icons": {
    "icon_directories": ["./icons", "./assets/icons"],
    "fontawesome_version": "6.4.2",
    "fontawesome_mode": "free",
    "enable_auto_loading": true,
    "cache_processed_icons": true
}
```

- `icon_directories`: List of directories where SVG icons are stored
- `fontawesome_version`: Version of FontAwesome to use
- `fontawesome_mode`: "free" or "pro" depending on which FontAwesome package you're using
- `enable_auto_loading`: Whether to automatically load icons from configured directories
- `cache_processed_icons`: Whether to cache processed icons for better performance

## Using Icons

### In Content

Icons can be used directly in content strings using a simple syntax:

```python
{
    "type": "h1",
    "props": {
        "content": "Welcome Home {%icon-ca-home%}"
    }
}
```

### Syntax

The basic syntax is:

```
{%icon-prefix-name parameters%}
```

Where:
- `prefix`: Two-letter prefix, either:
  - `ca`: Custom icons (SVG)
  - `fa`: FontAwesome icons
- `name`: The name of the icon
- `parameters`: Optional space-separated parameters in `key=value` format

### Parameters

You can customize icons with parameters:

```python
# Set the color
{%icon-ca-home color=#ff0000%}

# Set the size (in pixels)
{%icon-ca-home size=32%}

# Multiple parameters
{%icon-fa-check size=24 color=#4CAF50%}
```

## FontAwesome Integration

To use FontAwesome icons, you need to include the FontAwesome library in your application. This is automatically included in the default Cacao HTML template, but if you're using a custom template, make sure to add:

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
```

## API Reference

### Main Class: IconRegistry

The main class that manages icons and processing.

#### Methods

- `initialize(config: Dict) -> None`: Initialize the registry with configuration
- `register_icon(name: str, svg_content: str) -> bool`: Register a custom SVG icon
- `register_icon_from_file(name: str, file_path: str) -> bool`: Register a custom SVG icon from a file
- `load_icons_from_directory(directory: str) -> int`: Load all SVG files from a directory as icons
- `process_content(content: str) -> str`: Process content string to replace icon placeholders
- `get_icon(prefix: str, name: str, params: Optional[str] = None) -> str`: Get HTML for an icon by prefix and name
- `get_all_icon_names() -> Dict[str, List[str]]`: Get all registered icon names grouped by prefix
- `clear_cache() -> None`: Clear the icon cache

### Example Usage

```python
import cacao

# Register a custom icon programmatically
custom_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
  <path d="M12,4C14.21,4 16,5.79 16,8C16,10.21 14.21,12 12,12C9.79,12 8,10.21 8,8C8,5.79 9.79,4 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z" fill="currentColor"/>
</svg>
"""
cacao.icon_registry.register_icon("user", custom_svg)

@app.mix("/")
def home():
    return {
        "type": "div",
        "props": {
            "content": "Welcome {%icon-ca-user%} to my app!"
        }
    }
```

## How It Works

1. When the Cacao server starts, it initializes the icon registry with the configuration from cacao.json
2. The registry loads any SVG files from the configured directories
3. When a route function is called, the resulting component tree is processed to find and replace icon placeholders
4. For custom SVG icons, the actual SVG content is inserted directly into the HTML
5. For FontAwesome icons, appropriate HTML tags are generated with the right classes and styles

This system allows for easy and flexible use of icons throughout your Cacao application without having to worry about icon imports or management.