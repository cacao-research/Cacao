"""
Default theme for the Cacao framework.
Provides built-in theme settings for CSS and JS.
"""

class DefaultTheme:
    """
    Default theme with basic styling and behavior.
    """
    CSS = """
    :root {
        --primary-color: #3498db;
        --secondary-color: #2ecc71;
        --font-color: #333;
        --bg-color: #fff;
        --font-family: Arial, sans-serif;
    }
    body {
        background-color: var(--bg-color);
        color: var(--font-color);
        font-family: var(--font-family);
    }
    """

    JS = """
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Default Cacao theme loaded.');
    });
    """
