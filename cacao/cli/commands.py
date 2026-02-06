"""
Command registry for the Cacao CLI.
Defines available CLI commands and their handlers.
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Callable, Dict, List

COMMANDS: Dict[str, Callable] = {}

def register_command(name: str) -> Callable:
    """
    Decorator to register a new CLI command.
    """
    def decorator(func: Callable) -> Callable:
        COMMANDS[name] = func
        return func
    return decorator

@register_command("serve")
def serve_command(args: List[str]) -> None:
    """
    Run the development server with hot reload.
    """
    parser = argparse.ArgumentParser(description="Run the Cacao development server")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--host", default="localhost", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=1634, help="Port for the HTTP server")
    parser.add_argument("--ws-port", type=int, default=1633, help="Port for the WebSocket server")
    parser.add_argument("--pwa", action="store_true", help="Enable Progressive Web App mode")
    
    parsed_args = parser.parse_args(args)
    
    try:
        from cacao.core.server import CacaoServer
        server = CacaoServer(
            host=parsed_args.host,
            http_port=parsed_args.port,
            ws_port=parsed_args.ws_port,
            verbose=parsed_args.verbose,
            enable_pwa=parsed_args.pwa
        )
        print(f"Starting Cacao development server...")
        server.run()
    except ImportError:
        print("Error: Could not import CacaoServer. Make sure Cacao is installed correctly.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        sys.exit(1)
        
@register_command("create")
def create_command(args: List[str]) -> None:
    """
    Create a new Cacao project from a template.
    """
    parser = argparse.ArgumentParser(description="Create a new Cacao project")
    parser.add_argument("name", nargs="?", help="Project name")
    parser.add_argument("-t", "--template", choices=["minimal", "counter", "dashboard"],
                        help="Template to use (minimal, counter, dashboard)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    parsed_args = parser.parse_args(args)

    try:
        from cacao.cli.scaffolding import create_project, interactive_create, TEMPLATES

        # If no name provided, run interactive mode
        if not parsed_args.name:
            success = interactive_create()
            sys.exit(0 if success else 1)

        # If name but no template, prompt for template
        if not parsed_args.template:
            print("\nAvailable templates:")
            template_list = list(TEMPLATES.items())
            for i, (key, info) in enumerate(template_list, 1):
                print(f"  [{i}] {info['name']}: {info['description']}")

            try:
                selection = input(f"\nSelect template [1-{len(template_list)}]: ").strip()
                selection_idx = int(selection) - 1
                if selection_idx < 0 or selection_idx >= len(template_list):
                    raise ValueError()
                template_name = template_list[selection_idx][0]
            except (ValueError, KeyboardInterrupt, EOFError):
                print("Cancelled.")
                sys.exit(1)
        else:
            template_name = parsed_args.template

        # Create the project
        print(f"\nCreating project '{parsed_args.name}' with '{template_name}' template...")

        if create_project(parsed_args.name, template_name, verbose=parsed_args.verbose):
            print(f"\nProject '{parsed_args.name}' created successfully!")
            print("\nNext steps:")
            print(f"  cd {parsed_args.name}")
            print("  pip install -r requirements.txt")
            print("  cacao dev app.py")
            sys.exit(0)
        else:
            sys.exit(1)

    except ImportError as e:
        print(f"Error: Could not import scaffolding module: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


@register_command("dev")
def dev_command(args: List[str]) -> None:
    """
    Run a Cacao v1 application with hot reload enabled.
    For Cacao v2 apps, use 'cacao run' instead.
    """
    parser = argparse.ArgumentParser(description="Run a Cacao v1 app with hot reload")
    parser.add_argument("app_file", help="Path to the app file (e.g., app.py)")
    parser.add_argument("--host", default="localhost", help="Host to bind to")
    parser.add_argument("--port", type=int, default=1634, help="Port for HTTP server")
    parser.add_argument("--ws-port", type=int, default=1633, help="Port for WebSocket server")
    parser.add_argument("--no-reload", action="store_true", help="Disable hot reload")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")

    parsed_args = parser.parse_args(args)

    app_path = Path(parsed_args.app_file)

    if not app_path.exists():
        print(f"Error: File '{parsed_args.app_file}' not found")
        sys.exit(1)

    if not app_path.suffix == ".py":
        print(f"Error: '{parsed_args.app_file}' is not a Python file")
        sys.exit(1)

    # Add the app's directory to sys.path so imports work
    app_dir = app_path.parent.resolve()
    if str(app_dir) not in sys.path:
        sys.path.insert(0, str(app_dir))

    # Change to app directory
    original_cwd = os.getcwd()
    os.chdir(app_dir)

    try:
        import importlib.util

        # Load the app module
        spec = importlib.util.spec_from_file_location("app", app_path.resolve())
        if spec is None or spec.loader is None:
            print(f"Error: Could not load '{parsed_args.app_file}'")
            sys.exit(1)

        module = importlib.util.module_from_spec(spec)
        sys.modules["app"] = module

        hot_reload = not parsed_args.no_reload
        reload_msg = "enabled" if hot_reload else "disabled"

        print(f"Starting Cacao development server...")
        print(f"  App: {app_path.resolve()}")
        print(f"  URL: http://{parsed_args.host}:{parsed_args.port}")
        print(f"  Hot reload: {reload_msg}")
        print()

        # Execute the module
        spec.loader.exec_module(module)

    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error running app: {e}")
        if parsed_args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    finally:
        os.chdir(original_cwd)


@register_command("run")
def run_command(args: List[str]) -> None:
    """
    Run a Cacao v2 application with hot reload.
    This is the recommended way to run modern Cacao apps.
    """
    try:
        from cacao_v2.cli.commands import run_command as v2_run_command
        v2_run_command(args)
    except ImportError as e:
        print(f"Error: Could not import cacao_v2: {e}")
        print("Make sure cacao_v2 is properly installed.")
        sys.exit(1)


@register_command("build-components")
def build_components_command(args: List[str]) -> None:
    """
    Build component JavaScript files into cacao-components.js
    """
    parser = argparse.ArgumentParser(description="Compile modular components into cacao-components.js")
    parser.add_argument('--components-dir', default='cacao/ui/components',
                        help='Directory containing component directories')
    parser.add_argument('--output', default='cacao/core/static/js/cacao-components.js',
                        help='Output path for compiled components file')
    parser.add_argument('--force', action='store_true',
                        help='Force rebuild even if files haven\'t changed')
    parser.add_argument('--verbose', action='store_true',
                        help='Show detailed compilation information')
    
    parsed_args = parser.parse_args(args)
    
    try:
        from cacao.core.component_compiler import compile_components
        
        print(f"🔧 Building components from {parsed_args.components_dir}...")
        print("📝 Automatic function call transformation enabled")
        print("   Direct CacaoCore function calls will be auto-namespaced")
        print("   See docs/COMPONENT_DEVELOPMENT_GUIDE.md for best practices")
        print()
        
        success = compile_components(
            components_dir=parsed_args.components_dir,
            output_path=parsed_args.output,
            force=parsed_args.force,
            verbose=parsed_args.verbose
        )
        
        if success:
            print(f"✅ Component compilation completed successfully")
            print(f"📁 Output: {parsed_args.output}")
        else:
            print(f"❌ Component compilation failed")
            sys.exit(1)
            
    except ImportError as e:
        print(f"Error: Could not import component compiler: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error during compilation: {e}")
        sys.exit(1)


def run_cli() -> None:
    """
    Parse arguments and execute the corresponding CLI command.
    """
    # Handle --help and --version before argparse takes over
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print("Cacao CLI - Build reactive web apps with Python")
        print()
        print("Usage: cacao <command> [options]")
        print()
        print("Commands:")
        print("  run <app.py>        Run a Cacao v2 app with hot reload")
        print("  dev <app.py>        Run a Cacao v1 app")
        print("  create [name]       Create a new project from template")
        print("  serve               Start the development server")
        print("  build-components    Compile UI components")
        print()
        print("Examples:")
        print("  cacao run app.py              Run app with hot reload")
        print("  cacao run app.py --port 3000  Run on custom port")
        print("  cacao create my-app           Create a new project")
        print()
        print("Use 'cacao <command> --help' for more information about a command.")
        return

    if sys.argv[1] in ("--version", "-V"):
        print("Cacao CLI")
        return

    # Parse command and pass remaining args
    command = sys.argv[1]
    remaining_args = sys.argv[2:]

    command_func = COMMANDS.get(command)
    if command_func:
        command_func(remaining_args)
    else:
        print(f"Command '{command}' not recognized.")
        print(f"Available commands: {', '.join(COMMANDS.keys())}")
