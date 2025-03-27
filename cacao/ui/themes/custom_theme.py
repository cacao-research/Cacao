"""
Custom theme module for the Cacao framework.
Defines a custom theme to override default styles and behaviors.
"""

class CustomTheme:
    """
    Custom theme for Cacao. Override default styling and behavior.
    """
    CSS = """
    :root {
        --primary-color: #2ecc71;
        --font-family: 'Roboto', sans-serif;
    }
    body {
        font-family: 'Roboto', sans-serif;
    }
    """

    JS = """
    document.addEventListener('cacao-init', () => {
        console.log('Custom theme loaded!');
    });
    """
