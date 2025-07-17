# Cacao Component Development Guide

## Overview

This guide covers the automated component compilation process in the Cacao framework and provides best practices for developing components that integrate seamlessly with the system.

## Component Compilation Architecture

### Two-Stage Loading Architecture

The Cacao framework uses a two-stage loading architecture:

1. **Stage 1**: [`cacao-core.js`](../cacao/core/static/js/cacao-core.js) - Defines core functions in the `window.CacaoCore` namespace
2. **Stage 2**: [`cacao-components.js`](../cacao/core/static/js/cacao-components.js) - Auto-generated component registrations

### Compilation Process

The [`ComponentCompiler`](../cacao/core/component_compiler.py) automatically:

1. **Discovers components** from the `cacao/ui/components/` directory
2. **Reads JavaScript files** from component directories
3. **Transforms function calls** to use proper namespacing
4. **Wraps components** with registration logic
5. **Generates output** to `cacao-components.js`

## Function Call Transformation

### The Problem (Resolved)

Previously, component JavaScript files contained direct function calls like:
```javascript
renderChildren(el, children);
applyContent(el, content);
renderComponent(component);
```

These caused runtime errors because the functions weren't properly namespaced.

### The Solution

The compilation system now **automatically transforms** these calls to:
```javascript
window.CacaoCore.renderChildren(el, children);
window.CacaoCore.applyContent(el, content);
window.CacaoCore.renderComponent(component);
```

### Supported Functions

The following CacaoCore functions are automatically transformed:
- `renderChildren()` → `window.CacaoCore.renderChildren()`
- `applyContent()` → `window.CacaoCore.applyContent()`
- `renderComponent()` → `window.CacaoCore.renderComponent()`

## Component Development Best Practices

### 1. Component Directory Structure

```
cacao/ui/components/
├── data/
│   ├── avatar/
│   │   ├── avatar.js        # Component JavaScript
│   │   ├── avatar.css       # Component styles
│   │   └── avatar.py        # Component Python class
│   └── card/
│       ├── card.js
│       ├── card.css
│       └── card.py
└── forms/
    ├── input/
    │   ├── input.js
    │   ├── input.css
    │   └── input.py
    └── ...
```

### 2. JavaScript Component Format

Components should be written as arrow functions that return DOM elements:

```javascript
// Good: Simple component structure
(component) => {
    const el = document.createElement("div");
    el.className = "my-component";
    
    // Use CacaoCore functions directly - they will be auto-transformed
    if (component.props?.content) {
        applyContent(el, component.props.content);
    }
    
    if (component.children) {
        renderChildren(el, component.children);
    }
    
    return el;
}
```

### 3. Function Call Guidelines

#### ✅ Recommended Approach
Write direct function calls - they will be automatically transformed:

```javascript
// These will be automatically transformed during compilation
renderChildren(el, component.children);
applyContent(el, component.props.content);
renderComponent(childComponent);
```

#### ✅ Alternative Approach
You can also use the full namespace explicitly:

```javascript
// These will not be transformed (already correct)
window.CacaoCore.renderChildren(el, component.children);
window.CacaoCore.applyContent(el, component.props.content);
window.CacaoCore.renderComponent(childComponent);
```

#### ❌ Avoid These Patterns

```javascript
// Method calls - will NOT be transformed
obj.renderChildren(el, children);
myObject.applyContent(el, content);

// Already namespaced calls - will NOT be double-transformed
window.CacaoCore.renderChildren(el, children);
```

### 4. Component Props and Children

Components receive a `component` object with:
- `component.props` - Component properties
- `component.children` - Child components
- `component.type` - Component type name

```javascript
(component) => {
    const el = document.createElement("div");
    
    // Handle props
    if (component.props?.className) {
        el.className = component.props.className;
    }
    
    if (component.props?.style) {
        Object.assign(el.style, component.props.style);
    }
    
    // Handle content
    if (component.props?.content) {
        applyContent(el, component.props.content);
    }
    
    // Handle children
    if (component.children) {
        renderChildren(el, component.children);
    } else if (component.props?.children) {
        renderChildren(el, component.props.children);
    }
    
    return el;
}
```

## Compilation Commands

### Manual Compilation

```bash
# Compile all components
python -c "from cacao.core.component_compiler import compile_components; compile_components()"

# Compile with verbose output
python -c "from cacao.core.component_compiler import compile_components; compile_components(verbose=True)"

# Force recompilation
python -c "from cacao.core.component_compiler import compile_components; compile_components(force=True)"
```

### Integration with Development

The compilation system integrates with:
- **Hot Reload**: Components are recompiled when files change
- **Error Handling**: Compilation errors don't break the app
- **CLI Integration**: Available via `cacao build-components` command

## Troubleshooting

### Common Issues

1. **Component Not Found**
   - Ensure component directory contains a `.js` file
   - Check that the file exports a function

2. **Function Not Defined Errors**
   - Recompile components: `compile_components(force=True)`
   - Check that `cacao-core.js` loads before `cacao-components.js`

3. **Compilation Warnings**
   - Review console output during compilation
   - Check for syntax errors in component JavaScript

### Debugging

Enable verbose compilation to see transformation details:

```python
from cacao.core.component_compiler import compile_components
compile_components(verbose=True)
```

This will show:
- Component discovery process
- Function call transformations
- Validation warnings
- Compilation success/failure

## Testing

### Running Component Tests

```bash
# Run component compiler tests
python test/test_component_compiler.py

# Run with pytest (if available)
pytest test/test_component_compiler.py -v
```

### Creating Component Tests

When creating new components, test them with:

```python
from cacao.core.component_compiler import ComponentCompiler

compiler = ComponentCompiler()
js_content = "your component code here"
result = compiler._transform_function_calls(js_content)
warnings = compiler._validate_function_calls(result, "component-name")
```

## Migration Guide

### From Legacy Components

If you have legacy components with direct function calls:

1. **No action needed** - The compilation system automatically transforms function calls
2. **Recompile** - Run `compile_components(force=True)` to regenerate
3. **Verify** - Check the generated `cacao-components.js` for proper namespacing

### Best Practices for New Components

1. Write components as arrow functions
2. Use direct CacaoCore function calls (they'll be auto-transformed)
3. Follow the standard directory structure
4. Test components individually before integration
5. Use the compilation system's validation features

## Advanced Usage

### Custom Compilation

```python
from cacao.core.component_compiler import ComponentCompiler

# Custom compiler instance
compiler = ComponentCompiler(
    components_dir="custom/components/path",
    output_path="custom/output/path.js"
)

# Compile with custom settings
success = compiler.compile(force=True, verbose=True)
```

### Adding New CacaoCore Functions

To add new functions to the transformation whitelist:

1. Update the `cacao_core_functions` list in `_transform_function_calls`
2. Add the function to the validation system
3. Update this documentation

## Summary

The Cacao component compilation system provides:

- **Automatic function transformation** for proper namespacing
- **Validation system** to catch common errors
- **Hot reload support** for development
- **Comprehensive testing** to ensure reliability

By following these guidelines, you can develop components that integrate seamlessly with the Cacao framework while avoiding common scope and namespacing issues.