# Examples Gallery

Browse example Cacao applications to learn different patterns and techniques.

## Getting Started Examples

These examples demonstrate core Cacao concepts:

| Example | Description | Key Concepts |
|---------|-------------|--------------|
| [Counter](counter.md) | Interactive counter | State management, events |
| [Dashboard](dashboard.md) | Dashboard layout | Layouts, cards, navigation |
| [Data Tables](tables.md) | Table with filtering | Data components, forms |

## Running Examples

All examples are located in the `examples/` directory:

```bash
# Clone the repository
git clone https://github.com/cacao-research/Cacao.git
cd Cacao

# Install Cacao
pip install -e .

# Run an example
python examples/counter_example.py
```

Or use the `cacao dev` command:

```bash
cacao dev examples/counter_example.py
```

## Available Examples

### Basic

| File | Description |
|------|-------------|
| `simple_app_example.py` | Minimal hello world app |
| `counter_example.py` | Counter with state management |
| `theme_example.py` | Theming demonstration |

### Components

| File | Description |
|------|-------------|
| `components_showcase_example.py` | Showcase of built-in components |
| `icon_app_example.py` | Using the icon system |
| `range_sliders_example.py` | Slider input components |

### Layouts

| File | Description |
|------|-------------|
| `sidebar_layout_example.py` | Sidebar navigation layout |
| `standard_app_example.py` | Standard app structure |

### Data

| File | Description |
|------|-------------|
| `pandas_table_desktop_app.py` | Pandas DataFrame display |
| `pandas_table_with_filters_desktop_app.py` | Filtered data tables |

### Desktop

| File | Description |
|------|-------------|
| `simple_desktop_app.py` | Basic desktop application |

### Advanced

| File | Description |
|------|-------------|
| `react_component_example.py` | React component integration |
| `pwa_example.py` | Progressive Web App features |
| `custom_theme_example.py` | Custom theming |

## Creating Your Own

Use the CLI to scaffold a new project:

```bash
cacao create my-app
```

Choose from templates:

1. **Minimal** - Simple starting point
2. **Counter** - State management example
3. **Dashboard** - Full layout with navigation

## Project Structure

A typical Cacao project:

```
my-app/
├── app.py              # Main application
├── requirements.txt    # Dependencies
├── components/         # Custom components (optional)
│   └── my_component.py
├── static/
│   └── css/
│       └── custom.css  # Custom styles
└── cacao.json          # Configuration (optional)
```

## Contributing Examples

Have a great example? Contributions are welcome:

1. Fork the repository
2. Add your example to `examples/`
3. Update this gallery
4. Submit a pull request

See the [Contributing Guide](https://github.com/cacao-research/Cacao/blob/main/CONTRIBUTING.md) for details.
