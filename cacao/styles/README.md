# Cacao Styles

This directory contains the Less-based styling system for Cacao components.

## Setup

```bash
cd cacao/styles
npm install
```

## Commands

```bash
# Build CSS (outputs to ../core/static/css/cacao-components.css)
npm run build

# Build minified CSS
npm run build:min

# Watch for changes and rebuild
npm run dev
```

## Structure

```
styles/
├── main.less                 # Main entry point
├── tokens/
│   ├── _variables.less       # Design tokens (colors, spacing, etc.)
│   └── _mixins.less          # Reusable mixins
├── base/
│   ├── reset.less           # CSS reset
│   └── base.less            # Base styles
└── components/
    ├── data/                # Data display components
    ├── forms/               # Form components
    ├── navigation/          # Navigation components
    └── ui/                  # UI layout components
```

## Design Tokens

All design tokens are defined in `tokens/_variables.less`:

- **Colors**: `@cacao-primary`, `@cacao-success`, `@cacao-error`, etc.
- **Spacing**: `@space-1` (4px) through `@space-16` (64px)
- **Typography**: `@text-xs` through `@text-4xl`, `@font-bold`, etc.
- **Radius**: `@radius-sm`, `@radius-md`, `@radius-lg`, `@radius-full`
- **Shadows**: `@shadow-sm`, `@shadow`, `@shadow-md`, `@shadow-lg`
- **Transitions**: `@transition-fast`, `@transition`, `@transition-slow`

## Mixins

Common patterns are defined in `tokens/_mixins.less`:

- `.focus-ring()` - Standard focus outline
- `.transition()` - Default transition
- `.flex-center()` - Flexbox centering
- `.truncate()` - Text ellipsis
- `.button-base()` - Button styles
- `.input-base()` - Input styles
- `.card-base()` - Card styles
- `.custom-scrollbar()` - Styled scrollbar

## Adding a New Component

1. Create a new `.less` file in the appropriate `components/` subdirectory
2. Import the file in `main.less`
3. Use tokens and mixins for consistency:

```less
// components/data/my-component.less

.my-component {
  padding: @space-4;
  background-color: @cacao-surface;
  border: 1px solid @cacao-border;
  border-radius: @radius-md;
  .transition();

  &:hover {
    border-color: @cacao-primary;
  }

  &:focus {
    .focus-ring();
  }
}
```

## Theming

Users can override tokens by setting CSS custom properties. The compiled CSS also outputs CSS custom properties for runtime theming.
