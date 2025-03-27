# Cacao Theming Guide

This guide explains how to customize the appearance of your Cacao applications using themes.

## Default Theme

Cacao comes with a default theme that includes basic CSS variables:
- **Primary Color:** `#3498db`
- **Secondary Color:** `#2ecc71`
- **Font Family:** `Arial, sans-serif`

## Custom Themes

To create a custom theme, override the default theme by providing your own CSS and JS files.

Example custom theme in `cacao/ui/themes/custom_theme.py`:
```python
class CustomTheme:
    CSS = """
    :root {
        --primary-color: #2ecc71;
        --font-family: 'Roboto', sans-serif;
    }
    """
    JS = """
    document.addEventListener('cacao-init', () => {
        console.log('Custom theme loaded!');
    });
    """



Applying Themes
Themes can be loaded via the theme loader utility:

from cacao.ui.themes.theme_loader import load_theme

assets = load_theme("custom_theme")
Further Customizations
For advanced theming, consider:

Defining additional CSS variables.

Overriding default component styles.

Injecting custom JavaScript behavior.
