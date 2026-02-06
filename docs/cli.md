# CLI Reference

Cacao provides a command-line interface for common development tasks.

## Installation

The CLI is installed automatically with Cacao:

```bash
pip install cacao
```

Verify installation:

```bash
cacao --help
```

## Commands

### `cacao create`

Create a new Cacao project from a template.

```bash
# Interactive mode
cacao create

# With project name
cacao create my-app

# With template selection
cacao create my-app --template counter
```

**Options:**

| Option | Description |
|--------|-------------|
| `name` | Project name (optional, interactive if omitted) |
| `-t, --template` | Template to use: `minimal`, `counter`, `dashboard` |
| `-v, --verbose` | Show detailed output |

**Templates:**

| Template | Description |
|----------|-------------|
| `minimal` | Bare-bones hello world app |
| `counter` | Interactive counter with state management |
| `dashboard` | Dashboard layout with sidebar navigation |

**Generated Structure:**

```
my-app/
├── app.py           # Main application
├── requirements.txt # Dependencies (cacao)
└── static/
    └── css/
        └── custom.css  # Custom styles
```

### `cacao dev`

Run a Cacao application with hot reload enabled.

```bash
# Basic usage
cacao dev app.py

# With options
cacao dev app.py --port 8080 --no-reload
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `app_file` | Path to the Python app file | Required |
| `--host` | Host to bind to | `localhost` |
| `--port` | HTTP server port | `1634` |
| `--ws-port` | WebSocket server port | `1633` |
| `--no-reload` | Disable hot reload | Hot reload enabled |
| `-v, --verbose` | Enable verbose logging | Off |

**Example:**

```bash
cacao dev examples/counter_example.py --port 8000 --verbose
```

### `cacao serve`

Run the development server (without specifying an app file).

```bash
cacao serve --port 8080 --verbose
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--host` | Host to bind the server to | `localhost` |
| `--port` | HTTP server port | `1634` |
| `--ws-port` | WebSocket server port | `1633` |
| `--pwa` | Enable Progressive Web App mode | Off |
| `-v, --verbose` | Enable verbose logging | Off |

### `cacao build-components`

Compile JavaScript components into `cacao-components.js`.

```bash
# Basic usage
cacao build-components

# With options
cacao build-components --force --verbose
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--components-dir` | Component source directory | `cacao/ui/components` |
| `--output` | Output file path | `cacao/core/static/js/cacao-components.js` |
| `--force` | Force rebuild even if files haven't changed | Off |
| `--verbose` | Show detailed compilation information | Off |

This command is typically run automatically, but you can run it manually after modifying JavaScript components.

## Common Workflows

### Starting a New Project

```bash
# Create project
cacao create my-app --template dashboard

# Enter project directory
cd my-app

# Install dependencies
pip install -r requirements.txt

# Start development server
cacao dev app.py
```

### Development Workflow

```bash
# Start dev server with hot reload
cacao dev app.py

# In another terminal, watch for component changes
cacao build-components --verbose
```

### Running Examples

```bash
# Clone the repo
git clone https://github.com/cacao-research/Cacao.git
cd Cacao

# Install in development mode
pip install -e .

# Run any example
cacao dev examples/counter_example.py
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `CACAO_DEBUG` | Enable debug mode (`1` or `true`) |
| `CACAO_HOST` | Default host for servers |
| `CACAO_PORT` | Default HTTP port |

## Configuration File

Create a `cacao.json` for project-specific settings:

```json
{
    "documentation": {
        "output_dir": "./docs",
        "formats": ["html", "md"]
    },
    "theme": {
        "css": "./static/css/custom.css"
    },
    "icons": {
        "icon_directories": ["./icons"],
        "fontawesome_version": "6.4.2"
    }
}
```

## Troubleshooting

### Command Not Found

If `cacao` command is not found:

1. Ensure Cacao is installed: `pip install cacao`
2. Check your PATH includes Python's scripts directory
3. Try: `python -m cacao.cli`

### Port Already in Use

```bash
# Use a different port
cacao dev app.py --port 8080
```

### Hot Reload Not Working

```bash
# Check if watchfiles is installed
pip install watchfiles

# Run without reload to diagnose
cacao dev app.py --no-reload --verbose
```

## Next Steps

- [Quickstart](getting-started/quickstart.md) - Get started with your first app
- [Examples](examples/index.md) - Browse example applications
