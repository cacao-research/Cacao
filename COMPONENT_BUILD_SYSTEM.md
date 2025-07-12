# Cacao Component Build System

## Overview

The Cacao Component Build System uses a two-stage architecture for component integration. First, core components are registered statically in `cacao-core.js`. Then, additional modular components are compiled into a single `cacao-components.js` file, which is loaded after `cacao-core.js` at runtime. This system supports both modular components (with their own directories and `meta.json` files) and legacy components (hardcoded in `cacao-core.js`), allowing seamless extension and backward compatibility.

## Features

- **Automatic Compilation**: Components are compiled automatically when you call `app.brew()`
- **Smart Rebuilding**: Only rebuilds when component files have changed
- **Hybrid Support**: Works with both new modular components and existing legacy components
- **Zero Configuration**: Works out of the box with sensible defaults
- **Hot Reload Compatible**: Integrates seamlessly with Cacao's development workflow

## Two-Stage Loading Architecture

The component system uses a two-stage loading approach to ensure both static and dynamic components are available:

### Stage 1: Static Component Registration
1. **`cacao-core.js` loads first** and contains all legacy/static components in a `componentRenderers` object
2. **Global exposure**: The static components are exposed via `window.CacaoCore.componentRenderers`
3. **Immediate availability**: Core components like `descriptions`, `list`, `EnhancedTable`, etc. are ready for use

### Stage 2: Dynamic Component Extension
1. **`cacao-components.js` loads after** `cacao-core.js` has initialized
2. **Extension mechanism**: The compiled file extends `window.CacaoCore.componentRenderers` with additional components
3. **Auto-compilation**: New modular components are automatically compiled and added to this file
4. **Hot reload support**: Changes to component files trigger recompilation

### Loading Order
The correct loading sequence in [`index.html`](cacao/core/static/index.html:28-29) is:
```html
<script src="/static/js/cacao-core.js"></script>     <!-- Stage 1: Static components -->
<script src="/static/js/cacao-components.js"></script> <!-- Stage 2: Compiled components -->
```

## How It Works

### 1. Component Discovery

The system discovers components in two ways:

#### Modular Components
- Scans `cacao/ui/components/` for directories containing `meta.json` files
- Reads the JavaScript file path from each `meta.json`
- Example structure:
  ```
  cacao/ui/components/EnhancedTable/
  ├── meta.json
  ├── EnhancedTable.js
  ├── EnhancedTable.py
  └── EnhancedTable.css
  ```

#### Legacy Components
- Extracts existing component renderers from `cacao-core.js`
- Automatically converts them to the new modular format
- Avoids duplicates with modular components

### 2. Component Structure

#### meta.json Format
```json
{
    "name": "EnhancedTable",
    "py": "EnhancedTable.py",
    "js": "EnhancedTable.js",
    "css": "EnhancedTable.css"
}
```

#### Component JavaScript File Format
```javascript
// cacao/ui/components/EnhancedTable/EnhancedTable.js
(component) => {
    console.log("[CacaoCore] Rendering enhanced table component:", component);
    const wrapper = document.createElement("div");
    wrapper.className = "enhanced-table-wrapper";
    
    // Component rendering logic here
    
    return wrapper;
}
```

### 3. Compilation Process

1. **Discovery**: Find all modular components (legacy components are already in `cacao-core.js`)
2. **Reading**: Read JavaScript code from component files
3. **Wrapping**: Wrap each component with registration logic that extends `window.CacaoCore.componentRenderers`
4. **Combining**: Combine all components into a single file
5. **Output**: Write to `cacao/core/static/js/cacao-components.js`, which loads after `cacao-core.js`
6. **Integration**: The compiled file safely merges with existing static components at runtime

### 4. Generated Output

The compiled `cacao-components.js` file extends the static component registry:

```javascript
/*
 * Auto-generated Cacao Components
 * Generated on: 2025-01-09 23:27:00
 * Components: 5
 *
 * This file extends window.CacaoCore.componentRenderers with compiled components.
 * It must be loaded AFTER cacao-core.js to ensure the global registry exists.
 */

// Auto-generated component: EnhancedTable
(function() {
    // Ensure the global registry exists (defensive programming)
    if (!window.CacaoCore) {
        console.warn('[CacaoComponents] CacaoCore not found - ensure cacao-core.js loads first');
        window.CacaoCore = {};
    }
    if (!window.CacaoCore.componentRenderers) {
        window.CacaoCore.componentRenderers = {};
    }
    
    // Extend the existing registry with the new component
    window.CacaoCore.componentRenderers['enhancedtable'] = (component) => {
        console.log("[CacaoCore] Rendering enhanced table component:", component);
        const wrapper = document.createElement("div");
        wrapper.className = "enhanced-table-wrapper";
        
        // Component rendering logic here
        
        return wrapper;
    };
})();

// Additional compiled components follow the same pattern...
```

## Usage

> **Important**: The loading order in [`index.html`](cacao/core/static/index.html) must be: first `cacao-core.js`, then `cacao-components.js`. This ensures the global component registry is available for extension.

### Basic Usage

The component build system is enabled by default. Simply call `app.brew()`:

```python
import cacao

app = cacao.App()

@app.mix("/")
def home():
    return {
        "type": "EnhancedTable",
        "props": {
            "columns": [...],
            "dataSource": [...]
        }
    }

# Components are compiled automatically
app.brew()
```

### Disabling Component Compilation

If you want to disable automatic compilation:

```python
app.brew(compile_components=False)
```

### Manual Compilation

You can also compile components manually:

```python
from cacao.core.component_compiler import compile_components

# Compile with verbose output
compile_components(verbose=True)

# Force rebuild even if files haven't changed
compile_components(force=True)
```

## Creating New Components

### 1. Create Component Directory

```bash
mkdir cacao/ui/components/MyComponent
```

### 2. Create meta.json

```json
{
    "name": "MyComponent",
    "py": "MyComponent.py",
    "js": "MyComponent.js",
    "css": "MyComponent.css"
}
```

### 3. Create JavaScript File

```javascript
// cacao/ui/components/MyComponent/MyComponent.js
(component) => {
    const el = document.createElement("div");
    el.className = "my-component";
    
    // Add your component logic here
    if (component.props.content) {
        el.textContent = component.props.content;
    }
    
    return el;
}
```

### 4. Use in Your App

```python
@app.mix("/")
def home():
    return {
        "type": "myComponent",  # Note: lowercase
        "props": {
            "content": "Hello from MyComponent!"
        }
    }
```

## File Structure

```
cacao/
├── core/
│   ├── component_compiler.py    # Component compilation logic
│   ├── app.py                   # Integration with app.brew()
│   └── static/
│       ├── index.html           # Two-stage loading: cacao-core.js → cacao-components.js
│       └── js/
│           ├── cacao-core.js    # Stage 1: Static component registry
│           └── cacao-components.js  # Stage 2: Compiled component extensions
└── ui/
    └── components/
        └── EnhancedTable/       # Example modular component
            ├── meta.json
            ├── EnhancedTable.js
            ├── EnhancedTable.py
            └── EnhancedTable.css
```

## Performance

- **Smart Rebuilding**: Only rebuilds when component files change
- **Fast Compilation**: Typically completes in milliseconds
- **Minimal Overhead**: Adds negligible startup time
- **Caching**: Generated files are cached until source changes

## Troubleshooting

### Component Not Found

If a component isn't being discovered:

1. Check that `meta.json` exists and is valid JSON
2. Verify the JavaScript file path in `meta.json`
3. Ensure the component directory is under `cacao/ui/components/`

### Compilation Errors

Enable verbose output to see detailed error messages:

```python
app.brew(ASCII_debug=False)  # Shows emoji output with details
```

### Manual Debugging

Test the compilation manually:

```python
from cacao.core.component_compiler import ComponentCompiler

compiler = ComponentCompiler()
success = compiler.compile(verbose=True)
print(f"Compilation {'succeeded' if success else 'failed'}")
```

## Integration with Development Workflow

The component build system integrates seamlessly with Cacao's development workflow:

1. **Hot Reload**: Components are recompiled when files change
2. **Error Handling**: Compilation errors don't break the app
3. **Fallback**: If compilation fails, the app continues with existing components
4. **CLI Integration**: Available via `cacao build-components` command

## Migration from Legacy Components

The two-stage architecture ensures full backward compatibility:

### Legacy Component Support
- **Static components** in [`cacao-core.js`](cacao/core/static/js/cacao-core.js) remain fully functional
- **No breaking changes** to existing component registrations
- **Immediate availability** of legacy components at runtime

### Migrating to Modular Structure
To migrate legacy components to the new modular structure:

1. **Create component directory**: `mkdir cacao/ui/components/MyComponent`
2. **Extract component logic**: Move the renderer function to `MyComponent.js`
3. **Create meta.json**: Define component metadata
4. **Automatic compilation**: The build system compiles it into `cacao-components.js`
5. **Seamless integration**: The modular version extends the static registry

### Coexistence
- **Legacy and modular components work together** seamlessly
- **No conflicts**: Modular components can override legacy ones if needed
- **Gradual migration**: Move components at your own pace

## Best Practices

1. **Component Naming**: Use PascalCase for component names in `meta.json`
2. **File Organization**: Keep related files (JS, CSS, Python) in the same directory
3. **Error Handling**: Include proper error handling in component JavaScript
4. **Performance**: Avoid heavy computations in component renderers
5. **Testing**: Test components individually before integration

## Auto-Loading Mechanism

The `cacao-components.js` file is automatically loaded after `cacao-core.js` in the following scenarios:

### Automatic Compilation
- **On app startup**: When you call `app.brew()`, components are compiled if needed
- **File changes**: During development, file watchers trigger recompilation
- **Hot reload**: The browser automatically loads the updated compiled file

### Loading Sequence
1. **Browser loads** [`index.html`](cacao/core/static/index.html)
2. **Static components** are registered via `cacao-core.js`
3. **Compiled components** extend the registry via `cacao-components.js`
4. **All components** are now available for rendering

### Error Handling
- **Graceful fallback**: If compilation fails, static components remain available
- **Defensive programming**: The compiled file checks for `window.CacaoCore` existence
- **Console warnings**: Missing dependencies are logged for debugging

## Advanced Configuration

For advanced use cases, you can customize the component compiler:

```python
from cacao.core.component_compiler import ComponentCompiler

compiler = ComponentCompiler(
    components_dir="custom/components/path",
    output_path="custom/output/path.js"
)
compiler.compile()
```

## Summary

This two-stage component build system makes Cacao development more modular, maintainable, and scalable:

- **Preserves backward compatibility** with existing static components
- **Enables dynamic extension** through compiled modular components
- **Supports hot reload** for rapid development
- **Provides graceful fallbacks** when compilation fails
- **Maintains clean separation** between core and extended functionality

The architecture ensures that both legacy and modern component patterns work seamlessly together, allowing teams to migrate at their own pace while maintaining full functionality.