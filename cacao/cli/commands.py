"""
CLI commands for Cacao v2.

Provides the main CLI interface for running Cacao applications with hot reload.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import random
import socket
import subprocess
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

# ANSI color codes
BROWN = "\033[38;5;130m"
DARK_BROWN = "\033[38;5;94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def _get_logo() -> str:
    """Get the ASCII art logo with the current version."""
    from cacao import __version__

    return f"""{BROWN}
   ______
  / ____/___ _________ _____
 / /   / __ `/ ___/ __ `/ __ \\
/ /___/ /_/ / /__/ /_/ / /_/ /
\\____/\\__,_/\\___/\\__,_/\\____/{RESET}  {DIM}v{__version__}{RESET}
"""


# Historic chocolate years (sorted) - used as default ports
# Each year represents a milestone in chocolate history
CHOCOLATE_YEARS = [
    1502,  # Columbus encounters cacao beans in Honduras
    1519,  # Cortés encounters chocolate in Aztec court
    1544,  # Chocolate introduced to Spanish court by Mayan nobles
    1585,  # First official shipment of cacao to Europe
    1657,  # Chocolate arrives in England from France
    1729,  # Walter Churchman patents water-powered cocoa milling
    1753,  # Linnaeus names cacao tree Theobroma ("food of the gods")
    1760,  # Chocolaterie Lombart founded, first French chocolate company
    1789,  # J.S. Fry & Sons acquires cocoa milling patent
    1819,  # François-Louis Cailler opens first Swiss chocolate factory
    1828,  # Van Houten patents Dutch cocoa process
    1847,  # Fry's creates the first chocolate bar
    1875,  # Daniel Peter invents milk chocolate
    1879,  # Rodolphe Lindt invents conching
    1925,  # Octaaf Callebaut invents couverture chocolate
    1936,  # Nestlé introduces white chocolate
]

# Random chocolate facts to display on startup
CHOCOLATE_FACTS = [
    "The word 'chocolate' likely comes from the Nahuatl word 'xocoatl' meaning 'bitter water'",
    "Aztecs believed cacao was a gift from the god Quetzalcoatl",
    "Cocoa beans were used as currency in ancient Mesoamerica - 100 beans could buy a turkey!",
    "The Maya consumed chocolate as early as 600 BC",
    "Columbus encountered cacao beans in 1502 but didn't know what they were",
    "Chocolate was originally drunk, not eaten - solid chocolate wasn't invented until 1847",
    "The conching process that makes chocolate smooth was kept secret for over 20 years",
    "The scientific name for cacao, Theobroma, means 'food of the gods' in Greek",
    "Chocolate was once considered medicine in Europe and used to treat various ailments",
    "The Maya poured chocolate from a height to create a highly prized brown foam",
    "White chocolate was first sold by Nestle in 1936",
    "Quaker families founded Cadbury, Rowntree's, and Fry's as an alternative to alcohol",
    "Early Europeans found chocolate's foam particularly objectionable",
    "Milk chocolate was invented in 1875 using newly-invented powdered milk",
    "The molinillo (wooden whisk) was invented by Spaniards to create chocolate foam",
    "Chocolate houses in England served chocolate to anyone who could pay",
    "Aztec soldiers received chocolate rations as a stimulant during battle",
    "Counterfeit cocoa beans were made from dough, wax, or broken avocado pits",
    "Ghana overtook Sao Tome as the world's largest cacao producer in 1911",
    "Before conching was invented in 1879, chocolate was gritty in texture",
]


def is_port_available(host: str, port: int) -> bool:
    """Check if a port is available for binding."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            s.bind((host, port))
            return True
    except OSError:
        return False


def find_available_port(host: str, preferred_port: int | None = None) -> tuple[int, str]:
    """
    Find an available port from chocolate history years.

    Returns:
        Tuple of (port, year_description)
    """
    year_descriptions = {
        1502: "Columbus encounters cacao in Honduras",
        1519: "Cortés meets chocolate in Aztec court",
        1544: "Chocolate arrives at Spanish court",
        1585: "First cacao shipment to Europe",
        1657: "Chocolate reaches England",
        1729: "Water-powered cocoa milling patented",
        1753: "Linnaeus names it Theobroma",
        1760: "First French chocolate company founded",
        1789: "Fry acquires cocoa milling patent",
        1819: "First Swiss chocolate factory opens",
        1828: "Van Houten's Dutch cocoa process",
        1847: "First chocolate bar created",
        1875: "Milk chocolate invented",
        1879: "Conching invented by Lindt",
        1925: "Couverture chocolate invented",
        1936: "Nestlé launches white chocolate",
    }

    # If a preferred port is given and available, use it
    if preferred_port is not None:
        if is_port_available(host, preferred_port):
            desc = year_descriptions.get(preferred_port, "")
            return preferred_port, desc
        # If preferred port is in our list, start from there
        if preferred_port in CHOCOLATE_YEARS:
            start_idx = CHOCOLATE_YEARS.index(preferred_port)
        else:
            start_idx = 0
    else:
        start_idx = 0

    # Try chocolate years starting from the preferred one
    for i in range(len(CHOCOLATE_YEARS)):
        idx = (start_idx + i) % len(CHOCOLATE_YEARS)
        port = CHOCOLATE_YEARS[idx]
        if is_port_available(host, port):
            return port, year_descriptions.get(port, "")

    # Fallback: try ports after the highest chocolate year
    for port in range(CHOCOLATE_YEARS[-1] + 1, 65536):
        if is_port_available(host, port):
            return port, ""

    raise RuntimeError("No available ports found")


def print_banner(
    host: str,
    port: int,
    reload: bool,
    app_file: str,
    year_significance: str = "",
    config_file: str | None = None,
) -> None:
    """Print the startup banner with a random chocolate fact."""
    print(_get_logo())

    # Consistent label width for alignment
    def _line(label: str, value: str) -> str:
        return f"  {DARK_BROWN}{label:<12}{RESET}{value}"

    print(_line("App", app_file))
    if config_file:
        print(_line("Config", config_file))
    print(_line("URL", f"{CYAN}http://{host}:{port}{RESET}"))
    if year_significance:
        print(_line("Port", f"{DIM}{port} \u00b7 {year_significance}{RESET}"))
    reload_val = f"{GREEN}enabled{RESET}" if reload else f"{DIM}disabled{RESET}"
    print(_line("Hot reload", reload_val))
    print()
    # Display a random chocolate fact
    fact = random.choice(CHOCOLATE_FACTS)
    print(f"  {DIM}{fact}{RESET}")
    print()
    print(f"  {DIM}Press Ctrl+C to stop{RESET}")
    print()


def load_app_module(app_path: Path) -> Any:
    """
    Load a Python module from a file path.

    Args:
        app_path: Path to the Python file

    Returns:
        The loaded module
    """
    # Add the app's directory to sys.path
    app_dir = app_path.parent.resolve()
    if str(app_dir) not in sys.path:
        sys.path.insert(0, str(app_dir))

    # Load the module
    spec = importlib.util.spec_from_file_location("__cacao_app__", app_path.resolve())
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {app_path}")

    module = importlib.util.module_from_spec(spec)

    # Don't add to sys.modules to avoid caching issues with reload
    spec.loader.exec_module(module)

    return module


def find_app_instance(module: Any) -> Any:
    """
    Find the Cacao App instance in a module.

    Looks for (in order):
    1. Simple mode global app (from `import cacao as c`)
    2. A variable named 'app'
    3. Any instance of cacao.server.ui.App

    Args:
        module: The loaded module

    Returns:
        The App instance

    Raises:
        RuntimeError: If no App instance is found
    """
    # First, check for simple mode (global app from cacao module)
    try:
        import cacao

        if cacao.is_simple_mode():
            return cacao.get_app()
    except (ImportError, AttributeError):
        pass

    # Second, try to find 'app' variable
    if hasattr(module, "app"):
        app = getattr(module, "app")
        if hasattr(app, "run") and hasattr(app, "_pages"):
            return app

    # Third, search for any App instance
    from cacao.server.ui import App

    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, App):
            return obj

    raise RuntimeError(
        "No Cacao App instance found in module. "
        "Make sure to create an App instance, e.g.:\n\n"
        "  from cacao.server.ui import App\n"
        "  app = App(title='My App')\n"
    )


def run_with_reload(app_path: Path, host: str, port: int, verbose: bool) -> None:
    """
    Run the app with hot reload using watchfiles.

    Uses subprocess to run the app and restarts on file changes.
    """
    try:
        import watchfiles
    except ImportError:
        print(
            f"{YELLOW}Warning: watchfiles not installed. "
            f"Install with: pip install watchfiles{RESET}"
        )
        print(f"{DIM}Running without hot reload...{RESET}")
        run_without_reload(app_path, host, port, verbose)
        return

    app_dir = app_path.parent.resolve()

    def run_app() -> subprocess.Popen[bytes]:
        """Start the app in a subprocess."""
        env = os.environ.copy()
        env["CACAO_APP_FILE"] = str(app_path.resolve())
        env["CACAO_HOST"] = host
        env["CACAO_PORT"] = str(port)
        env["CACAO_VERBOSE"] = "1" if verbose else "0"
        env["PYTHONUNBUFFERED"] = "1"

        # Run the internal runner
        return subprocess.Popen(
            [sys.executable, "-m", "cacao.cli.runner"],
            env=env,
            cwd=str(app_dir),
        )

    process = run_app()

    try:
        # Watch for changes
        for changes in watchfiles.watch(app_dir, watch_filter=lambda _, path: path.endswith(".py")):
            changed_files = [str(c[1]) for c in changes]

            # Print reload message
            print()
            print(f"{DARK_BROWN}Detected changes in:{RESET}")
            for f in changed_files:
                rel_path = os.path.relpath(f, app_dir)
                print(f"  {DIM}{rel_path}{RESET}")
            print(f"{BROWN}Reloading...{RESET}")

            # Stop the old process
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()

            # Start new process
            time.sleep(0.1)  # Small delay to release port
            process = run_app()

    except KeyboardInterrupt:
        pass
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


def run_without_reload(app_path: Path, host: str, port: int, verbose: bool) -> None:
    """
    Run the app directly without hot reload.
    """
    # Change to app directory
    app_dir = app_path.parent.resolve()
    original_cwd = os.getcwd()
    os.chdir(app_dir)

    try:
        module = load_app_module(app_path)
        app = find_app_instance(module)

        if verbose:
            app.debug = True

        # Run the app
        app.run(host=host, port=port, reload=False)

    finally:
        os.chdir(original_cwd)


def run_command(args: list[str]) -> None:
    """
    Run a Cacao v2 application.

    Usage: cacao run app.py [options]
    """
    # Default port is the first chocolate year (1502 - Columbus encounters cacao)
    default_port = CHOCOLATE_YEARS[0]

    parser = argparse.ArgumentParser(prog="cacao run", description="Run a Cacao v2 application")
    parser.add_argument("app_file", help="Path to the app file (e.g., app.py)")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to (default: 127.0.0.1)")
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=default_port,
        help=f"Port to listen on (default: {default_port}, historic chocolate years)",
    )
    parser.add_argument("--no-reload", action="store_true", help="Disable hot reload")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode (verbose WS logging + browser DevTools)",
    )

    parsed_args = parser.parse_args(args)

    app_path = Path(parsed_args.app_file)

    # Validate app file
    if not app_path.exists():
        print(f"{RED}Error: File '{parsed_args.app_file}' not found{RESET}")
        sys.exit(1)

    if not app_path.suffix == ".py":
        print(f"{RED}Error: '{parsed_args.app_file}' is not a Python file{RESET}")
        sys.exit(1)

    hot_reload = not parsed_args.no_reload
    verbose = parsed_args.verbose or parsed_args.debug

    # Find an available port (auto-increment through chocolate years if needed)
    try:
        port, year_significance = find_available_port(parsed_args.host, parsed_args.port)
        if port != parsed_args.port:
            print(f"{YELLOW}Port {parsed_args.port} is in use, using port {port} instead{RESET}")
    except RuntimeError as e:
        print(f"{RED}Error: {e}{RESET}")
        sys.exit(1)

    # Check for cacao.yaml config file
    from cacao.config import find_config_file

    config_file = find_config_file(app_path.parent)
    config_file_str = str(config_file) if config_file else None

    # Print banner
    print_banner(
        host=parsed_args.host,
        port=port,
        reload=hot_reload,
        app_file=str(app_path.resolve()),
        year_significance=year_significance,
        config_file=config_file_str,
    )

    if verbose:
        print(
            f"  {CYAN}Debug mode enabled{RESET}"
            " — verbose WS logging + browser DevTools (Ctrl+Shift+D)"
        )
        print()

    try:
        if hot_reload:
            run_with_reload(app_path, parsed_args.host, port, verbose)
        else:
            run_without_reload(app_path, parsed_args.host, port, verbose)
    except KeyboardInterrupt:
        print(f"\n{DIM}Server stopped{RESET}")
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


def create_command(args: list[str]) -> None:
    """
    Create a new Cacao v2 project.

    Usage: cacao create [name] [--template <template>]
    """
    parser = argparse.ArgumentParser(
        prog="cacao create", description="Create a new Cacao v2 project"
    )
    parser.add_argument("name", nargs="?", help="Project name")
    parser.add_argument(
        "-t",
        "--template",
        choices=["minimal", "counter", "dashboard", "structured"],
        default="minimal",
        help="Template to use",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    parsed_args = parser.parse_args(args)

    # Get project name interactively if not provided
    project_name = parsed_args.name
    if not project_name:
        try:
            project_name = input("Project name: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nCancelled.")
            sys.exit(1)

    if not project_name:
        print(f"{RED}Error: Project name cannot be empty{RESET}")
        sys.exit(1)

    # Validate project name
    import re

    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", project_name):
        print(
            f"{RED}Error: Project name can only contain letters, "
            f"numbers, hyphens, and underscores{RESET}"
        )
        sys.exit(1)

    project_path = Path.cwd() / project_name

    if project_path.exists():
        print(f"{RED}Error: Directory '{project_name}' already exists{RESET}")
        sys.exit(1)

    print(f"\nCreating project '{project_name}' with '{parsed_args.template}' template...")

    try:
        # Create project structure
        project_path.mkdir(parents=True)

        # Get template content (single file or multi-file dict)
        template = _get_template(parsed_args.template)

        if isinstance(template, dict):
            # Multi-file template
            for rel_path, content in template.items():
                file_path = project_path / rel_path
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(content, encoding="utf-8")
        else:
            # Single file template
            app_file = project_path / "app.py"
            app_file.write_text(template, encoding="utf-8")

        # Write requirements.txt
        requirements = project_path / "requirements.txt"
        requirements.write_text("cacao\nuvicorn\nwatchfiles\n", encoding="utf-8")

        print(f"\n{GREEN}Project created successfully!{RESET}")
        print("\nNext steps:")
        print(f"  {CYAN}cd {project_name}{RESET}")
        print(f"  {CYAN}pip install -r requirements.txt{RESET}")
        print(f"  {CYAN}cacao run app.py{RESET}")

    except Exception as e:
        print(f"{RED}Error creating project: {e}{RESET}")
        # Clean up on failure
        if project_path.exists():
            import shutil

            shutil.rmtree(project_path)
        sys.exit(1)


def _get_template(template_name: str) -> str:
    """Get the content for a project template."""
    templates = {
        "minimal": '''"""
Minimal Cacao v2 application.
"""
from cacao.server.ui import App, title, text

app = App(title="My Cacao App")

with app.page("/"):
    title("Welcome to Cacao")
    text("Edit app.py to get started")

if __name__ == "__main__":
    app.run()
''',
        "counter": '''"""
Counter application demonstrating Cacao v2 signals.
"""
from cacao.server.ui import App, row, card, metric, button, title

app = App(title="Counter")

count = app.signal(0, name="count")

@app.on("increment")
async def increment(session, event):
    count.set(session, count.get(session) + 1)

@app.on("decrement")
async def decrement(session, event):
    count.set(session, count.get(session) - 1)

@app.on("reset")
async def reset(session, event):
    count.set(session, 0)

with app.page("/"):
    title("Counter Demo")
    with row():
        metric("Count", count)
    with row():
        button("-", on_click="decrement", variant="secondary")
        button("+", on_click="increment")
        button("Reset", on_click="reset", variant="ghost")

if __name__ == "__main__":
    app.run()
''',
        "dashboard": '''"""
Dashboard template with metrics and charts.
"""
from cacao.server.ui import App, row, col, card, metric, title, text, sidebar, select
from cacao.server.chart import line, bar, pie
from cacao.server.data import sample_sales_data

app = App(title="Sales Dashboard", theme="dark")

# Load sample data
sales_data = sample_sales_data()

with app.page("/"):
    title("Sales Dashboard")
    text("Real-time sales metrics and analytics", color="muted")

    # KPI metrics row
    with row():
        metric("Revenue", "$45,231", trend="+20.1%", trend_direction="up")
        metric("Orders", "1,247", trend="+12.5%", trend_direction="up")
        metric("Customers", "842", trend="+5.3%", trend_direction="up")
        metric("Avg Order", "$36.25", trend="-2.1%", trend_direction="down")

    # Charts row
    with row():
        with col(span=8):
            with card("Revenue Trend"):
                line(sales_data, x="date", y="revenue", area=True)
        with col(span=4):
            with card("Sales by Category"):
                pie(sales_data[:5], name_field="category", value_field="revenue", donut=True)

with sidebar():
    title("Filters", level=3)
    select("Time Period", ["Last 7 days", "Last 30 days", "Last 90 days", "This year"])
    select("Category", ["All", "Electronics", "Clothing", "Food", "Other"])

if __name__ == "__main__":
    app.run()
''',
        "structured": _get_structured_template(),
    }
    return templates.get(template_name, templates["minimal"])


def _get_structured_template() -> dict[str, str]:
    """Generate a multi-file structured project template.

    Returns a dict of {relative_path: content} for all files.
    """
    return {
        # --- Entry point ---
        "app.py": '''"""My Cacao App - main entry point."""
import cacao as c

c.config(title="My App", theme="dark")

# Import pages (each page registers itself)
from pages import home, settings  # noqa: E402, F401

# Import event handlers
from handlers import events  # noqa: E402, F401
''',
        # --- Pages ---
        "pages/__init__.py": "",
        "pages/home.py": '''"""Home page."""
import cacao as c

from components.header import render_header


with c.page("/"):
    render_header()
    c.title("Welcome")
    c.text("Edit pages/home.py to get started.")

    with c.row():
        c.metric("Status", "Online", trend="+100%", trend_direction="up")
''',
        "pages/settings.py": '''"""Settings page."""
import cacao as c


theme_choice = c.signal("dark", name="theme_choice")

with c.page("/settings"):
    c.title("Settings")
    c.select(
        "Theme",
        options=["dark", "light"],
        signal=theme_choice,
        on_change="change_theme",
    )
''',
        # --- Shared components ---
        "components/__init__.py": "",
        "components/header.py": '''"""Reusable header component."""
import cacao as c


def render_header() -> None:
    """Render the app header."""
    with c.row(gap=4, align="center"):
        c.title("My App", level=3)
        c.badge("v1.0", color="info")
''',
        # --- Event handlers ---
        "handlers/__init__.py": "",
        "handlers/events.py": '''"""Event handlers."""
import cacao as c
from cacao.server.session import Session


@c.on("change_theme")
async def handle_change_theme(session: Session, event: dict) -> None:
    """Handle theme change."""
    pass  # Theme signal updates automatically via c.select binding
''',
        # --- Data directory ---
        "data/.gitkeep": "",
    }


def build_command(args: list[str]) -> None:
    """
    Build a static version of a Cacao application.

    Usage: cacao build app.py [options]

    Generates a static site that can be hosted on GitHub Pages, Netlify, etc.
    No server required - runs entirely in the browser with JavaScript handlers.
    """
    import json
    import shutil

    parser = argparse.ArgumentParser(
        prog="cacao build", description="Build a static Cacao application"
    )
    parser.add_argument("app_file", help="Path to the app file (e.g., app.py)")
    parser.add_argument("-o", "--output", default="dist", help="Output directory (default: dist)")
    parser.add_argument(
        "--base-path", default="", help="Base path for deployment (e.g., /my-repo for GitHub Pages)"
    )
    parser.add_argument(
        "--embed-url",
        default="",
        help="URL where the app will be hosted (generates embed snippet)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    parsed_args = parser.parse_args(args)

    app_path = Path(parsed_args.app_file)
    output_dir = Path(parsed_args.output)

    # Validate app file
    if not app_path.exists():
        print(f"{RED}Error: File '{parsed_args.app_file}' not found{RESET}")
        sys.exit(1)

    if not app_path.suffix == ".py":
        print(f"{RED}Error: '{parsed_args.app_file}' is not a Python file{RESET}")
        sys.exit(1)

    print(f"{CYAN}Building static site...{RESET}")

    # Load the app module
    app_dir = app_path.parent.resolve()
    original_cwd = os.getcwd()
    os.chdir(app_dir)

    try:
        # Import and execute the app to build component tree
        if parsed_args.verbose:
            print(f"  Loading {app_path.name}...")

        module = load_app_module(app_path)

        # Get the export data using cacao.export_static()
        import cacao

        export_data = cacao.export_static()

        if parsed_args.verbose:
            print(f"  Found {len(export_data.get('pages', {}))} page(s)")
            print(f"  Found {len(export_data.get('signals', {}))} signal(s)")

    finally:
        os.chdir(original_cwd)

    # Create output directory
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    # Copy Cacao frontend assets
    frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"

    if not frontend_dist.exists():
        print(
            f"{RED}Error: Frontend not built. Run 'npm run build' in cacao/frontend first.{RESET}"
        )
        sys.exit(1)

    # Determine which component categories are used
    categories: set[str] | None = None
    try:
        import cacao as _cacao_mod

        if _cacao_mod.is_simple_mode():
            app_instance = _cacao_mod.get_app()
        else:
            app_instance = find_app_instance(module)
        if hasattr(app_instance, "get_used_categories"):
            categories = app_instance.get_used_categories()
            if parsed_args.verbose:
                cats = ", ".join(sorted(categories)) if categories else "none"
                print(f"  Component categories: {cats}")
    except Exception:
        pass  # Fall back to full bundle

    # Copy JS (always needed)
    shutil.copy(frontend_dist / "cacao.js", output_dir / "cacao.js")

    # Copy CSS — optimized per category or full bundle as fallback
    if categories is not None and (frontend_dist / "cacao-core.css").exists():
        shutil.copy(frontend_dist / "cacao-core.css", output_dir / "cacao-core.css")
        for cat in sorted(categories):
            css_file = f"cacao-cat-{cat}.css"
            if (frontend_dist / css_file).exists():
                shutil.copy(frontend_dist / css_file, output_dir / css_file)
    else:
        shutil.copy(frontend_dist / "cacao.css", output_dir / "cacao.css")
        categories = None  # Signal to use full bundle in HTML

    if parsed_args.verbose:
        print("  Copied cacao.js (includes built-in handlers)")
        if categories is not None:
            print(f"  Copied optimized CSS: core + {', '.join(sorted(categories))}")
        else:
            print("  Copied full cacao.css")

    # Generate index.html
    metadata = export_data.get("metadata", {})
    title = metadata.get("title", "Cacao App")
    theme = metadata.get("theme", "dark")
    branding = metadata.get("branding")

    # Serialize pages data
    pages_json = json.dumps(
        {
            "pages": export_data.get("pages", {}),
            "metadata": metadata,
        }
    )
    signals_json = json.dumps(export_data.get("signals", {}))

    # Static handlers and scripts from the app
    static_handlers = export_data.get("static_handlers", {})
    static_scripts = export_data.get("static_scripts", [])

    # Merge handler plugin handlers (extension system)
    handler_plugin_handlers = export_data.get("handler_plugins", {})
    for evt_name, js_code in handler_plugin_handlers.items():
        if evt_name not in static_handlers:
            static_handlers[evt_name] = js_code

    # Build handlers JS object: { "event_name": async function(signals, event) { ... }, ... }
    handler_entries = []
    for evt_name, js_code in static_handlers.items():
        handler_entries.append(f'"{evt_name}": {js_code}')
    handlers_js = "{" + ", ".join(handler_entries) + "}" if handler_entries else "{}"

    # Build extra scripts block
    extra_scripts = "\n".join(static_scripts) if static_scripts else ""

    # Build the HTML
    # Use relative paths when no base_path is specified (for file:// and local preview)
    # Use absolute paths when base_path is set (for GitHub Pages subdirectories)
    base_path = parsed_args.base_path.rstrip("/")
    asset_prefix = base_path if base_path else "."

    # Generate branding HTML
    branding_html = ""
    if branding:
        if isinstance(branding, str):
            branding_html = f'\n    <div class="cacao-branding">{branding}</div>'
        else:
            branding_html = (
                '\n    <div class="cacao-branding">'
                'Built with <a href="https://github.com/cacao-research/Cacao"'
                ' target="_blank"><strong>Cacao</strong></a> &#x1F90E;</div>'
            )

    # Build CSS links based on categories
    if categories is not None:
        css_links = f'    <link rel="stylesheet" href="{asset_prefix}/cacao-core.css">'
        for cat in sorted(categories):
            css_links += f'\n    <link rel="stylesheet" href="{asset_prefix}/cacao-cat-{cat}.css">'
    else:
        css_links = f'    <link rel="stylesheet" href="{asset_prefix}/cacao.css">'

    needs_charts = categories is None or "charts" in (categories or set())
    chartjs_tag = (
        '\n    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>'
        if needs_charts
        else ""
    )

    html_content = f'''<!DOCTYPE html>
<html lang="en" data-theme="{theme}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
{css_links}
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
          rel="stylesheet">
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>{chartjs_tag}
</head>
<body>
    <div id="root"><div class="loading">Loading...</div></div>{branding_html}

    <script>
    // Static mode configuration
    window.__CACAO_STATIC__ = true;
    window.__CACAO_DEFER_MOUNT__ = true;
    window.__CACAO_BASE_PATH__ = "{base_path}";
    window.__CACAO_PAGES__ = {pages_json};
    window.__CACAO_INITIAL_SIGNALS__ = {signals_json};
    </script>

    <script src="{asset_prefix}/cacao.js"></script>

    {f"<script>{extra_scripts}</script>" if extra_scripts else ""}

    <script>
    // Initialize static mode and mount (handlers are built into cacao.js)
    (function() {{
        Cacao.initStatic({{
            pages: window.__CACAO_PAGES__,
            signals: window.__CACAO_INITIAL_SIGNALS__,
            handlers: {handlers_js}
        }});
        Cacao.mount();
    }})();
    </script>
</body>
</html>'''

    # Write index.html
    (output_dir / "index.html").write_text(html_content, encoding="utf-8")

    # Create 404.html for SPA routing on GitHub Pages
    (output_dir / "404.html").write_text(html_content, encoding="utf-8")

    print(f"{GREEN}Build complete!{RESET}")
    print(f"\nOutput: {output_dir.resolve()}")
    print("  - index.html")
    print("  - 404.html (for SPA routing)")
    if categories is not None:
        print("  - cacao-core.css")
        for cat in sorted(categories):
            print(f"  - cacao-cat-{cat}.css")
        skipped = {"layout", "display", "typography", "form"} - categories
        if skipped:
            print(f"  {DIM}(skipped: {', '.join(sorted(skipped))}){RESET}")
        if "charts" not in categories:
            print(f"  {DIM}(skipped: Chart.js CDN ~200KB){RESET}")
    else:
        print("  - cacao.css")
    print("  - cacao.js (includes built-in handlers)")
    print()
    print("To preview locally:")
    print(f"  {CYAN}python -m http.server -d {output_dir}{RESET}")
    print()

    # Print embed snippet if URL is provided
    if parsed_args.embed_url:
        from .gallery import generate_embed_snippet

        embed_url = parsed_args.embed_url.rstrip("/")
        print(f"{BOLD}Embed snippet:{RESET}")
        snippet = generate_embed_snippet(embed_url, title=title)
        for line in snippet.split("\n"):
            print(f"  {DIM}{line}{RESET}")
        print()


def version_command(args: list[str]) -> None:
    """Show version information."""
    from cacao import __version__

    print(f"Cacao v{__version__}")
    print(f"Python: {sys.version}")


def help_command(args: list[str]) -> None:
    """Show help information."""
    print(_get_logo())
    print("Usage: cacao <command> [options]")
    print()
    print("Commands:")
    print(f"  {CYAN}run{RESET} <app.py>     Run a Cacao application with hot reload")
    print(f"  {CYAN}build{RESET} <app.py>   Build a static site (for GitHub Pages, etc.)")
    print(f"  {CYAN}share{RESET} <app.py>   Share app via public URL (tunnel + QR code)")
    print(f"  {CYAN}deploy{RESET} <app.py>  Deploy to cloud (HF Spaces, Railway, Render, Fly.io)")
    print(f"  {CYAN}docker{RESET} <app.py>  Generate Dockerfile for containerized deployment")
    print(f"  {CYAN}publish{RESET} <app.py> Publish app to the Cacao gallery")
    print(f"  {CYAN}gallery{RESET}          Browse the Cacao app gallery")
    print(f"  {CYAN}install{RESET} <ext>    Install a Cacao extension or theme")
    print(f"  {CYAN}uninstall{RESET} <ext>  Uninstall a Cacao extension")
    print(f"  {CYAN}extensions{RESET}       List installed extensions, themes & handlers")
    print(f"  {CYAN}convert{RESET} <nb.ipynb> Convert a Jupyter notebook to a Cacao app")
    print(f"  {CYAN}test{RESET} [target]    Run tests for a Cacao app")
    print(f"  {CYAN}create{RESET} [name]    Create a new Cacao project")
    print(f"  {CYAN}version{RESET}          Show version information")
    print(f"  {CYAN}help{RESET}             Show this help message")
    print()
    print("Examples:")
    print("  cacao run app.py              Run app with hot reload (default port: 1502)")
    print("  cacao run app.py --port 1847  Run on port 1847 (year of first chocolate bar)")
    print("  cacao run app.py --debug      Enable DevTools + verbose WS logging")
    print("  cacao run app.py --no-reload  Run without hot reload")
    print("  cacao create my-dashboard     Create a new project")
    print("  cacao create my-app -t structured  Multi-file project with pages/components")
    print()
    print(f"  {BOLD}Static builds:{RESET}")
    print("  cacao build app.py                     Build static site to dist/")
    print("  cacao build app.py --base-path /repo   Set base path for GitHub Pages")
    print()
    print(f"  {BOLD}Sharing:{RESET}")
    print("  cacao share app.py                     Share via public tunnel URL")
    print("  cacao share app.py --password secret    Password-protected sharing")
    print("  cacao share app.py --expire 24          Auto-expire after 24 hours")
    print()
    print(f"  {BOLD}Deployment:{RESET}")
    print("  cacao deploy app.py                    Guided cloud deployment")
    print("  cacao deploy app.py hf                 Generate Hugging Face Spaces files")
    print("  cacao deploy app.py railway             Generate Railway config")
    print("  cacao docker app.py                    Generate Dockerfile")
    print()
    print(f"  {BOLD}Notebook:{RESET}")
    print("  cacao convert notebook.ipynb              Convert notebook to app")
    print("  cacao convert notebook.ipynb -o app.py    Custom output path")
    print("  cacao convert notebook.ipynb --no-markdown Skip markdown cells")
    print()
    print(f"  {BOLD}Testing:{RESET}")
    print("  cacao test tests/                      Run all tests in directory")
    print("  cacao test test_app.py                 Run tests in a specific file")
    print("  cacao test tests/ -v                   Verbose output")
    print("  cacao test tests/ -u                   Update snapshots")
    print()
    print(f"  {BOLD}Gallery:{RESET}")
    print("  cacao publish app.py                   Publish app to gallery")
    print("  cacao publish app.py --url https://...  With live URL + embed snippet")
    print("  cacao gallery                          Browse all published apps")
    print("  cacao gallery --embed my-app           Get embed snippet for an app")
    print("  cacao gallery dashboard --tag ml        Search & filter apps")
    print()
    print(f"  {BOLD}Extensions:{RESET}")
    print("  cacao install my-widget                Install extension from PyPI")
    print("  cacao install my-widget --upgrade      Upgrade an extension")
    print("  cacao install --theme ocean            Install a marketplace theme")
    print("  cacao uninstall my-widget              Remove an extension")
    print("  cacao extensions                       List installed extensions")
    print("  cacao extensions --themes              Browse theme marketplace")
    print("  cacao extensions --handlers            Show handler plugins")
    print("  cacao extensions --create my-ext       Scaffold a new extension")
    print()
    print(
        f"{DIM}Ports are historic chocolate years (1502-1936). "
        f"If in use, auto-increments to next year.{RESET}"
    )
    print()


def test_command(args: list[str]) -> None:
    """
    Run tests for a Cacao application.

    Usage: cacao test [target] [options]
    """
    parser = argparse.ArgumentParser(prog="cacao test", description="Run Cacao app tests")
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Path to test file or directory (default: current directory)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument(
        "--pattern",
        "-p",
        default="test_*.py",
        help="Glob pattern for test files (default: test_*.py)",
    )
    parser.add_argument(
        "--update-snapshots",
        "-u",
        action="store_true",
        help="Update snapshot files with current values",
    )

    parsed = parser.parse_args(args)

    from cacao.testing import run_tests

    print(_get_logo())
    print(f"  {CYAN}Running tests...{RESET}")

    result = run_tests(
        parsed.target,
        verbose=parsed.verbose,
        pattern=parsed.pattern,
        update_snapshots=parsed.update_snapshots,
    )

    if not result.all_passed:
        sys.exit(1)


# Lazy imports for commands to avoid heavy imports at CLI startup
def convert_command(args: list[str]) -> None:
    """
    Convert a Jupyter notebook to a Cacao application.

    Usage: cacao convert notebook.ipynb [options]

    Extracts code and markdown cells from a notebook and generates
    a standalone Cacao app.py file.
    """
    parser = argparse.ArgumentParser(
        prog="cacao convert", description="Convert a Jupyter notebook to a Cacao app"
    )
    parser.add_argument("notebook", help="Path to the .ipynb file")
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output .py file path (default: same name with .py extension)",
    )
    parser.add_argument(
        "--no-markdown",
        action="store_true",
        help="Skip markdown cells (don't convert to c.markdown())",
    )
    parser.add_argument(
        "--include-outputs",
        action="store_true",
        help="Include cell outputs as comments",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    parsed = parser.parse_args(args)

    notebook_path = Path(parsed.notebook)
    if not notebook_path.exists():
        print(f"{RED}Error: File '{parsed.notebook}' not found{RESET}")
        sys.exit(1)

    if not notebook_path.suffix == ".ipynb":
        print(f"{RED}Error: '{parsed.notebook}' is not a Jupyter notebook (.ipynb){RESET}")
        sys.exit(1)

    print(_get_logo())
    print(f"  {CYAN}Converting notebook...{RESET}")

    from cacao.notebook import convert_notebook

    try:
        output = convert_notebook(
            notebook_path,
            parsed.output,
            include_markdown=not parsed.no_markdown,
            include_outputs=parsed.include_outputs,
        )
        print(f"  {GREEN}Created {output}{RESET}")
        print()
        print("Next steps:")
        print(f"  {CYAN}cacao run {output}{RESET}          Run the converted app")
        print(f"  {CYAN}cacao build {output}{RESET}        Build as static site")
        print()
    except Exception as e:
        print(f"  {RED}Error: {e}{RESET}")
        sys.exit(1)


def _share_command_wrapper(args: list[str]) -> None:
    from .share import share_command

    share_command(args)


def _deploy_command_wrapper(args: list[str]) -> None:
    from .deploy import deploy_command

    deploy_command(args)


def _docker_command_wrapper(args: list[str]) -> None:
    from .deploy import docker_command

    docker_command(args)


def _publish_command_wrapper(args: list[str]) -> None:
    from .gallery import publish_command

    publish_command(args)


def _gallery_command_wrapper(args: list[str]) -> None:
    from .gallery import gallery_command

    gallery_command(args)


def _install_command_wrapper(args: list[str]) -> None:
    from .install import install_command

    install_command(args)


def _uninstall_command_wrapper(args: list[str]) -> None:
    from .install import uninstall_command

    uninstall_command(args)


def _extensions_command_wrapper(args: list[str]) -> None:
    from .install import extensions_command

    extensions_command(args)


# Command registry
COMMANDS: dict[str, Callable[[list[str]], None]] = {
    "run": run_command,
    "build": build_command,
    "convert": convert_command,
    "share": _share_command_wrapper,
    "deploy": _deploy_command_wrapper,
    "docker": _docker_command_wrapper,
    "publish": _publish_command_wrapper,
    "gallery": _gallery_command_wrapper,
    "install": _install_command_wrapper,
    "uninstall": _uninstall_command_wrapper,
    "extensions": _extensions_command_wrapper,
    "test": test_command,
    "create": create_command,
    "version": version_command,
    "help": help_command,
}


def run_cli() -> None:
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        help_command([])
        sys.exit(0)

    command = sys.argv[1]
    args = sys.argv[2:]

    # Handle --help and --version flags
    if command in ("--help", "-h"):
        help_command([])
        sys.exit(0)

    if command in ("--version", "-V"):
        version_command([])
        sys.exit(0)

    # Find and run command
    handler = COMMANDS.get(command)
    if handler:
        handler(args)
    else:
        print(f"{RED}Unknown command: {command}{RESET}")
        print("Run 'cacao help' for usage information")
        sys.exit(1)


def main() -> None:
    """Alias for run_cli."""
    run_cli()


if __name__ == "__main__":
    main()
