# Icons

Use icons in your Cacao applications with a simple template syntax.

## Overview

The Icon Registry system enables templated icon insertion using syntax like:

- `{%icon-ca-home%}` for custom SVG icons
- `{%icon-fa-heart%}` for FontAwesome icons

## Basic Usage

Use icons directly in content strings:

```python
{
    "type": "h1",
    "props": {
        "content": "Welcome Home {%icon-ca-home%}"
    }
}
```

```python
{
    "type": "button",
    "props": {
        "label": "{%icon-fa-save%} Save"
    }
}
```

## Icon Syntax

The basic syntax is:

```
{%icon-prefix-name parameters%}
```

Where:

| Part | Description |
|------|-------------|
| `prefix` | `ca` for custom icons, `fa` for FontAwesome |
| `name` | The icon name |
| `parameters` | Optional `key=value` pairs |

## Parameters

Customize icons with parameters:

```python
# Set the color
{%icon-ca-home color=#ff0000%}

# Set the size (in pixels)
{%icon-ca-home size=32%}

# Multiple parameters
{%icon-fa-check size=24 color=#4CAF50%}
```

## Configuration

Configure icons in your `cacao.json`:

```json
{
    "icons": {
        "icon_directories": ["./icons", "./assets/icons"],
        "fontawesome_version": "6.4.2",
        "fontawesome_mode": "free",
        "enable_auto_loading": true,
        "cache_processed_icons": true
    }
}
```

| Option | Description |
|--------|-------------|
| `icon_directories` | Directories containing SVG icons |
| `fontawesome_version` | FontAwesome version to use |
| `fontawesome_mode` | `"free"` or `"pro"` |
| `enable_auto_loading` | Auto-load icons from directories |
| `cache_processed_icons` | Cache processed icons |

## FontAwesome Integration

FontAwesome is included in the default Cacao HTML template. If using a custom template, add:

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
```

### Common FontAwesome Icons

```python
# Navigation
{%icon-fa-home%}
{%icon-fa-arrow-left%}
{%icon-fa-arrow-right%}
{%icon-fa-bars%}

# Actions
{%icon-fa-plus%}
{%icon-fa-edit%}
{%icon-fa-trash%}
{%icon-fa-save%}

# Status
{%icon-fa-check%}
{%icon-fa-times%}
{%icon-fa-exclamation%}
{%icon-fa-info%}

# Social
{%icon-fa-github%}
{%icon-fa-twitter%}
{%icon-fa-linkedin%}
```

## Custom Icons

### Register Programmatically

```python
import cacao

custom_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
  <path d="M12,4C14.21,4 16,5.79 16,8C16,10.21 14.21,12 12,12C9.79,12 8,10.21 8,8C8,5.79 9.79,4 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z" fill="currentColor"/>
</svg>
"""

cacao.icon_registry.register_icon("user", custom_svg)
```

### Register from File

```python
cacao.icon_registry.register_icon_from_file("logo", "./icons/logo.svg")
```

### Load from Directory

```python
# Load all SVG files from a directory
count = cacao.icon_registry.load_icons_from_directory("./icons")
print(f"Loaded {count} icons")
```

## Icon Registry API

### Methods

| Method | Description |
|--------|-------------|
| `initialize(config)` | Initialize with configuration |
| `register_icon(name, svg_content)` | Register a custom SVG icon |
| `register_icon_from_file(name, file_path)` | Register from file |
| `load_icons_from_directory(directory)` | Load all SVGs from directory |
| `process_content(content)` | Replace icon placeholders |
| `get_icon(prefix, name, params)` | Get HTML for an icon |
| `get_all_icon_names()` | Get all registered icon names |
| `clear_cache()` | Clear the icon cache |

## Complete Example

```python
import cacao

app = cacao.App()

# Register a custom icon
cacao.icon_registry.register_icon("coffee", """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
  <path d="M2,21H20V19H2M20,8H18V5H20M20,3H4V13A4,4 0 0,0 8,17H14A4,4 0 0,0 18,13V10H20A2,2 0 0,0 22,8V5C22,3.89 21.1,3 20,3Z" fill="currentColor"/>
</svg>
""")

@app.mix("/")
def home():
    return {
        "type": "div",
        "props": {
            "style": {"padding": "40px", "textAlign": "center"}
        },
        "children": [
            {
                "type": "h1",
                "props": {
                    "content": "{%icon-ca-coffee size=48%} Welcome to Cacao"
                }
            },
            {
                "type": "p",
                "props": {
                    "content": "{%icon-fa-heart color=#e74c3c%} Built with love"
                }
            },
            {
                "type": "button",
                "props": {
                    "label": "{%icon-fa-github%} View on GitHub",
                    "action": "open_github"
                }
            }
        ]
    }

if __name__ == "__main__":
    app.brew()
```

## How It Works

1. When the server starts, it initializes the icon registry with your configuration
2. The registry loads SVG files from configured directories
3. When rendering UI, the system finds and replaces icon placeholders
4. Custom SVG icons are inserted directly into the HTML
5. FontAwesome icons generate appropriate HTML tags with classes

## Best Practices

### 1. Use Consistent Sizing

```python
# Define icon sizes as constants
ICON_SM = "size=16"
ICON_MD = "size=24"
ICON_LG = "size=32"

f"{{%icon-fa-home {ICON_MD}%}}"
```

### 2. Match Icon Colors to Theme

```python
from cacao.core import get_color

primary = get_color("primary")
f"{{%icon-fa-check color={primary}%}}"
```

### 3. Provide Fallback Text

For accessibility, include text alongside icons:

```python
{
    "type": "button",
    "props": {
        "label": "{%icon-fa-save%} Save",  # Icon + text
        "aria-label": "Save document"
    }
}
```

## Next Steps

- [Theming](theming.md) - Style icons with your theme
- [Components](components.md) - Build icon-enhanced components
