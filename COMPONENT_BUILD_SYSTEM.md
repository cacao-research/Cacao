# Cacao Component Build System

## Overview

The Cacao Component Build System has been completely transformed to support modern, folder-based component discovery alongside the existing meta.json system. The new system automatically discovers components based on folder structure and naming conventions, eliminating the need for meta.json files while maintaining full backward compatibility.

The system uses a two-stage architecture: core components are registered statically in `cacao-core.js`, then additional components are compiled into `cacao-components.js` and loaded at runtime. This supports both the new folder-based components and legacy components, ensuring seamless extension and backward compatibility.

## Key Features

- **🆕 Folder-Based Discovery**: Automatically discovers components based on folder structure and naming conventions
- **🔄 Automatic Compilation**: Components are compiled automatically when you call `app.brew()`
- **⚡ Smart Rebuilding**: Only rebuilds when component files have changed
- **🔀 Hybrid Support**: Works with both new folder-based and legacy meta.json components
- **⚙️ Zero Configuration**: Works out of the box with sensible defaults
- **🔥 Hot Reload Compatible**: Integrates seamlessly with Cacao's development workflow
- **📊 High Performance**: Excellent discovery and compilation performance (0.025s discovery, 0.633s compilation for 51 components)
- **🎯 Multi-Level Categories**: Supports nested component organization

## New Component Structure (Recommended)

The new folder-based system organizes components using a clear, intuitive structure:

```
cacao/ui/components/category/component/
├── component.js    # JavaScript renderer (required)
├── component.css   # Component styles (optional)
└── component.py    # Python integration (optional)
```

### Folder Structure Examples

#### Single-Level Categories
```
cacao/ui/components/
├── data/
│   ├── table/
│   │   ├── table.js
│   │   ├── table.css
│   │   └── table.py
│   └── chart/
│       ├── chart.js
│       └── chart.css
├── forms/
│   ├── input/
│   │   ├── input.js
│   │   └── input.css
│   └── button/
│       ├── button.js
│       └── button.css
└── navigation/
    ├── navbar/
    │   ├── navbar.js
    │   └── navbar.css
    └── sidebar/
        ├── sidebar.js
        └── sidebar.css
```

#### Multi-Level Categories
```
cacao/ui/components/
├── data/
│   ├── display/
│   │   ├── table/
│   │   │   ├── table.js
│   │   │   └── table.css
│   │   └── list/
│   │       ├── list.js
│   │       └── list.css
│   └── input/
│       ├── form/
│       │   ├── form.js
│       │   └── form.css
│       └── field/
│           ├── field.js
│           └── field.css
```

### Component Naming Conventions

- **📁 Folder Names**: Use lowercase with hyphens for multi-word components (e.g., `data-table`)
- **📄 File Names**: Must be exactly `component.js`, `component.css`, `component.py` (all lowercase)
- **🎯 Component Names**: Derived from folder name, automatically converted to camelCase in registry
- **📂 Categories**: Derived from parent folder structure, support unlimited nesting

### File Requirements

| File | Required | Purpose |
|------|----------|---------|
| `component.js` | ✅ Yes | Component renderer function |
| `component.css` | ❌ Optional | Component-specific styles |
| `component.py` | ❌ Optional | Python integration/logic |

> **Note**: At least one file must be present for the component to be discovered. JavaScript file is recommended for most components.

## Component Creation Guide

### Step 1: Create Component Folder

Choose an appropriate category and create your component folder:

```bash
# For a data display component
mkdir -p cacao/ui/components/data/table

# For a form input component
mkdir -p cacao/ui/components/forms/input

# For a navigation component
mkdir -p cacao/ui/components/navigation/navbar

# For a multi-level category
mkdir -p cacao/ui/components/data/display/table
```

### Step 2: Create Component Files

#### JavaScript File (Required)
Create `component.js` with your renderer function:

```javascript
// cacao/ui/components/data/table/table.js
(component) => {
    console.log("[CacaoCore] Rendering table component:", component);
    
    const wrapper = document.createElement("div");
    wrapper.className = "cacao-table";
    
    // Create table structure
    const table = document.createElement("table");
    table.className = "table table-striped";
    
    // Add headers
    if (component.props.columns) {
        const thead = document.createElement("thead");
        const headerRow = document.createElement("tr");
        
        component.props.columns.forEach(col => {
            const th = document.createElement("th");
            th.textContent = col.title || col.key;
            headerRow.appendChild(th);
        });
        
        thead.appendChild(headerRow);
        table.appendChild(thead);
    }
    
    // Add data rows
    if (component.props.data) {
        const tbody = document.createElement("tbody");
        
        component.props.data.forEach(row => {
            const tr = document.createElement("tr");
            
            component.props.columns.forEach(col => {
                const td = document.createElement("td");
                td.textContent = row[col.key] || '';
                tr.appendChild(td);
            });
            
            tbody.appendChild(tr);
        });
        
        table.appendChild(tbody);
    }
    
    wrapper.appendChild(table);
    return wrapper;
}
```

#### CSS File (Optional)
Create `component.css` for styling:

```css
/* cacao/ui/components/data/table/table.css */
.cacao-table {
    width: 100%;
    margin: 1rem 0;
}

.cacao-table table {
    border-collapse: collapse;
    width: 100%;
}

.cacao-table th,
.cacao-table td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid #dee2e6;
}

.cacao-table th {
    background-color: #f8f9fa;
    font-weight: 600;
}

.cacao-table tr:hover {
    background-color: #f5f5f5;
}
```

#### Python File (Optional)
Create `component.py` for server-side logic:

```python
# cacao/ui/components/data/table/table.py
from typing import List, Dict, Any

class TableComponent:
    """Server-side logic for table component"""
    
    @staticmethod
    def process_data(data: List[Dict[str, Any]], columns: List[Dict[str, str]]) -> Dict[str, Any]:
        """Process table data before rendering"""
        # Add sorting, filtering, pagination logic here
        return {
            "data": data,
            "columns": columns,
            "total": len(data)
        }
    
    @staticmethod
    def validate_props(props: Dict[str, Any]) -> bool:
        """Validate component props"""
        required_props = ["data", "columns"]
        return all(prop in props for prop in required_props)
```

### Step 3: Use in Your Application

```python
import cacao

app = cacao.App()

@app.mix("/")
def home():
    return {
        "type": "table",  # Component name (folder name)
        "props": {
            "columns": [
                {"key": "name", "title": "Name"},
                {"key": "age", "title": "Age"},
                {"key": "city", "title": "City"}
            ],
            "data": [
                {"name": "John", "age": 30, "city": "New York"},
                {"name": "Jane", "age": 25, "city": "Los Angeles"},
                {"name": "Bob", "age": 35, "city": "Chicago"}
            ]
        }
    }

# Components are discovered and compiled automatically
app.brew()
```

## Component Discovery System

The new discovery system automatically finds and processes components without requiring configuration files:

### Discovery Process

1. **📂 Folder Scanning**: Walks through `cacao/ui/components/` directory recursively
2. **📝 File Detection**: Looks for `component.js`, `component.css`, and `component.py` files
3. **🏷️ Category Derivation**: Extracts category from folder path (e.g., `data/table` → category: `data`)
4. **📊 Component Registration**: Registers component with derived name and category
5. **🔄 Graceful Handling**: Continues processing even if some files are missing

### Category Derivation Examples

| Folder Path | Component Name | Category |
|-------------|----------------|----------|
| `data/table/` | `table` | `data` |
| `forms/input/` | `input` | `forms` |
| `navigation/navbar/` | `navbar` | `navigation` |
| `data/display/table/` | `table` | `data/display` |
| `forms/input/text/` | `text` | `forms/input` |

### Multi-Level Category Support

The system supports unlimited nesting:

```
cacao/ui/components/
├── ui/
│   ├── feedback/
│   │   ├── alert/          # Category: ui/feedback
│   │   ├── toast/          # Category: ui/feedback
│   │   └── modal/          # Category: ui/feedback
│   └── layout/
│       ├── grid/           # Category: ui/layout
│       ├── container/      # Category: ui/layout
│       └── responsive/
│           ├── breakpoint/ # Category: ui/layout/responsive
│           └── viewport/   # Category: ui/layout/responsive
```

### Missing File Handling

The system gracefully handles missing files:

- **Missing CSS**: Component works without styles
- **Missing Python**: Component works without server-side logic
- **Missing JavaScript**: Component skipped with warning
- **Empty Directories**: Ignored during discovery

## Updated ComponentCompiler Usage

### Basic Usage

The component compiler is automatically invoked when you call `app.brew()`:

```python
import cacao

app = cacao.App()

# Components are discovered and compiled automatically
app.brew()
```

### Manual Compilation

For more control, use the compiler directly:

```python
from cacao.core.component_compiler import ComponentCompiler

# Create compiler instance
compiler = ComponentCompiler()

# Discover components
components = compiler.discover_components()
print(f"Found {len(components)} components")

# Compile components
success = compiler.compile(verbose=True)
print(f"Compilation {'succeeded' if success else 'failed'}")
```

### Advanced Usage Examples

#### Force Rebuild
```python
# Force rebuild even if files haven't changed
compiler.compile(force=True)
```

#### Verbose Output
```python
# Enable detailed logging
compiler.compile(verbose=True)
```

#### Custom Paths
```python
# Use custom component directory
compiler = ComponentCompiler(
    components_dir="custom/components/path",
    output_dir="custom/output/path"
)
```

#### Discovery Only
```python
# Just discover components without compiling
components = compiler.discover_components()
for comp in components:
    print(f"Found: {comp['name']} (category: {comp.get('category', 'none')})")
```

### Performance Characteristics

Based on testing with 51 components:

- **Discovery Time**: ~0.025 seconds
- **Compilation Time**: ~0.633 seconds  
- **Total Time**: ~0.658 seconds
- **Memory Usage**: Minimal overhead
- **Cache Efficiency**: Only rebuilds when files change

### Debugging and Troubleshooting

#### Enable Debug Mode
```python
# Enable detailed debug output
app.brew(verbose=True)
```

#### Manual Testing
```python
from cacao.core.component_compiler import ComponentCompiler
import os

# Test component discovery
compiler = ComponentCompiler()
components = compiler.discover_components()

print(f"Found {len(components)} components:")
for comp in components:
    comp_type = 'folder-based' if 'category' in comp else 'meta.json'
    print(f"  • {comp['name']} ({comp_type})")
    if 'js_path' in comp:
        print(f"    JS: {comp['js_path']}")
    if 'css_path' in comp:
        print(f"    CSS: {comp['css_path']}")

# Test compilation
success = compiler.compile(force=True, verbose=True)
print(f"Compilation successful: {success}")

# Verify output files
js_output = 'cacao/core/static/js/cacao-components.js'
css_output = 'cacao/core/static/css/cacao-components.css'
print(f"JS output exists: {os.path.exists(js_output)}")
print(f"CSS output exists: {os.path.exists(css_output)}")
```

## Migration Guide

### From meta.json to Folder-Based Structure

The new system maintains full backward compatibility while encouraging migration to the cleaner folder-based approach.

#### Side-by-Side Comparison

| Aspect | Old System (meta.json) | New System (Folder-Based) |
|--------|------------------------|---------------------------|
| **Discovery** | Requires meta.json file | Automatic via folder structure |
| **Configuration** | Manual JSON configuration | Zero configuration |
| **Naming** | Defined in meta.json | Derived from folder name |
| **Categories** | Manual specification | Automatic from folder path |
| **File Structure** | Flexible, defined in JSON | Standardized naming convention |
| **Maintenance** | Manual updates to JSON | Automatic, self-documenting |

#### Old System Example
```
cacao/ui/components/MyComponent/
├── meta.json           # Required configuration
├── MyComponent.js      # Custom filename
├── MyComponent.css     # Custom filename
└── MyComponent.py      # Custom filename
```

```json
{
    "name": "MyComponent",
    "py": "MyComponent.py",
    "js": "MyComponent.js",
    "css": "MyComponent.css"
}
```

#### New System Example
```
cacao/ui/components/data/mycomponent/
├── component.js        # Standardized filename
├── component.css       # Standardized filename
└── component.py        # Standardized filename
```

No configuration file needed - everything is automatic!

#### Migration Steps

1. **Create New Folder Structure**
   ```bash
   # Choose appropriate category
   mkdir -p cacao/ui/components/data/mycomponent
   ```

2. **Move and Rename Files**
   ```bash
   # Move JavaScript file
   mv cacao/ui/components/MyComponent/MyComponent.js \
      cacao/ui/components/data/mycomponent/component.js
   
   # Move CSS file
   mv cacao/ui/components/MyComponent/MyComponent.css \
      cacao/ui/components/data/mycomponent/component.css
   
   # Move Python file
   mv cacao/ui/components/MyComponent/MyComponent.py \
      cacao/ui/components/data/mycomponent/component.py
   ```

3. **Remove meta.json**
   ```bash
   rm cacao/ui/components/MyComponent/meta.json
   ```

4. **Update Component References** (if needed)
   ```python
   # Old reference
   {"type": "MyComponent"}
   
   # New reference (usually unchanged)
   {"type": "mycomponent"}
   ```

5. **Test and Verify**
   ```python
   from cacao.core.component_compiler import ComponentCompiler
   
   compiler = ComponentCompiler()
   components = compiler.discover_components()
   
   # Verify your component is found
   component_names = [c['name'] for c in components]
   assert 'mycomponent' in component_names
   ```

### Backward Compatibility

Both systems work seamlessly together:

- **✅ Existing meta.json components continue to work**
- **✅ New folder-based components are automatically discovered**
- **✅ No breaking changes to existing applications**
- **✅ Gradual migration at your own pace**

### Deprecation Timeline

- **Current**: Both systems supported
- **Deprecation Warnings**: meta.json usage logs deprecation warnings
- **Future**: meta.json support will be removed in a future major version
- **Recommendation**: Migrate to folder-based structure for new components

## Two-Stage Loading Architecture

The component system maintains its two-stage loading approach to ensure both static and dynamic components are available:

### Stage 1: Static Component Registration
1. **`cacao-core.js` loads first** containing legacy/static components
2. **Global exposure** via `window.CacaoCore.componentRenderers`
3. **Immediate availability** of core components

### Stage 2: Dynamic Component Extension
1. **`cacao-components.js` loads after** core initialization
2. **Extension mechanism** extends the component registry
3. **Auto-compilation** from both folder-based and meta.json components
4. **Hot reload support** for development

### Loading Order
```html
<!-- In index.html -->
<script src="/static/js/cacao-core.js"></script>     <!-- Stage 1 -->
<script src="/static/js/cacao-components.js"></script> <!-- Stage 2 -->
```

## Examples and Best Practices

### Real-World Component Examples

#### Data Display Components
```
cacao/ui/components/data/
├── table/
│   ├── component.js    # Sortable, filterable table
│   ├── component.css   # Table styling
│   └── component.py    # Data processing
├── chart/
│   ├── component.js    # Chart rendering
│   └── component.css   # Chart styles
└── list/
    ├── component.js    # Dynamic list
    └── component.css   # List styling
```

#### Form Components
```
cacao/ui/components/forms/
├── input/
│   ├── text/
│   │   ├── component.js
│   │   └── component.css
│   ├── email/
│   │   ├── component.js
│   │   └── component.css
│   └── password/
│       ├── component.js
│       └── component.css
├── button/
│   ├── component.js
│   └── component.css
└── validation/
    ├── component.js
    └── component.css
```

#### Navigation Components
```
cacao/ui/components/navigation/
├── navbar/
│   ├── component.js
│   └── component.css
├── sidebar/
│   ├── component.js
│   └── component.css
├── breadcrumb/
│   ├── component.js
│   └── component.css
└── pagination/
    ├── component.js
    └── component.css
```

### Organization Best Practices

1. **📁 Logical Grouping**: Group related components by functionality
2. **🏷️ Consistent Naming**: Use clear, descriptive folder names
3. **📊 Category Hierarchy**: Use nested categories for complex applications
4. **🔄 Reusable Components**: Create generic components that can be styled differently
5. **📝 Documentation**: Include comments in component files

### Common Pitfalls and Solutions

#### Pitfall 1: Incorrect File Naming
```bash
# ❌ Wrong
cacao/ui/components/data/table/Table.js    # Capital T
cacao/ui/components/data/table/table.JS    # Capital extension

# ✅ Correct
cacao/ui/components/data/table/component.js
```

#### Pitfall 2: Missing Required Files
```bash
# ❌ Wrong - no JavaScript file
cacao/ui/components/data/table/
├── component.css
└── component.py

# ✅ Correct - at least JavaScript file
cacao/ui/components/data/table/
├── component.js
├── component.css
└── component.py
```

#### Pitfall 3: Overly Nested Categories
```bash
# ❌ Avoid excessive nesting
cacao/ui/components/data/display/table/advanced/sortable/filterable/

# ✅ Keep it reasonable
cacao/ui/components/data/table/
```

### Performance Optimization Tips

1. **🚀 Lazy Loading**: Load components only when needed
2. **📦 Component Bundling**: Group related components together
3. **🗜️ Minification**: Minify JavaScript and CSS in production
4. **💾 Caching**: Leverage browser caching for compiled components
5. **📊 Profiling**: Monitor component discovery and compilation times

## File Structure Overview

```
cacao/
├── core/
│   ├── component_compiler.py    # New folder-based discovery logic
│   ├── app.py                   # Integration with app.brew()
│   └── static/
│       ├── index.html           # Two-stage loading
│       ├── js/
│       │   ├── cacao-core.js    # Stage 1: Static components
│       │   └── cacao-components.js  # Stage 2: Compiled components
│       └── css/
│           └── cacao-components.css # Compiled component styles
└── ui/
    └── components/
        ├── data/                # Data display components
        │   ├── table/
        │   │   ├── component.js
        │   │   ├── component.css
        │   │   └── component.py
        │   └── chart/
        │       ├── component.js
        │       └── component.css
        ├── forms/               # Form components
        │   ├── input/
        │   │   ├── component.js
        │   │   └── component.css
        │   └── button/
        │       ├── component.js
        │       └── component.css
        ├── navigation/          # Navigation components
        │   ├── navbar/
        │   │   ├── component.js
        │   │   └── component.css
        │   └── sidebar/
        │       ├── component.js
        │       └── component.css
        └── legacy/              # Legacy meta.json components
            └── OldComponent/
                ├── meta.json
                ├── OldComponent.js
                └── OldComponent.css
```

## Compilation Process

The updated compilation process handles both folder-based and meta.json components:

1. **🔍 Discovery Phase**:
   - Scan for folder-based components (new system)
   - Scan for meta.json components (legacy system)
   - Merge component lists, prioritizing folder-based

2. **📝 Processing Phase**:
   - Read JavaScript files from discovered components
   - Process CSS files for compilation
   - Validate component structure and files

3. **🔧 Compilation Phase**:
   - Wrap JavaScript components with registry logic
   - Combine all JavaScript into single file
   - Compile CSS into separate stylesheet

4. **📤 Output Phase**:
   - Write `cacao-components.js` with all compiled components
   - Write `cacao-components.css` with all styles
   - Update modification timestamps for caching

## Integration with Development Workflow

The component build system integrates seamlessly with Cacao's development workflow:

### Hot Reload Support
- **🔄 File Watching**: Components recompiled when files change
- **⚡ Fast Rebuilds**: Only changed components are reprocessed
- **🔥 Browser Refresh**: Automatically loads updated components

### Error Handling
- **🛡️ Graceful Fallback**: Compilation errors don't break the app
- **📊 Detailed Logging**: Verbose mode shows compilation details
- **🔍 Debug Information**: Clear error messages for troubleshooting

### CLI Integration
```bash
# Manual component compilation
cacao build-components

# Verbose compilation
cacao build-components --verbose

# Force rebuild
cacao build-components --force
```

## Advanced Configuration

### Custom Component Directory
```python
from cacao.core.component_compiler import ComponentCompiler

# Use custom component directory
compiler = ComponentCompiler(
    components_dir="my_custom_components",
    output_dir="static/compiled"
)
```

### Custom File Patterns
```python
# Future: Support for custom file patterns
compiler = ComponentCompiler(
    js_pattern="*.component.js",
    css_pattern="*.component.css",
    py_pattern="*.component.py"
)
```

## Troubleshooting

### Component Not Found

**For folder-based components:**
1. ✅ Check folder structure follows `category/component/` pattern
2. ✅ Verify `component.js` exists (required)
3. ✅ Ensure component directory is under `cacao/ui/components/`
4. ✅ Check file names are exactly `component.js`, `component.css`, `component.py`

**For meta.json components:**
1. ✅ Check `meta.json` exists and is valid JSON
2. ✅ Verify JavaScript file path in `meta.json`
3. ✅ Ensure component directory is under `cacao/ui/components/`

### Compilation Errors

Enable verbose output for detailed error messages:

```python
# Verbose app startup
app.brew(verbose=True)

# Verbose manual compilation
from cacao.core.component_compiler import ComponentCompiler
compiler = ComponentCompiler()
compiler.compile(verbose=True)
```

### Discovery Issues

Debug component discovery:

```python
from cacao.core.component_compiler import ComponentCompiler

compiler = ComponentCompiler()
components = compiler.discover_components()

print(f"Found {len(components)} components:")
for comp in components:
    comp_type = 'folder-based' if 'category' in comp else 'meta.json'
    print(f"  • {comp['name']} ({comp_type})")
    if 'category' in comp:
        print(f"    Category: {comp['category']}")
    if 'js_path' in comp:
        print(f"    JS: {comp['js_path']}")
    if 'css_path' in comp:
        print(f"    CSS: {comp['css_path']}")
```

### Performance Issues

Monitor compilation performance:

```python
import time
from cacao.core.component_compiler import ComponentCompiler

compiler = ComponentCompiler()

# Time discovery
start_time = time.time()
components = compiler.discover_components()
discovery_time = time.time() - start_time

# Time compilation
start_time = time.time()
success = compiler.compile(verbose=True)
compilation_time = time.time() - start_time

print(f"Discovery: {discovery_time:.3f}s")
print(f"Compilation: {compilation_time:.3f}s")
print(f"Total: {discovery_time + compilation_time:.3f}s")
```

## Summary

The enhanced Cacao Component Build System provides a modern, intuitive way to organize and build components while maintaining full backward compatibility:

### Key Benefits

- **🆕 Modern Structure**: Folder-based organization replaces complex meta.json configuration
- **⚡ Zero Configuration**: Components discovered automatically based on folder structure
- **🔄 Backward Compatible**: Existing meta.json components continue to work seamlessly
- **📊 High Performance**: Excellent discovery and compilation performance
- **🎯 Developer Friendly**: Clear conventions and self-documenting structure
- **🔧 Flexible**: Supports both simple and complex component hierarchies

### Migration Path

1. **Immediate**: Start using folder-based structure for new components
2. **Gradual**: Migrate existing components at your own pace
3. **Future-Proof**: Folder-based structure is the long-term direction

### Best Practices Summary

- Use folder-based structure for new components
- Follow naming conventions: `component.js`, `component.css`, `component.py`
- Organize components by logical categories
- Include at least a JavaScript file for each component
- Test component discovery and compilation regularly
- Monitor performance in large applications

The architecture ensures that both legacy and modern component patterns work seamlessly together, providing a smooth upgrade path while enabling more maintainable and scalable component development.