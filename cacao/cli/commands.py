"""
CLI commands for Cacao v2.

Provides the main CLI interface for running Cacao applications with hot reload.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
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


def print_banner(host: str, port: int, reload: bool, app_file: str) -> None:
    """Print the startup banner."""
    print(LOGO)
    print(f"  {BOLD}App:{RESET}        {app_file}")
    print(f"  {BOLD}URL:{RESET}        {CYAN}http://{host}:{port}{RESET}")
    print(f"  {BOLD}Hot reload:{RESET} {GREEN}enabled{RESET}" if reload else f"  {BOLD}Hot reload:{RESET} {DIM}disabled{RESET}")
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
    parser = argparse.ArgumentParser(
        prog="cacao run",
        description="Run a Cacao v2 application"
    )
    parser.add_argument("app_file", help="Path to the app file (e.g., app.py)")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to (default: 127.0.0.1)")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Port to listen on (default: 8000)")
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

    # Print banner
    print_banner(
        host=parsed_args.host,
        port=parsed_args.port,
        reload=hot_reload,
        app_file=str(app_path.resolve())
    )

    try:
        if hot_reload:
            run_with_reload(app_path, parsed_args.host, parsed_args.port, parsed_args.verbose)
        else:
            run_without_reload(app_path, parsed_args.host, parsed_args.port, parsed_args.verbose)
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
    print(f"  {CYAN}create{RESET} [name]    Create a new Cacao project")
    print(f"  {CYAN}version{RESET}          Show version information")
    print(f"  {CYAN}help{RESET}             Show this help message")
    print()
    print("Examples:")
    print(f"  cacao run app.py              Run app with hot reload")
    print(f"  cacao run app.py --port 3000  Run on port 3000")
    print(f"  cacao run app.py --no-reload  Run without hot reload")
    print(f"  cacao create my-dashboard     Create a new project")
    print()


# Command registry
COMMANDS: dict[str, Callable[[list[str]], None]] = {
    "run": run_command,
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
