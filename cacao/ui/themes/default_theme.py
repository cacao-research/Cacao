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
        --primary-color: rgb(107, 66, 38);        /* Cacao brown */
        --secondary-color: #2ecc71;              /* Fresh green accent */
        --font-color: #3b2c23;                   /* Darker brown for text */
        --bg-color: #fff8f2;                     /* Soft cacao background */
        --font-family: 'Segoe UI', Arial, sans-serif;

        --input-bg: #ffffff;
        --input-border: #d8cfc7;                 /* Softer brown-gray border */
        --input-radius: 6px;
        --input-padding: 10px;
        --input-focus: rgba(107, 66, 38, 0.2);   /* Light brown focus ring */
        --input-disabled: #f3f0ed;

        --checkbox-accent: var(--primary-color);
        --switch-bg: #ccc;
        --switch-checked-bg: var(--primary-color);

        --rate-star: #f4c542;                    /* Golden yellow */
        --rate-star-empty: #eee;

        --upload-border: var(--secondary-color);
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
