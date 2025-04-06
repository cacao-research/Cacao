# Cacao Theming Guide

This guide explains how to customize the appearance of your Cacao applications using themes.

## Global Theme System

Cacao provides a global theme system that allows you to set theme properties at the application level and have components inherit these properties. This makes it easy to maintain a consistent look and feel across your entire application.

### Setting a Global Theme

You can set a global theme when starting your application using the `theme` parameter in the `app.brew()` method:

```python
import cacao

app = cacao.App()

# Define your custom theme
my_theme = {
    "colors": {
        "primary": "#2196F3",
        "secondary": "#03A9F4",
        "background": "#F0F8FF",
        "text": "#2C3E50",
        "accent": "#FF5722",
        "sidebar_bg": "#1A365D",
        "sidebar_header_bg": "#2C5282",
        "content_bg": "#F0F8FF",
        "card_bg": "#FFFFFF",
        "border_color": "#BEE3F8"
    }
}

# Create your components and routes
# ...

# Start the application with your custom theme
app.brew(
    type="web",
    title="My Themed App",
    theme=my_theme
)
```

### Default Theme Properties

The default theme includes the following color properties:

```python
DEFAULT_THEME = {
    "colors": {
        "secondary": "#2ecc71",    # Secondary color for accents
        "background": "#ffffff",   # Main background color
        "text": "#333333",         # Main text color
        "accent": "#e74c3c",       # Accent color for highlights
        # Component-specific colors
        "sidebar_bg": "#2D2013",          # Sidebar background
        "sidebar_header_bg": "#6B4226",   # Sidebar header background
        "sidebar_text": "#D6C3B6",        # Sidebar text color
        "content_bg": "#FAF6F3",          # Content area background
        "card_bg": "#FFFFFF",             # Card background
        "border_color": "#D6C3B6",        # Border color
    }
}
```

You can override any of these properties in your custom theme.

### Component-Level Styles

Components can also accept local style overrides through a `styles` parameter. These styles will take precedence over the global theme:

```python
from cacao.ui.components.sidebar_layout import SidebarLayout

# Create a sidebar layout with custom styles
sidebar = SidebarLayout(
    nav_items=nav_items,
    content_components=content_components,
    app_title="My App",
    styles={
        "sidebar_header_bg": "#9b59b6",  # Purple header (overrides the global theme)
        "card_padding": "32px"           # More padding in cards
    }
)
```

## Theme API

### Setting the Theme

```python
from cacao.core import set_theme

# Set or update the global theme
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
background_color = get_color("background", "#ffffff")  # With default fallback
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

## Complete Example

See `examples/theme_example.py` for a complete example of using the global theme system.

```bash
# Run with default theme
python examples/theme_example.py

# Run with dark theme
python examples/theme_example.py --theme dark

# Run with blue theme
python examples/theme_example.py --theme blue
