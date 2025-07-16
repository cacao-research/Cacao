/**
 * Theme Loader for Cacao Framework
 * Loads the CSS from default_theme.py and injects it into the HTML template
 */

document.addEventListener('DOMContentLoaded', async function() {
    try {
        // Fetch the theme CSS from the server
        console.log('[ThemeLoader] window.location.origin:', window.location.origin);
        console.log('[ThemeLoader] Fetching theme CSS from:', '/api/theme-css');
        const response = await fetch('/api/theme-css');
        
        if (!response.ok) {
            console.error('[ThemeLoader] Failed to load theme CSS:', response.status);
            return;
        }
        
        const css = await response.text();
        
        // Find the theme-css style element
        const styleElement = document.getElementById('theme-css');
        
        if (styleElement) {
            // Inject the CSS into the style element
            styleElement.textContent = css;
            console.log('[ThemeLoader] Theme CSS loaded successfully');
        } else {
            // Create a new style element if it doesn't exist
            const newStyle = document.createElement('style');
            newStyle.id = 'theme-css';
            newStyle.textContent = css;
            document.head.appendChild(newStyle);
            console.log('[ThemeLoader] Theme CSS injected successfully');
        }
    } catch (error) {
        console.error('[ThemeLoader] Error loading theme CSS:', error);
    }
});