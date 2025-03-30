"""
Command registry for the Cacao CLI.
Defines available CLI commands and their handlers.
"""

import argparse
import sys
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

def run_cli() -> None:
    """
    Parse arguments and execute the corresponding CLI command.
    """
    parser = argparse.ArgumentParser(description="Cacao CLI")
    parser.add_argument("command", help="Command to run")
    args, unknown = parser.parse_known_args()

    command_func = COMMANDS.get(args.command)
    if command_func:
        command_func(unknown)
    else:
        print(f"Command '{args.command}' not recognized.")
        print(f"Available commands: {', '.join(COMMANDS.keys())}")
