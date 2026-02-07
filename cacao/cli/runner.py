"""
Internal runner for Cacao v2 hot reload.

This module is invoked as a subprocess by the CLI when hot reload is enabled.
It reads configuration from environment variables.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from typing import Any


def load_app_module(app_path: Path) -> Any:
    """Load a Python module from a file path."""
    app_dir = app_path.parent.resolve()
    if str(app_dir) not in sys.path:
        sys.path.insert(0, str(app_dir))

    spec = importlib.util.spec_from_file_location("__cacao_app__", app_path.resolve())
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {app_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def find_app_instance(module: Any) -> Any:
    """Find the Cacao App instance in a module."""
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

    raise RuntimeError("No Cacao App instance found in module.")


def main() -> None:
    """Run the app from environment variables."""
    app_file = os.environ.get("CACAO_APP_FILE")
    if not app_file:
        print("Error: CACAO_APP_FILE environment variable not set")
        sys.exit(1)

    host = os.environ.get("CACAO_HOST", "127.0.0.1")
    port = int(os.environ.get("CACAO_PORT", "8000"))
    verbose = os.environ.get("CACAO_VERBOSE", "0") == "1"

    app_path = Path(app_file)

    try:
        module = load_app_module(app_path)
        app = find_app_instance(module)

        if verbose:
            app.debug = True

        # Run without uvicorn's reload (we handle it externally)
        app.run(host=host, port=port, reload=False)

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
