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
from pathlib import Path
from typing import Any, Callable

# ANSI color codes
PURPLE = "\033[95m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

# ASCII art logo
LOGO = f"""{PURPLE}
   ______
  / ____/___ _________ _____
 / /   / __ `/ ___/ __ `/ __ \\
/ /___/ /_/ / /__/ /_/ / /_/ /
\\____/\\__,_/\\___/\\__,_/\\____/  {DIM}v2{RESET}
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
    except (OSError, socket.error):
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
) -> None:
    """Print the startup banner with a random chocolate fact."""
    print(LOGO)
    print(f"  {BOLD}App:{RESET}        {app_file}")
    print(f"  {BOLD}URL:{RESET}        {CYAN}http://{host}:{port}{RESET}")
    if year_significance:
        print(f"  {BOLD}Port:{RESET}       {DIM}{port} - {year_significance}{RESET}")
    print(f"  {BOLD}Hot reload:{RESET} {GREEN}enabled{RESET}" if reload else f"  {BOLD}Hot reload:{RESET} {DIM}disabled{RESET}")
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
    if hasattr(module, 'app'):
        app = getattr(module, 'app')
        if hasattr(app, 'run') and hasattr(app, '_pages'):
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
        print(f"{YELLOW}Warning: watchfiles not installed. Install with: pip install watchfiles{RESET}")
        print(f"{DIM}Running without hot reload...{RESET}")
        run_without_reload(app_path, host, port, verbose)
        return

    app_dir = app_path.parent.resolve()

    def run_app() -> subprocess.Popen:
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
        for changes in watchfiles.watch(app_dir, watch_filter=lambda _, path: path.endswith('.py')):
            changed_files = [str(c[1]) for c in changes]

            # Print reload message
            print()
            print(f"{YELLOW}Detected changes in:{RESET}")
            for f in changed_files:
                rel_path = os.path.relpath(f, app_dir)
                print(f"  {DIM}{rel_path}{RESET}")
            print(f"{CYAN}Reloading...{RESET}")

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

    parser = argparse.ArgumentParser(
        prog="cacao run",
        description="Run a Cacao v2 application"
    )
    parser.add_argument("app_file", help="Path to the app file (e.g., app.py)")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to (default: 127.0.0.1)")
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=default_port,
        help=f"Port to listen on (default: {default_port}, historic chocolate years)"
    )
    parser.add_argument("--no-reload", action="store_true", help="Disable hot reload")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")

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

    # Find an available port (auto-increment through chocolate years if needed)
    try:
        port, year_significance = find_available_port(parsed_args.host, parsed_args.port)
        if port != parsed_args.port:
            print(f"{YELLOW}Port {parsed_args.port} is in use, using port {port} instead{RESET}")
    except RuntimeError as e:
        print(f"{RED}Error: {e}{RESET}")
        sys.exit(1)

    # Print banner
    print_banner(
        host=parsed_args.host,
        port=port,
        reload=hot_reload,
        app_file=str(app_path.resolve()),
        year_significance=year_significance,
    )

    try:
        if hot_reload:
            run_with_reload(app_path, parsed_args.host, port, parsed_args.verbose)
        else:
            run_without_reload(app_path, parsed_args.host, port, parsed_args.verbose)
    except KeyboardInterrupt:
        print(f"\n{DIM}Server stopped{RESET}")
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        if parsed_args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def create_command(args: list[str]) -> None:
    """
    Create a new Cacao v2 project.

    Usage: cacao create [name] [--template <template>]
    """
    parser = argparse.ArgumentParser(
        prog="cacao create",
        description="Create a new Cacao v2 project"
    )
    parser.add_argument("name", nargs="?", help="Project name")
    parser.add_argument("-t", "--template", choices=["minimal", "counter", "dashboard"],
                        default="minimal", help="Template to use")
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
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', project_name):
        print(f"{RED}Error: Project name can only contain letters, numbers, hyphens, and underscores{RESET}")
        sys.exit(1)

    project_path = Path.cwd() / project_name

    if project_path.exists():
        print(f"{RED}Error: Directory '{project_name}' already exists{RESET}")
        sys.exit(1)

    print(f"\nCreating project '{project_name}' with '{parsed_args.template}' template...")

    try:
        # Create project structure
        project_path.mkdir(parents=True)

        # Get template content
        template_content = _get_template(parsed_args.template)

        # Write app.py
        app_file = project_path / "app.py"
        app_file.write_text(template_content, encoding="utf-8")

        # Write requirements.txt
        requirements = project_path / "requirements.txt"
        requirements.write_text("cacao\nuvicorn\nwatchfiles\n", encoding="utf-8")

        print(f"\n{GREEN}Project created successfully!{RESET}")
        print(f"\nNext steps:")
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
    }
    return templates.get(template_name, templates["minimal"])


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
        prog="cacao build",
        description="Build a static Cacao application"
    )
    parser.add_argument("app_file", help="Path to the app file (e.g., app.py)")
    parser.add_argument("-o", "--output", default="dist", help="Output directory (default: dist)")
    parser.add_argument("--base-path", default="", help="Base path for deployment (e.g., /my-repo for GitHub Pages)")
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
        print(f"{RED}Error: Frontend not built. Run 'npm run build' in cacao/frontend first.{RESET}")
        sys.exit(1)

    # Copy CSS and JS
    shutil.copy(frontend_dist / "cacao.css", output_dir / "cacao.css")
    shutil.copy(frontend_dist / "cacao.js", output_dir / "cacao.js")

    if parsed_args.verbose:
        print(f"  Copied cacao.css and cacao.js (includes built-in handlers)")

    # Generate index.html
    metadata = export_data.get("metadata", {})
    title = metadata.get("title", "Cacao App")
    theme = metadata.get("theme", "dark")

    # Serialize pages data
    pages_json = json.dumps({
        "pages": export_data.get("pages", {}),
        "metadata": metadata,
    })
    signals_json = json.dumps(export_data.get("signals", {}))

    # Build the HTML
    base_path = parsed_args.base_path.rstrip("/")

    html_content = f'''<!DOCTYPE html>
<html lang="en" data-theme="{theme}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="{base_path}/cacao.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
</head>
<body>
    <div id="root"><div class="loading">Loading...</div></div>

    <script>
    // Static mode configuration
    window.__CACAO_STATIC__ = true;
    window.__CACAO_DEFER_MOUNT__ = true;
    window.__CACAO_BASE_PATH__ = "{base_path}";
    window.__CACAO_PAGES__ = {pages_json};
    window.__CACAO_INITIAL_SIGNALS__ = {signals_json};
    </script>

    <script src="{base_path}/cacao.js"></script>

    <script>
    // Initialize static mode and mount (handlers are built into cacao.js)
    (function() {{
        Cacao.initStatic({{
            pages: window.__CACAO_PAGES__,
            signals: window.__CACAO_INITIAL_SIGNALS__,
            handlers: {{}}
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
    print(f"  - index.html")
    print(f"  - 404.html (for SPA routing)")
    print(f"  - cacao.css")
    print(f"  - cacao.js (includes built-in handlers)")
    print()
    print(f"To preview locally:")
    print(f"  {CYAN}python -m http.server -d {output_dir}{RESET}")
    print()


def version_command(args: list[str]) -> None:
    """Show version information."""
    print(f"Cacao v2 CLI")
    print(f"Python: {sys.version}")


def help_command(args: list[str]) -> None:
    """Show help information."""
    print(LOGO)
    print("Usage: cacao <command> [options]")
    print()
    print("Commands:")
    print(f"  {CYAN}run{RESET} <app.py>     Run a Cacao application with hot reload")
    print(f"  {CYAN}build{RESET} <app.py>   Build a static site (for GitHub Pages, etc.)")
    print(f"  {CYAN}create{RESET} [name]    Create a new Cacao project")
    print(f"  {CYAN}version{RESET}          Show version information")
    print(f"  {CYAN}help{RESET}             Show this help message")
    print()
    print("Examples:")
    print(f"  cacao run app.py              Run app with hot reload (default port: 1502)")
    print(f"  cacao run app.py --port 1847  Run on port 1847 (year of first chocolate bar)")
    print(f"  cacao run app.py --no-reload  Run without hot reload")
    print(f"  cacao create my-dashboard     Create a new project")
    print()
    print(f"  {BOLD}Static builds:{RESET}")
    print(f"  cacao build app.py                     Build static site to dist/")
    print(f"  cacao build app.py --base-path /repo   Set base path for GitHub Pages")
    print()
    print(f"{DIM}Ports are historic chocolate years (1502-1936). If in use, auto-increments to next year.{RESET}")
    print()


# Command registry
COMMANDS: dict[str, Callable[[list[str]], None]] = {
    "run": run_command,
    "build": build_command,
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
        print(f"Run 'cacao help' for usage information")
        sys.exit(1)


def main() -> None:
    """Alias for run_cli."""
    run_cli()


if __name__ == "__main__":
    main()
