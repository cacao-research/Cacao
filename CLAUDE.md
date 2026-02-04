# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Cacao is a high-performance reactive web framework for Python that enables building interactive dashboards, internal tools, and data applications. It uses WebSocket-driven real-time updates, JSON-defined UIs, and supports both web and desktop modes.

**Current Status:** Early development (v1.0.46-dev) - APIs subject to change.

## Common Commands

### Testing
```bash
# Run all tests
python test.py

# Run specific test files
python test.py test/test_state.py test/test_server.py

# Run tests matching pattern
python test.py -k "component"
```

### Component Compilation
```bash
# Compile components (auto-triggered on app startup)
python -c "from cacao.core.component_compiler import compile_components; compile_components()"

# Force recompilation with verbose output
python -c "from cacao.core.component_compiler import compile_components; compile_components(force=True, verbose=True)"
```

### Running Examples
```bash
# Web mode (default)
python examples/counter_example.py

# Desktop mode
python examples/simple_desktop_app.py
```

## Architecture

### Core Abstractions

- **`@mix` decorator** (`cacao/core/decorators.py`): Registers routes and event handlers. Routes stored in global `ROUTES` registry.
- **`State[T]`** (`cacao/core/state.py`): Generic reactive container with subscriber pattern. Changes auto-trigger UI updates via WebSocket.
- **`Component`** (`cacao/ui/components/base.py`): Abstract base for UI components. Each component has a `component_type` for state isolation.
- **`CacaoServer`** (`cacao/core/server.py`): Dual HTTP (port 1634) and WebSocket (port 1633) server with hot reload support.

### Data Flow

```
Python @mix route → JSON UI definition → WebSocket → Client renders
         ↑                                              ↓
    State.update() ←── Event handler ←── Client action
```

### Two-Stage JavaScript Loading

1. `cacao-core.js` loads first, defines `window.CacaoCore` namespace
2. `cacao-components.js` (auto-generated) registers component renderers

The `ComponentCompiler` auto-discovers components from `cacao/ui/components/` and transforms function calls like `renderChildren()` to `window.CacaoCore.renderChildren()`.

### Component Directory Structure

```
cacao/ui/components/data/{component_name}/
├── {component_name}.js   # Client-side renderer
├── {component_name}.css  # Styles
└── {component_name}.py   # Python class
```

### JSON UI Definition Pattern

Components return Python dicts that define UI structure:
```python
{
    "type": "div",
    "component_type": "unique-id",  # For state isolation
    "props": {
        "content": "text",
        "children": [...],
        "style": {...}
    }
}
```

## Code Conventions

- Type hints required for all Python code
- Google-style docstrings with Args/Returns/Raises
- UI components inherit from `cacao.ui.components.base.Component`
- State changes via `State.update()` or `State.set()` methods
- Event handlers use `@app.event("event_name")` or `@mix.event("event_name")`

## Windows Development

When running PowerShell commands, use semicolon (`;`) to separate commands, not `&&`.

## Key Files

- `cacao/core/app.py`: Main `App` class with `brew()` method for starting web/desktop
- `cacao/core/decorators.py`: `@mix` decorator, `ROUTES` and `EVENT_HANDLERS` registries
- `cacao/core/state.py`: `State` class, `GlobalStateManager` singleton
- `cacao/core/component_compiler.py`: Auto-compiles JS components on startup
- `cacao/desktop.py`: `CacaoDesktopApp` wrapper for pywebview
- `test/conftest.py`: Shared pytest fixtures
