"""
Cacao Extension System.

Provides the SDK for building custom components, installing community
extensions, theme marketplace, and handler plugins for static builds.

Extensions follow a naming convention: ``cacao-<name>`` on PyPI, with
a ``cacao_extensions`` entry point group that exposes a ``register``
callable.

Example extension package (setup.cfg / pyproject.toml):

    [options.entry_points]
    cacao_extensions =
        my_ext = my_cacao_ext:register

The ``register`` callable receives the Cacao plugin instance::

    def register(plugin):
        plugin.on("on_ready", lambda: print("Extension loaded!"))
"""

from __future__ import annotations

import importlib
import json
import logging
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger("cacao.extensions")

# Entry point group used by extension packages
ENTRY_POINT_GROUP = "cacao_extensions"

# Directory for cached extension metadata
_EXTENSIONS_DIR = Path.home() / ".cacao" / "extensions"

# ============================================================================
# Custom Component SDK
# ============================================================================


@dataclass
class ComponentSpec:
    """Specification for a custom React component usable from Python.

    This is the core SDK class for extension authors who want to create
    custom UI components.

    Args:
        name: Component type name (PascalCase, e.g. ``"ColorPicker"``)
        js_code: JavaScript source for the React component. The code
            must export a function with the same name as *name*.
        css_code: Optional LESS/CSS styles for the component.
        props_schema: Optional dict describing accepted props (for
            validation and documentation).
        category: Component category (``"form"``, ``"display"``, etc.)
        description: Human-readable description shown in docs.

    Example::

        spec = ComponentSpec(
            name="ColorPicker",
            js_code='''
                export function ColorPicker({ value, onChange, ...props }) {
                    return React.createElement("input", {
                        type: "color",
                        value: value || "#000000",
                        onChange: (e) => onChange && onChange(e.target.value),
                        ...props,
                    });
                }
            ''',
            css_code=".cacao-color-picker { border: none; cursor: pointer; }",
            props_schema={"value": "string", "on_change": "event"},
            category="form",
            description="A color picker input.",
        )
    """

    name: str
    js_code: str
    css_code: str = ""
    props_schema: dict[str, str] = field(default_factory=dict)
    category: str = "custom"
    description: str = ""

    def validate(self) -> list[str]:
        """Return a list of validation errors (empty if valid)."""
        errors: list[str] = []
        if not self.name or not self.name[0].isupper():
            errors.append("Component name must be PascalCase (e.g. 'ColorPicker')")
        if not self.js_code.strip():
            errors.append("js_code must contain the React component source")
        if "export" not in self.js_code and "function" not in self.js_code:
            errors.append("js_code should export a named function matching the component name")
        return errors


# Global registry of custom component specs
_custom_components: dict[str, ComponentSpec] = {}


def register_component(spec: ComponentSpec) -> None:
    """Register a custom component so it can be used from Python.

    After registration, the component is available via
    ``c.custom("<Name>", prop=value)`` in the simple API, or via
    ``custom_component("<Name>", prop=value)`` in ``server.ui``.

    Args:
        spec: A :class:`ComponentSpec` instance.

    Raises:
        ValueError: If the spec fails validation.
    """
    errors = spec.validate()
    if errors:
        raise ValueError(f"Invalid ComponentSpec: {'; '.join(errors)}")
    _custom_components[spec.name] = spec
    logger.info("Custom component registered: %s", spec.name)


def get_custom_component(name: str) -> ComponentSpec | None:
    """Look up a registered custom component by name."""
    return _custom_components.get(name)


def get_all_custom_components() -> dict[str, ComponentSpec]:
    """Return all registered custom components."""
    return dict(_custom_components)


# ============================================================================
# Extension Discovery & Installation
# ============================================================================


@dataclass
class ExtensionInfo:
    """Metadata about an installed or available extension."""

    name: str
    version: str = "0.0.0"
    description: str = ""
    author: str = ""
    installed: bool = False
    entry_point: str = ""


def discover_extensions() -> dict[str, ExtensionInfo]:
    """Discover installed extensions via ``cacao_extensions`` entry points.

    Scans ``importlib.metadata`` for packages that declare the
    ``cacao_extensions`` entry point group.
    """
    from importlib.metadata import entry_points

    extensions: dict[str, ExtensionInfo] = {}

    try:
        eps = entry_points(group=ENTRY_POINT_GROUP)
    except TypeError:
        # Python < 3.12 fallback
        eps = entry_points().get(ENTRY_POINT_GROUP, [])  # type: ignore[assignment]

    for ep in eps:
        try:
            dist = ep.dist
            extensions[ep.name] = ExtensionInfo(
                name=ep.name,
                version=str(dist.version) if dist else "0.0.0",
                description=(dist.metadata.get("Summary", "") if dist else ""),
                author=(dist.metadata.get("Author", "") if dist else ""),
                installed=True,
                entry_point=f"{ep.value}",
            )
        except Exception:
            logger.warning("Failed to read extension entry point: %s", ep.name)

    return extensions


def load_extensions() -> list[str]:
    """Load all discovered extensions, calling their ``register`` functions.

    Returns a list of successfully loaded extension names.
    """
    from .server.plugin import get_registry

    loaded: list[str] = []
    extensions = discover_extensions()

    for ext_name, info in extensions.items():
        try:
            from importlib.metadata import entry_points

            try:
                eps = entry_points(group=ENTRY_POINT_GROUP)
            except TypeError:
                eps = entry_points().get(ENTRY_POINT_GROUP, [])  # type: ignore[assignment]

            for ep in eps:
                if ep.name == ext_name:
                    register_fn = ep.load()
                    # Create a plugin for this extension
                    plugin = get_registry().register(
                        ext_name,
                        version=info.version,
                        description=info.description,
                        author=info.author,
                        extension=True,
                    )
                    register_fn(plugin)
                    loaded.append(ext_name)
                    logger.info("Extension loaded: %s v%s", ext_name, info.version)
                    break
        except Exception:
            logger.exception("Failed to load extension: %s", ext_name)

    return loaded


def install_extension(name: str, *, upgrade: bool = False) -> bool:
    """Install an extension package from PyPI.

    The package name is normalized: if *name* doesn't start with
    ``cacao-``, the prefix is added automatically.

    Args:
        name: Extension name or PyPI package name.
        upgrade: If ``True``, upgrade if already installed.

    Returns:
        ``True`` if installation succeeded.
    """
    # Normalize package name
    pkg = name if name.startswith("cacao-") else f"cacao-{name}"

    cmd = [sys.executable, "-m", "pip", "install"]
    if upgrade:
        cmd.append("--upgrade")
    cmd.append(pkg)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            logger.info("Installed extension: %s", pkg)
            return True
        logger.error("pip install failed: %s", result.stderr.strip())
        return False
    except Exception:
        logger.exception("Failed to install extension: %s", pkg)
        return False


def uninstall_extension(name: str) -> bool:
    """Uninstall an extension package.

    Args:
        name: Extension name or PyPI package name.

    Returns:
        ``True`` if uninstallation succeeded.
    """
    pkg = name if name.startswith("cacao-") else f"cacao-{name}"

    cmd = [sys.executable, "-m", "pip", "uninstall", "-y", pkg]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            logger.info("Uninstalled extension: %s", pkg)
            return True
        logger.error("pip uninstall failed: %s", result.stderr.strip())
        return False
    except Exception:
        logger.exception("Failed to uninstall extension: %s", pkg)
        return False


# ============================================================================
# Theme Marketplace
# ============================================================================

# Built-in community themes registry (name -> theme definition)
_theme_registry: dict[str, dict[str, Any]] = {}


@dataclass
class ThemeDefinition:
    """A theme available in the marketplace."""

    name: str
    display_name: str
    author: str = ""
    description: str = ""
    variables: dict[str, str] = field(default_factory=dict)
    preview_colors: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    package: str = ""  # PyPI package if external


# Built-in community themes that ship with Cacao
BUILTIN_THEMES: list[ThemeDefinition] = [
    ThemeDefinition(
        name="ocean",
        display_name="Ocean",
        author="Cacao",
        description="Cool blue tones inspired by deep ocean waters",
        variables={
            "bg-primary": "#0a1628",
            "bg-secondary": "#112240",
            "bg-tertiary": "#1a3354",
            "text-primary": "#e0f7fa",
            "text-secondary": "#b0bec5",
            "accent-primary": "#4fc3f7",
            "accent-secondary": "#0288d1",
            "success": "#26a69a",
            "danger": "#ef5350",
            "warning": "#ffa726",
            "chart-1": "#4fc3f7",
            "chart-2": "#0288d1",
            "chart-3": "#26a69a",
            "chart-4": "#7e57c2",
            "chart-5": "#ffa726",
            "chart-6": "#ef5350",
        },
        preview_colors=["#0a1628", "#4fc3f7", "#26a69a"],
        tags=["dark", "cool", "blue"],
    ),
    ThemeDefinition(
        name="forest",
        display_name="Forest",
        author="Cacao",
        description="Rich green tones inspired by lush forests",
        variables={
            "bg-primary": "#1a2e1a",
            "bg-secondary": "#243524",
            "bg-tertiary": "#2e3e2e",
            "text-primary": "#e8f5e9",
            "text-secondary": "#a5d6a7",
            "accent-primary": "#66bb6a",
            "accent-secondary": "#2e7d32",
            "success": "#4caf50",
            "danger": "#e57373",
            "warning": "#ffb74d",
            "chart-1": "#66bb6a",
            "chart-2": "#2e7d32",
            "chart-3": "#8bc34a",
            "chart-4": "#4db6ac",
            "chart-5": "#ffb74d",
            "chart-6": "#e57373",
        },
        preview_colors=["#1a2e1a", "#66bb6a", "#4caf50"],
        tags=["dark", "green", "natural"],
    ),
    ThemeDefinition(
        name="sunset",
        display_name="Sunset",
        author="Cacao",
        description="Warm amber and orange tones like a golden sunset",
        variables={
            "bg-primary": "#2d1b00",
            "bg-secondary": "#3e2723",
            "bg-tertiary": "#4e342e",
            "text-primary": "#fff3e0",
            "text-secondary": "#ffcc80",
            "accent-primary": "#ff9800",
            "accent-secondary": "#e65100",
            "success": "#66bb6a",
            "danger": "#ef5350",
            "warning": "#ffca28",
            "chart-1": "#ff9800",
            "chart-2": "#e65100",
            "chart-3": "#ff5722",
            "chart-4": "#ffca28",
            "chart-5": "#66bb6a",
            "chart-6": "#ab47bc",
        },
        preview_colors=["#2d1b00", "#ff9800", "#e65100"],
        tags=["dark", "warm", "orange"],
    ),
    ThemeDefinition(
        name="lavender",
        display_name="Lavender",
        author="Cacao",
        description="Soft purple tones for a calming interface",
        variables={
            "bg-primary": "#f3e5f5",
            "bg-secondary": "#e1bee7",
            "bg-tertiary": "#ce93d8",
            "text-primary": "#311b92",
            "text-secondary": "#4a148c",
            "accent-primary": "#7e57c2",
            "accent-secondary": "#512da8",
            "success": "#66bb6a",
            "danger": "#e57373",
            "warning": "#ffb74d",
            "chart-1": "#7e57c2",
            "chart-2": "#512da8",
            "chart-3": "#ab47bc",
            "chart-4": "#5c6bc0",
            "chart-5": "#26a69a",
            "chart-6": "#ef5350",
        },
        preview_colors=["#f3e5f5", "#7e57c2", "#512da8"],
        tags=["light", "purple", "calm"],
    ),
    ThemeDefinition(
        name="midnight",
        display_name="Midnight",
        author="Cacao",
        description="Deep dark theme with neon accents for night owls",
        variables={
            "bg-primary": "#0d0d0d",
            "bg-secondary": "#1a1a1a",
            "bg-tertiary": "#262626",
            "text-primary": "#e0e0e0",
            "text-secondary": "#9e9e9e",
            "accent-primary": "#00e5ff",
            "accent-secondary": "#651fff",
            "success": "#00e676",
            "danger": "#ff1744",
            "warning": "#ffc400",
            "chart-1": "#00e5ff",
            "chart-2": "#651fff",
            "chart-3": "#00e676",
            "chart-4": "#ff1744",
            "chart-5": "#ffc400",
            "chart-6": "#ff9100",
        },
        preview_colors=["#0d0d0d", "#00e5ff", "#651fff"],
        tags=["dark", "neon", "contrast"],
    ),
    ThemeDefinition(
        name="paper",
        display_name="Paper",
        author="Cacao",
        description="Clean, minimal light theme resembling printed paper",
        variables={
            "bg-primary": "#fafafa",
            "bg-secondary": "#f5f5f5",
            "bg-tertiary": "#eeeeee",
            "text-primary": "#212121",
            "text-secondary": "#616161",
            "accent-primary": "#1565c0",
            "accent-secondary": "#0d47a1",
            "success": "#2e7d32",
            "danger": "#c62828",
            "warning": "#f57f17",
            "chart-1": "#1565c0",
            "chart-2": "#0d47a1",
            "chart-3": "#2e7d32",
            "chart-4": "#c62828",
            "chart-5": "#f57f17",
            "chart-6": "#6a1b9a",
        },
        preview_colors=["#fafafa", "#1565c0", "#2e7d32"],
        tags=["light", "minimal", "clean"],
    ),
]


def get_marketplace_themes() -> list[ThemeDefinition]:
    """Return all themes available in the marketplace.

    Combines built-in community themes with any themes registered by
    installed extensions.
    """
    themes = list(BUILTIN_THEMES)

    # Add themes registered by extensions
    for name, data in _theme_registry.items():
        if not any(t.name == name for t in themes):
            themes.append(
                ThemeDefinition(
                    name=data.get("name", name),
                    display_name=data.get("display_name", name.title()),
                    author=data.get("author", ""),
                    description=data.get("description", ""),
                    variables=data.get("variables", {}),
                    preview_colors=data.get("preview_colors", []),
                    tags=data.get("tags", []),
                    package=data.get("package", ""),
                )
            )

    return themes


def register_marketplace_theme(definition: ThemeDefinition) -> None:
    """Register a theme in the marketplace (used by extensions)."""
    _theme_registry[definition.name] = {
        "name": definition.name,
        "display_name": definition.display_name,
        "author": definition.author,
        "description": definition.description,
        "variables": definition.variables,
        "preview_colors": definition.preview_colors,
        "tags": definition.tags,
        "package": definition.package,
    }
    logger.info("Marketplace theme registered: %s", definition.name)


def install_theme(name: str) -> bool:
    """Install a theme from the marketplace.

    For built-in themes, this registers them with the app's theme system.
    For external themes (from extensions), this installs the package first.

    Args:
        name: Theme name.

    Returns:
        ``True`` if the theme was installed/registered.
    """
    # Check built-in themes first
    for theme in BUILTIN_THEMES:
        if theme.name == name:
            return True  # Already available, just needs c.config(theme=name)

    # Check extension-registered themes
    if name in _theme_registry:
        pkg = _theme_registry[name].get("package", "")
        if pkg:
            return install_extension(pkg)
        return True

    # Try installing as a cacao-theme-<name> package
    return install_extension(f"theme-{name}")


def search_themes(query: str = "", tags: list[str] | None = None) -> list[ThemeDefinition]:
    """Search marketplace themes by query string or tags.

    Args:
        query: Search string matched against name, description, author.
        tags: Filter by tags (e.g. ``["dark", "blue"]``).

    Returns:
        List of matching themes.
    """
    themes = get_marketplace_themes()
    results: list[ThemeDefinition] = []

    for theme in themes:
        # Tag filter
        if tags and not any(t in theme.tags for t in tags):
            continue

        # Query filter
        if query:
            q = query.lower()
            searchable = f"{theme.name} {theme.display_name} {theme.description} {theme.author}".lower()
            if q not in searchable:
                continue

        results.append(theme)

    return results


# ============================================================================
# Handler Plugins for Static Builds
# ============================================================================

# Registry of handler plugins: name -> dict with js_code and metadata
_handler_plugins: dict[str, dict[str, Any]] = {}


def register_handler_plugin(
    name: str,
    handlers: dict[str, str],
    *,
    description: str = "",
    author: str = "",
) -> None:
    """Register a handler plugin for static builds.

    Handler plugins provide client-side JavaScript functions that run
    in static builds (no Python server). They extend the built-in
    handlers (encoders, generators, converters, text, crypto).

    Args:
        name: Plugin name (e.g. ``"image-tools"``).
        handlers: Dict mapping handler names to JS function expressions.
            Each value should be an async function expression::

                async function(signals, event) { ... }

        description: Human-readable description.
        author: Plugin author.

    Example::

        c.register_handler_plugin("image-tools", {
            "resize_image": '''async function(signals, event) {
                const img = signals.get("image");
                // ... resize logic ...
                signals.set("resized", result);
            }''',
            "crop_image": '''async function(signals, event) {
                // ... crop logic ...
            }''',
        }, description="Image manipulation handlers")
    """
    _handler_plugins[name] = {
        "handlers": handlers,
        "description": description,
        "author": author,
    }
    logger.info(
        "Handler plugin registered: %s (%d handlers)",
        name,
        len(handlers),
    )


def get_handler_plugins() -> dict[str, dict[str, Any]]:
    """Return all registered handler plugins."""
    return dict(_handler_plugins)


def get_all_static_handlers() -> dict[str, str]:
    """Return a merged dict of all handler plugin handlers.

    Combines handlers from all registered plugins into a single flat
    dict of event_name -> js_function.
    """
    merged: dict[str, str] = {}
    for plugin_data in _handler_plugins.values():
        merged.update(plugin_data.get("handlers", {}))
    return merged


# ============================================================================
# SDK Utilities
# ============================================================================


def create_extension_template(name: str, output_dir: str | Path | None = None) -> Path:
    """Generate a starter template for a new Cacao extension.

    Creates a directory with the boilerplate needed to publish a
    Cacao extension on PyPI.

    Args:
        name: Extension name (e.g. ``"my-widget"``).
        output_dir: Where to create the template. Defaults to CWD.

    Returns:
        Path to the created directory.
    """
    if output_dir is None:
        output_dir = Path.cwd()
    output_dir = Path(output_dir)

    # Normalize name
    pkg_name = name.replace("-", "_")
    dir_name = f"cacao-{name}" if not name.startswith("cacao-") else name
    ext_dir = output_dir / dir_name

    ext_dir.mkdir(parents=True, exist_ok=True)
    (ext_dir / pkg_name).mkdir(exist_ok=True)

    # __init__.py
    init_content = f'''"""
Cacao extension: {name}
"""

from __future__ import annotations

from typing import Any


def register(plugin: Any) -> None:
    """Called by Cacao when the extension is loaded.

    Args:
        plugin: A Cacao Plugin instance. Use it to register hooks,
            components, handlers, and themes.
    """
    plugin.on("on_ready", lambda: None)

    # Example: register a custom component
    # from cacao.extensions import ComponentSpec, register_component
    # register_component(ComponentSpec(
    #     name="MyWidget",
    #     js_code=\'\'\'export function MyWidget({{ value }}) {{
    #         return React.createElement("div", null, value);
    #     }}\'\'\',
    # ))

    # Example: register static build handlers
    # from cacao.extensions import register_handler_plugin
    # register_handler_plugin("{name}", {{
    #     "my_action": \'\'\'async function(signals, event) {{
    #         signals.set("result", "done");
    #     }}\'\'\',
    # }})
'''

    (ext_dir / pkg_name / "__init__.py").write_text(init_content, encoding="utf-8")

    # pyproject.toml
    pyproject_content = f"""[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "cacao-{name}"
version = "0.1.0"
description = "A Cacao extension"
requires-python = ">=3.10"
dependencies = ["cacao"]

[project.entry-points.cacao_extensions]
{name} = "{pkg_name}:register"
"""

    (ext_dir / "pyproject.toml").write_text(pyproject_content, encoding="utf-8")

    return ext_dir
