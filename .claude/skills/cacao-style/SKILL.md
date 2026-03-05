---
name: cacao-style
description: Style Cacao components with LESS. Use when creating component styles, working with theme variables, adding responsive design, or ensuring dark/light mode compatibility.
---

# Cacao Styling Guide

Cacao uses LESS for styling with CSS custom properties for theming. All styles must work in both light and dark modes.

## File Structure

```
cacao/frontend/src/styles/
├── index.less          # Main entry, imports all
├── variables.less      # LESS variables (sizes, breakpoints)
├── mixins.less         # Reusable LESS mixins
├── base.less           # Reset, typography, utilities
├── layouts.less        # App layout, grid system
├── themes/
│   ├── dark.less       # Dark theme CSS variables
│   └── light.less      # Light theme CSS variables
└── components/
    ├── display.less    # Card, Metric, Table, Badge, etc.
    ├── form.less       # Button, Input, Select, etc.
    ├── typography.less # Title, Text, Code, etc.
    └── admin.less      # AppShell, NavSidebar, etc.
```

## Theme Variables (CSS Custom Properties)

**Always use these for colors** - they automatically switch with theme:

### Backgrounds
```less
var(--bg-primary)      // Main page background
var(--bg-secondary)    // Cards, elevated surfaces
var(--bg-tertiary)     // Inputs, nested elements
var(--bg-hover)        // Hover states
```

### Text
```less
var(--text-primary)    // Main text, headings
var(--text-secondary)  // Less prominent text
var(--text-muted)      // Labels, hints, disabled
var(--text-inverse)    // Text on accent backgrounds
```

### Accents
```less
var(--accent-primary)  // Primary buttons, links, focus
var(--accent-hover)    // Hover on accent elements
var(--accent-muted)    // Subtle accent (backgrounds)
```

### Status Colors
```less
var(--success)         // Green - positive actions
var(--success-muted)   // Light green background
var(--warning)         // Yellow/orange - caution
var(--warning-muted)   // Light warning background
var(--danger)          // Red - errors, destructive
var(--danger-muted)    // Light danger background
var(--info)            // Blue - informational
var(--info-muted)      // Light info background
```

### Borders & Shadows
```less
var(--border-color)    // Default border color
var(--shadow-sm)       // Subtle shadow
var(--shadow-md)       // Card shadow
var(--shadow-lg)       // Modal/dropdown shadow
```

## LESS Variables (Sizes & Spacing)

```less
// Font sizes
@font-size-xs: 0.75rem;    // 12px
@font-size-sm: 0.875rem;   // 14px
@font-size-base: 1rem;     // 16px
@font-size-lg: 1.125rem;   // 18px
@font-size-xl: 1.25rem;    // 20px
@font-size-2xl: 1.5rem;    // 24px
@font-size-3xl: 1.875rem;  // 30px

// Border radius
@radius-sm: 0.25rem;       // 4px
@radius-md: 0.5rem;        // 8px
@radius-lg: 0.75rem;       // 12px
@radius-xl: 1rem;          // 16px
@radius-full: 9999px;      // Pill shape

// Spacing (use with calc or directly)
@spacing-1: 0.25rem;       // 4px
@spacing-2: 0.5rem;        // 8px
@spacing-3: 0.75rem;       // 12px
@spacing-4: 1rem;          // 16px
@spacing-6: 1.5rem;        // 24px
@spacing-8: 2rem;          // 32px

// Breakpoints
@screen-sm: 640px;
@screen-md: 768px;
@screen-lg: 1024px;
@screen-xl: 1280px;
```

## Component Styling Pattern

### Basic Component

```less
// components/form.less

// MyInput component
.my-input-wrapper {
  margin-bottom: @spacing-4;
}

.my-input-label {
  display: block;
  font-size: @font-size-sm;
  color: var(--text-muted);
  margin-bottom: @spacing-2;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.my-input {
  width: 100%;
  padding: 0.625rem 0.875rem;
  border-radius: @radius-md;
  border: 1px solid var(--border-color);
  background: var(--bg-tertiary);
  color: var(--text-primary);
  font-size: @font-size-base;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;

  &::placeholder {
    color: var(--text-muted);
  }

  &:hover {
    border-color: var(--accent-primary);
  }

  &:focus {
    outline: none;
    border-color: var(--accent-primary);
    box-shadow: 0 0 0 3px var(--accent-muted);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}
```

### Size Variants

```less
.my-button {
  // Base styles
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  border-radius: @radius-md;
  transition: all 0.15s ease;
}

// Size modifiers
.my-button-sm {
  padding: 0.375rem 0.75rem;
  font-size: @font-size-sm;
}

.my-button-md {
  padding: 0.5rem 1rem;
  font-size: @font-size-base;
}

.my-button-lg {
  padding: 0.625rem 1.25rem;
  font-size: @font-size-lg;
}
```

### Color Variants

```less
.my-button {
  // Default/primary
  background: var(--accent-primary);
  color: var(--text-inverse);
  border: none;

  &:hover {
    background: var(--accent-hover);
  }
}

.my-button-secondary {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);

  &:hover {
    background: var(--bg-hover);
  }
}

.my-button-danger {
  background: var(--danger);
  color: white;

  &:hover {
    filter: brightness(1.1);
  }
}

.my-button-ghost {
  background: transparent;
  color: var(--text-secondary);

  &:hover {
    background: var(--bg-hover);
    color: var(--text-primary);
  }
}

.my-button-outline {
  background: transparent;
  color: var(--accent-primary);
  border: 1px solid var(--accent-primary);

  &:hover {
    background: var(--accent-muted);
  }
}
```

### Status States

```less
.my-alert {
  padding: @spacing-4;
  border-radius: @radius-md;
  border-left: 4px solid;
}

.my-alert-info {
  background: var(--info-muted);
  border-color: var(--info);
  color: var(--info);
}

.my-alert-success {
  background: var(--success-muted);
  border-color: var(--success);
  color: var(--success);
}

.my-alert-warning {
  background: var(--warning-muted);
  border-color: var(--warning);
  color: var(--warning);
}

.my-alert-error {
  background: var(--danger-muted);
  border-color: var(--danger);
  color: var(--danger);
}
```

## Common Patterns

### Card Container

```less
.my-card {
  background: var(--bg-secondary);
  border-radius: @radius-lg;
  padding: @spacing-6;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color);
}

.my-card-header {
  margin-bottom: @spacing-4;
  padding-bottom: @spacing-4;
  border-bottom: 1px solid var(--border-color);
}

.my-card-title {
  font-size: @font-size-lg;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}
```

### Interactive Element

```less
.my-interactive {
  cursor: pointer;
  transition: all 0.15s ease;

  &:hover {
    background: var(--bg-hover);
  }

  &:active {
    transform: scale(0.98);
  }

  &:focus-visible {
    outline: 2px solid var(--accent-primary);
    outline-offset: 2px;
  }

  &.disabled,
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
  }
}
```

### Flex Layout

```less
.my-row {
  display: flex;
  align-items: center;
  gap: @spacing-4;
}

.my-row-between {
  justify-content: space-between;
}

.my-row-center {
  justify-content: center;
}

.my-col {
  display: flex;
  flex-direction: column;
  gap: @spacing-4;
}
```

### Responsive Design

```less
.my-grid {
  display: grid;
  gap: @spacing-4;
  grid-template-columns: 1fr;

  @media (min-width: @screen-md) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (min-width: @screen-lg) {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

## Mixins

### Useful Mixins

```less
// mixins.less

.flex-center() {
  display: flex;
  align-items: center;
  justify-content: center;
}

.text-truncate() {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.focus-ring() {
  &:focus-visible {
    outline: 2px solid var(--accent-primary);
    outline-offset: 2px;
  }
}

.hover-lift() {
  transition: transform 0.15s ease, box-shadow 0.15s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
  }
}
```

### Using Mixins

```less
.my-card {
  .hover-lift();
  background: var(--bg-secondary);
  border-radius: @radius-lg;
}

.my-button {
  .flex-center();
  .focus-ring();
}
```

## Adding New Styles

### 1. Choose/Create File

```less
// For new category: components/my-category.less
// For existing: add to appropriate file
```

### 2. Import in index.less

```less
// styles/index.less
@import 'components/my-category.less';
```

### 3. Write Styles

```less
// Use BEM-ish naming: .component-element-modifier
.my-widget { }
.my-widget-header { }
.my-widget-body { }
.my-widget-sm { }
.my-widget-primary { }
```

### 4. Build

```bash
cd cacao/frontend && npm run build
```

## Checklist

- [ ] Uses CSS variables for colors (not hardcoded)
- [ ] Works in both dark and light themes
- [ ] Includes hover, focus, disabled states
- [ ] Uses LESS variables for sizes/spacing
- [ ] Follows naming convention
- [ ] Imported in index.less
- [ ] Rebuilt with `npm run build`
- [ ] Tested in browser

## Anti-Patterns

```less
// ❌ Don't hardcode colors
.my-widget {
  color: #ffffff;
  background: #1a1a2e;
}

// ✅ Do use CSS variables
.my-widget {
  color: var(--text-primary);
  background: var(--bg-secondary);
}

// ❌ Don't use magic numbers
.my-widget {
  padding: 13px 17px;
  font-size: 15px;
}

// ✅ Do use variables
.my-widget {
  padding: @spacing-3 @spacing-4;
  font-size: @font-size-base;
}

// ❌ Don't forget transitions
.my-button:hover {
  background: var(--accent-hover);
}

// ✅ Do add smooth transitions
.my-button {
  transition: background 0.15s ease;

  &:hover {
    background: var(--accent-hover);
  }
}
```
