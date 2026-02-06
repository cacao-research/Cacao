# Theming

Customize the appearance of your Cacao applications with themes.

## Global Theme System

Cacao provides a global theme system that allows you to set theme properties at the application level. Components inherit these properties for consistent styling.

## Setting a Theme

Set a global theme when starting your application:

```python
import cacao

app = cacao.App()

my_theme = {
    "colors": {
        "primary": "#2196F3",
        "secondary": "#03A9F4",
        "background": "#F0F8FF",
        "text": "#2C3E50",
        "accent": "#FF5722",
    }
}

# Start with your theme
app.brew(
    type="web",
    title="My Themed App",
    theme=my_theme
)
```

## Default Theme

The default theme includes these color properties:

```python
DEFAULT_THEME = {
    "colors": {
        "primary": "#6B4226",           # Primary brand color
        "secondary": "#2ecc71",         # Secondary accent
        "background": "#ffffff",        # Main background
        "text": "#333333",              # Main text color
        "accent": "#e74c3c",            # Highlight color
        "sidebar_bg": "#2D2013",        # Sidebar background
        "sidebar_header_bg": "#6B4226", # Sidebar header
        "sidebar_text": "#D6C3B6",      # Sidebar text
        "content_bg": "#FAF6F3",        # Content area
        "card_bg": "#FFFFFF",           # Card background
        "border_color": "#D6C3B6",      # Borders
    }
}
```

## Component-Level Styles

Components can accept local style overrides through a `styles` parameter:

```python
from cacao.ui.components.sidebar_layout import SidebarLayout

sidebar = SidebarLayout(
    nav_items=nav_items,
    content_components=content_components,
    app_title="My App",
    styles={
        "sidebar_header_bg": "#9b59b6",  # Override global theme
        "card_padding": "32px"
    }
)
```

Local styles take precedence over the global theme.

## Theme API

### Setting the Theme

```python
from cacao.core import set_theme

set_theme({
    "colors": {
        "primary": "#2196F3",
        "secondary": "#03A9F4"
    }
})
```

### Getting Theme Properties

```python
from cacao.core import get_theme, get_color

# Get the entire theme
theme = get_theme()

# Get a specific color
primary_color = get_color("primary")

# Get with fallback
bg_color = get_color("background", "#ffffff")
```

### Resetting the Theme

```python
from cacao.core import reset_theme

# Reset to default theme
reset_theme()
```

## Example Themes

### Dark Theme

```python
dark_theme = {
    "colors": {
        "primary": "#BB86FC",
        "secondary": "#03DAC6",
        "background": "#121212",
        "text": "#FFFFFF",
        "accent": "#CF6679",
        "sidebar_bg": "#1E1E1E",
        "sidebar_header_bg": "#6200EE",
        "sidebar_text": "#BBBBBB",
        "content_bg": "#121212",
        "card_bg": "#2D2D2D",
        "border_color": "#333333"
    }
}
```

### Blue Theme

```python
blue_theme = {
    "colors": {
        "primary": "#2196F3",
        "secondary": "#03A9F4",
        "background": "#F0F8FF",
        "text": "#2C3E50",
        "accent": "#FF5722",
        "sidebar_bg": "#1A365D",
        "sidebar_header_bg": "#2C5282",
        "sidebar_text": "#A0AEC0",
        "content_bg": "#F0F8FF",
        "card_bg": "#FFFFFF",
        "border_color": "#BEE3F8"
    }
}
```

### Green Theme

```python
green_theme = {
    "colors": {
        "primary": "#10B981",
        "secondary": "#34D399",
        "background": "#F0FDF4",
        "text": "#1F2937",
        "accent": "#F59E0B",
        "sidebar_bg": "#064E3B",
        "sidebar_header_bg": "#065F46",
        "sidebar_text": "#A7F3D0",
        "content_bg": "#ECFDF5",
        "card_bg": "#FFFFFF",
        "border_color": "#A7F3D0"
    }
}
```

## Using Theme Colors in Components

Access theme colors when building UI:

```python
from cacao.core import get_color

def themed_button(label: str, action: str) -> dict:
    return {
        "type": "button",
        "props": {
            "label": label,
            "action": action,
            "style": {
                "backgroundColor": get_color("primary"),
                "color": "white",
                "border": "none",
                "padding": "12px 24px",
                "borderRadius": "8px"
            }
        }
    }
```

## Dynamic Theme Switching

Allow users to switch themes at runtime:

```python
from cacao import State
from cacao.core import set_theme

themes = {
    "light": {...},
    "dark": {...}
}

current_theme = State("light")

@app.event("switch_theme")
def handle_theme_switch(event_data=None):
    if event_data and "theme" in event_data:
        theme_name = event_data["theme"]
        if theme_name in themes:
            set_theme(themes[theme_name])
            current_theme.set(theme_name)
    return {"theme": current_theme.value}
```

## Custom CSS

For advanced styling, add custom CSS:

```python
# In your project: static/css/custom.css

app.brew(
    type="web",
    custom_css="static/css/custom.css"
)
```

```css
/* static/css/custom.css */
.cacao-button {
    transition: all 0.2s ease;
}

.cacao-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
```

## Best Practices

### 1. Define Theme Constants

```python
# themes.py
THEMES = {
    "light": {...},
    "dark": {...},
    "custom": {...}
}

DEFAULT_THEME = "light"
```

### 2. Use Semantic Color Names

```python
# Good - semantic names
{
    "colors": {
        "primary": "#2196F3",
        "error": "#F44336",
        "success": "#4CAF50",
        "warning": "#FFC107"
    }
}

# Avoid - literal color names
{
    "colors": {
        "blue": "#2196F3",
        "red": "#F44336"
    }
}
```

### 3. Test Both Light and Dark Themes

Ensure your components look good in both light and dark modes.

## Complete Example

See `examples/theme_example.py` for a complete theming example:

```bash
# Run with default theme
python examples/theme_example.py

# Run with dark theme
python examples/theme_example.py --theme dark

# Run with blue theme
python examples/theme_example.py --theme blue
```

## Next Steps

- [Icons](icons.md) - Add icons with theming support
- [Components](components.md) - Build themed components
