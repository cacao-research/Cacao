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
    
    input[type="text"],
    input[type="password"],
    input[type="search"],
    input[type="date"],
    input[type="time"],
    textarea,
    select {
        width: 100%;
        padding: var(--input-padding);
        border: 1px solid var(--input-border);
        border-radius: var(--input-radius);
        background: var(--input-bg);
        color: var(--font-color);
        font-family: var(--font-family);
        margin-bottom: 10px;
        box-sizing: border-box;
        transition: border 0.2s, box-shadow 0.2s;
    }
    input[type="text"]:focus,
    input[type="password"]:focus,
    input[type="search"]:focus,
    input[type="date"]:focus,
    input[type="time"]:focus,
    textarea:focus,
    select:focus {
        outline: none;
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px var(--input-focus);
    }
    input[disabled],
    textarea[disabled],
    select[disabled] {
        background: var(--input-disabled);
        color: #aaa;
        cursor: not-allowed;
    }
    /* Checkbox */
    .checkbox-wrapper {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
        font-size: 1rem;
        cursor: pointer;
        padding: 8px 0 8px 4px;
        border-radius: 4px;
        transition: background 0.2s;
    }
    .checkbox-wrapper:hover {
        background: #f5f5f5;
    }
    .checkbox-wrapper input[type="checkbox"] {
        accent-color: var(--checkbox-accent);
        width: 18px;
        height: 18px;
        margin: 0 6px 0 0;
    }
    /* Radio */
    .radio-group {
        display: flex;
        gap: 20px;
        margin-bottom: 14px;
        padding: 4px 0 4px 2px;
    }
    .radio-wrapper {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 1rem;
        cursor: pointer;
        padding: 6px 0 6px 2px;
        border-radius: 4px;
        transition: background 0.2s;
    }
    .radio-wrapper:hover {
        background: #f5f5f5;
    }
    .radio-wrapper input[type="radio"] {
        accent-color: var(--primary-color);
        width: 18px;
        height: 18px;
        margin: 0 6px 0 0;
    }
    select option {
        padding: 8px 12px;
    }
    /* Switch */
    .switch-wrapper {
        position: relative;
        display: inline-flex;
        align-items: center;
        width: 44px;
        height: 24px;
        margin-right: 8px;
        margin-bottom: 0;
    }
    .switch-wrapper input[type="checkbox"] {
        opacity: 0;
        width: 0;
        height: 0;
    }
    .switch-slider {
        position: absolute;
        cursor: pointer;
        top: 0; left: 0; right: 0; bottom: 0;
        background: var(--switch-bg);
        border-radius: 24px;
        transition: background 0.2s;
    }
    .switch-wrapper input[type="checkbox"]:checked + .switch-slider {
        background: var(--switch-checked-bg);
    }
    .switch-slider:before {
        content: "";
        position: absolute;
        left: 4px;
        top: 4px;
        width: 16px;
        height: 16px;
        background: #fff;
        border-radius: 50%;
        transition: transform 0.2s;
    }
    .switch-wrapper input[type="checkbox"]:checked + .switch-slider:before {
        transform: translateX(20px);
    }
    /* Slider */
    .range-slider {
        width: 100%;
        margin: 10px 0;
        -webkit-appearance: none;
        background: transparent;
        height: 2px;
    }
    .range-slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        height: 20px;
        width: 20px;
        border-radius: 50%;
        background: var(--primary-color);
        cursor: pointer;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        border: 2px solid #fff;
        transition: all 0.2s;
    }
    .range-slider::-webkit-slider-thumb:hover {
        transform: scale(1.1);
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .range-slider::-webkit-slider-runnable-track {
        width: 100%;
        height: 4px;
        background: #eee;
        border-radius: 2px;
    }
    /* Rate (stars) */
    .rate-wrapper {
        display: flex;
        gap: 4px;
        font-size: 1.5rem;
        margin-bottom: 10px;
    }
    .rate-star {
        color: var(--rate-star-empty);
        cursor: pointer !important;
        transition: color 0.2s;
        user-select: none;
        position: relative;
        font-size: 2em;
    }
    .rate-star:hover {
        transform: scale(1.1);
    }
    .rate-star.filled {
        color: var(--rate-star);
    }
    .rate-star.half {
        color: var(--rate-star);
    }
    .rate-star.half:after {
        content: "★";
        color: var(--rate-star-empty);
        position: absolute;
        left: 50%;
        top: 0;
        width: 50%;
        overflow: hidden;
        z-index: 1;
    }
    /* Upload */
    .upload-wrapper {
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px dashed var(--upload-border);
        border-radius: var(--input-radius);
        padding: 20px;
        background: #fafafa;
        color: var(--font-color);
        margin-bottom: 10px;
        min-height: 60px;
    }
    .upload-wrapper input[type="file"] {
        width: auto;
        margin: 0;
        border: none;
        background: transparent;
        box-shadow: none;
        padding: 0;
    }
    /* Search input wrapper */
    .search-input-wrapper {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 10px;
    }
    """

    JS = """
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Default Cacao theme loaded.');
    });
    """
