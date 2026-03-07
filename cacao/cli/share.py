"""
One-command sharing for Cacao apps.

Exposes a local Cacao app via a public tunnel URL with optional
password protection, auto-expiry, and QR code display.

Uses Cloudflare's `cloudflared` quick tunnels (free, no account needed).
Falls back to pyngrok if available.
"""

from __future__ import annotations

import argparse
import atexit
import hashlib
import os
import platform
import re
import stat
import subprocess
import sys
import threading
import time
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

from .commands import (
    BOLD,
    CYAN,
    DARK_BROWN,
    DIM,
    GREEN,
    RED,
    RESET,
    YELLOW,
    _get_logo,
    find_app_instance,
    find_available_port,
    load_app_module,
)

# Directory for cached binaries
CACAO_BIN_DIR = Path.home() / ".cacao" / "bin"

# Cloudflared download URLs per platform
_CLOUDFLARED_URLS: dict[str, str] = {
    "windows-amd64": "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe",
    "linux-amd64": "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64",
    "linux-arm64": "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64",
    "darwin-amd64": "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz",
    "darwin-arm64": "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz",
}


def _get_platform_key() -> str:
    """Get the platform key for cloudflared downloads."""
    system = platform.system().lower()
    machine = platform.machine().lower()

    if machine in ("x86_64", "amd64"):
        arch = "amd64"
    elif machine in ("aarch64", "arm64"):
        arch = "arm64"
    else:
        arch = "amd64"  # Fallback

    return f"{system}-{arch}"


def _find_cloudflared() -> str | None:
    """Find cloudflared binary — in PATH or cached in ~/.cacao/bin/."""
    # Check PATH first
    for name in ("cloudflared", "cloudflared.exe"):
        from shutil import which

        path = which(name)
        if path:
            return path

    # Check cached binary
    suffix = ".exe" if platform.system() == "Windows" else ""
    cached = CACAO_BIN_DIR / f"cloudflared{suffix}"
    if cached.exists():
        return str(cached)

    return None


def _download_cloudflared() -> str:
    """Download cloudflared to ~/.cacao/bin/ and return the path."""
    key = _get_platform_key()
    url = _CLOUDFLARED_URLS.get(key)
    if not url:
        raise RuntimeError(f"No cloudflared binary available for {key}")

    CACAO_BIN_DIR.mkdir(parents=True, exist_ok=True)

    suffix = ".exe" if platform.system() == "Windows" else ""
    target = CACAO_BIN_DIR / f"cloudflared{suffix}"

    print(f"  {DIM}Downloading cloudflared...{RESET}")

    if url.endswith(".tgz"):
        # macOS: download tgz, extract
        import tarfile

        tgz_path = CACAO_BIN_DIR / "cloudflared.tgz"
        urllib.request.urlretrieve(url, str(tgz_path))
        with tarfile.open(str(tgz_path), "r:gz") as tf:
            tf.extractall(str(CACAO_BIN_DIR))
        tgz_path.unlink(missing_ok=True)
    elif url.endswith(".zip"):
        zip_path = CACAO_BIN_DIR / "cloudflared.zip"
        urllib.request.urlretrieve(url, str(zip_path))
        with zipfile.ZipFile(str(zip_path)) as zf:
            zf.extractall(str(CACAO_BIN_DIR))
        zip_path.unlink(missing_ok=True)
    else:
        # Direct binary download (Linux, Windows .exe)
        urllib.request.urlretrieve(url, str(target))

    # Make executable on Unix
    if platform.system() != "Windows":
        target.chmod(target.stat().st_mode | stat.S_IEXEC)

    print(f"  {GREEN}Downloaded to {target}{RESET}")
    return str(target)


def _ensure_cloudflared() -> str | None:
    """Find or download cloudflared. Returns path or None on failure."""
    path = _find_cloudflared()
    if path:
        return path

    try:
        return _download_cloudflared()
    except Exception as e:
        print(f"  {YELLOW}Could not download cloudflared: {e}{RESET}")
        return None


class TunnelProcess:
    """Manages a cloudflared tunnel subprocess."""

    def __init__(self, binary: str, local_port: int) -> None:
        self.binary = binary
        self.local_port = local_port
        self.process: subprocess.Popen[str] | None = None
        self.public_url: str | None = None

    def start(self) -> str:
        """Start the tunnel and return the public URL."""
        self.process = subprocess.Popen(
            [
                self.binary,
                "tunnel",
                "--url",
                f"http://127.0.0.1:{self.local_port}",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        # Parse the output to find the public URL
        url_pattern = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")
        deadline = time.monotonic() + 30  # 30s timeout

        assert self.process.stdout is not None
        while time.monotonic() < deadline:
            line = self.process.stdout.readline()
            if not line:
                if self.process.poll() is not None:
                    raise RuntimeError("cloudflared exited unexpectedly")
                continue

            match = url_pattern.search(line)
            if match:
                self.public_url = match.group(0)
                return self.public_url

        raise RuntimeError("Timed out waiting for cloudflared tunnel URL")

    def stop(self) -> None:
        """Stop the tunnel process."""
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()


class PyngrokTunnel:
    """Manages a pyngrok tunnel."""

    def __init__(self, local_port: int) -> None:
        self.local_port = local_port
        self.tunnel: Any = None

    def start(self) -> str:
        """Start the tunnel and return the public URL."""
        from pyngrok import ngrok

        self.tunnel = ngrok.connect(self.local_port, "http")
        return str(self.tunnel.public_url)

    def stop(self) -> None:
        """Stop the tunnel."""
        if self.tunnel:
            try:
                from pyngrok import ngrok

                ngrok.disconnect(self.tunnel.public_url)
            except Exception:
                pass


def _create_tunnel(local_port: int) -> TunnelProcess | PyngrokTunnel:
    """Create a tunnel using the best available provider."""
    # Try cloudflared first
    cloudflared_path = _ensure_cloudflared()
    if cloudflared_path:
        return TunnelProcess(cloudflared_path, local_port)

    # Try pyngrok
    try:
        import pyngrok  # noqa: F401

        return PyngrokTunnel(local_port)
    except ImportError:
        pass

    raise RuntimeError(
        "No tunnel provider found.\n\n"
        "Install cloudflared (recommended, free, no signup):\n"
        "  Windows:  winget install cloudflare.cloudflared\n"
        "  macOS:    brew install cloudflared\n"
        "  Linux:    See https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/\n\n"
        "Or install pyngrok (requires ngrok account):\n"
        "  pip install pyngrok\n"
        "  ngrok config add-authtoken <your-token>"
    )


def _print_qr_terminal(url: str) -> None:
    """Print a QR code in the terminal using the qrcode library."""
    try:
        import qrcode  # type: ignore[import-untyped]

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=1,
        )
        qr.add_data(url)
        qr.make(fit=True)

        matrix = qr.get_matrix()
        rows = len(matrix)

        # Try Unicode half-blocks first, fall back to ASCII on encoding errors
        try:
            lines: list[str] = []
            for r in range(0, rows, 2):
                line = "  "
                for c in range(len(matrix[0])):
                    top = matrix[r][c]
                    bottom = matrix[r + 1][c] if r + 1 < rows else False
                    if top and bottom:
                        line += "\u2588"  # Full block
                    elif top:
                        line += "\u2580"  # Upper half
                    elif bottom:
                        line += "\u2584"  # Lower half
                    else:
                        line += " "
                lines.append(line)
            # Test encoding before printing
            for line in lines:
                line.encode(sys.stdout.encoding or "utf-8")
            print()
            for line in lines:
                print(line)
            print()
        except (UnicodeEncodeError, UnicodeDecodeError):
            # ASCII fallback: ## for dark, spaces for light
            print()
            for r in range(rows):
                line = "  "
                for c in range(len(matrix[0])):
                    line += "##" if matrix[r][c] else "  "
                print(line)
            print()

    except ImportError:
        # Fallback: print a link to online QR generator
        from urllib.parse import urlencode

        params = urlencode({"data": url, "size": "300x300"})
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?{params}"
        print(f"\n  {DIM}QR Code: {qr_url}{RESET}\n")
        print(f"  {DIM}Tip: pip install qrcode for in-terminal QR codes{RESET}\n")


def _add_password_middleware(app: Any, password: str) -> None:
    """Add basic password protection middleware to the Starlette app."""
    import base64

    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.requests import Request
    from starlette.responses import Response

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    class PasswordMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next: Any) -> Response:
            # Allow WebSocket connections that already authenticated
            if request.url.path == "/ws":
                resp: Response = await call_next(request)
                return resp

            # Allow health check
            if request.url.path == "/health":
                resp = await call_next(request)
                return resp

            # Check for auth cookie
            token = request.cookies.get("cacao_share_token")
            if token and hashlib.sha256(token.encode()).hexdigest() == password_hash:
                resp = await call_next(request)
                return resp

            # Check for password in query param (for initial access)
            query_password = request.query_params.get("password")
            if (
                query_password
                and hashlib.sha256(query_password.encode()).hexdigest() == password_hash
            ):
                response: Response = await call_next(request)
                response.set_cookie(
                    "cacao_share_token", query_password, httponly=True, max_age=86400
                )
                return response

            # Check for Basic Auth header
            auth = request.headers.get("authorization", "")
            if auth.startswith("Basic "):
                try:
                    decoded = base64.b64decode(auth[6:]).decode()
                    _, pwd = decoded.split(":", 1)
                    if hashlib.sha256(pwd.encode()).hexdigest() == password_hash:
                        resp = await call_next(request)
                        return resp
                except Exception:
                    pass

            # Show login page
            return Response(
                content=_get_login_page(),
                media_type="text/html",
                status_code=401,
            )

    app.add_middleware(PasswordMiddleware)


def _get_login_page() -> str:
    """Return a simple login page HTML."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Required</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', system-ui, sans-serif;
            background: #1a1a2e;
            color: #e0e0e0;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        .card {
            background: #16213e;
            border: 1px solid #2a2a4a;
            border-radius: 12px;
            padding: 2rem;
            width: 100%;
            max-width: 360px;
            text-align: center;
        }
        h2 { margin-bottom: 0.5rem; color: #fff; font-size: 1.25rem; }
        p { margin-bottom: 1.5rem; color: #888; font-size: 0.875rem; }
        input {
            width: 100%;
            padding: 0.75rem 1rem;
            border: 1px solid #2a2a4a;
            border-radius: 8px;
            background: #0f3460;
            color: #fff;
            font-size: 1rem;
            margin-bottom: 1rem;
            outline: none;
        }
        input:focus { border-color: #e94560; }
        button {
            width: 100%;
            padding: 0.75rem;
            border: none;
            border-radius: 8px;
            background: #e94560;
            color: #fff;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
        }
        button:hover { background: #c73e54; }
        .error { color: #e94560; font-size: 0.8rem; margin-top: 0.5rem; display: none; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Password Required</h2>
        <p>This shared Cacao app is password-protected.</p>
        <form id="form">
            <input type="password" id="pwd" placeholder="Enter password" autofocus>
            <button type="submit">Access App</button>
        </form>
        <div class="error" id="err">Incorrect password</div>
    </div>
    <script>
        document.getElementById('form').addEventListener('submit', function(e) {
            e.preventDefault();
            var pwd = document.getElementById('pwd').value;
            var loc = window.location.pathname;
            window.location.href = loc + '?password=' + encodeURIComponent(pwd);
        });
        if (window.location.search.includes('password=')) {
            document.getElementById('err').style.display = 'block';
        }
    </script>
</body>
</html>"""


def share_command(args: list[str]) -> None:
    """
    Share a Cacao app via a public tunnel URL.

    Usage: cacao share app.py [options]
    """
    parser = argparse.ArgumentParser(
        prog="cacao share",
        description="Share a Cacao app via public URL",
    )
    parser.add_argument("app_file", help="Path to the app file (e.g., app.py)")
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=None,
        help="Local port (auto-selected if not specified)",
    )
    parser.add_argument(
        "--password",
        type=str,
        default=None,
        help="Password to protect the shared app",
    )
    parser.add_argument(
        "--expire",
        type=float,
        default=72,
        help="Auto-expire after N hours (default: 72, 0 = never)",
    )
    parser.add_argument(
        "--no-qr",
        action="store_true",
        help="Don't display QR code",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    parsed = parser.parse_args(args)
    app_path = Path(parsed.app_file)

    # Validate
    if not app_path.exists():
        print(f"{RED}Error: File '{parsed.app_file}' not found{RESET}")
        sys.exit(1)

    if not app_path.suffix == ".py":
        print(f"{RED}Error: '{parsed.app_file}' is not a Python file{RESET}")
        sys.exit(1)

    # Find a port
    host = "127.0.0.1"
    try:
        port, _ = find_available_port(host, parsed.port or 1502)
    except RuntimeError as e:
        print(f"{RED}Error: {e}{RESET}")
        sys.exit(1)

    # Generate password if not provided (offer auto-generated option)
    password = parsed.password

    # Print banner
    print(_get_logo())
    print(f"  {DARK_BROWN}{'Sharing':<12}{RESET}{app_path.resolve()}")
    print(f"  {DARK_BROWN}{'Local':<12}{RESET}{CYAN}http://{host}:{port}{RESET}")

    if password:
        print(f"  {DARK_BROWN}{'Password':<12}{RESET}{GREEN}enabled{RESET}")

    expire_str = f"{parsed.expire}h" if parsed.expire > 0 else "never"
    print(f"  {DARK_BROWN}{'Expires':<12}{RESET}{expire_str}")
    print()

    # Create tunnel
    print(f"  {DIM}Starting tunnel...{RESET}")

    try:
        tunnel = _create_tunnel(port)
    except RuntimeError as e:
        print(f"{RED}Error: {e}{RESET}")
        sys.exit(1)

    # Load and prepare the app
    app_dir = app_path.parent.resolve()
    original_cwd = os.getcwd()
    os.chdir(app_dir)

    try:
        module = load_app_module(app_path)
        app_instance = find_app_instance(module)
    finally:
        os.chdir(original_cwd)

    # Create Starlette server
    from cacao.server.server import create_server

    starlette_app = create_server(app_instance)

    # Add password middleware if requested
    if password:
        _add_password_middleware(starlette_app, password)

    # Start tunnel
    try:
        public_url = tunnel.start()
    except Exception as e:
        print(f"{RED}Error starting tunnel: {e}{RESET}")
        sys.exit(1)

    # Register cleanup
    def cleanup() -> None:
        tunnel.stop()
        print(f"\n  {DIM}Tunnel closed{RESET}")

    atexit.register(cleanup)

    # Print share info
    share_url = public_url
    if password:
        share_url_with_pw = f"{public_url}?password={password}"
    else:
        share_url_with_pw = None

    print(f"\n  {BOLD}{GREEN}Shared successfully!{RESET}")
    print()
    print(f"  {DARK_BROWN}{'Public URL':<12}{RESET}{BOLD}{CYAN}{share_url}{RESET}")

    if share_url_with_pw:
        print(f"  {DARK_BROWN}{'With auth':<12}{RESET}{DIM}{share_url_with_pw}{RESET}")

    # QR code
    if not parsed.no_qr:
        _print_qr_terminal(share_url_with_pw or share_url)

    # Expire timer
    if parsed.expire > 0:
        expire_seconds = parsed.expire * 3600

        def expire_handler() -> None:
            print(f"\n  {YELLOW}Share expired after {parsed.expire}h. Shutting down...{RESET}")
            tunnel.stop()
            os._exit(0)

        timer = threading.Timer(expire_seconds, expire_handler)
        timer.daemon = True
        timer.start()

    print(f"  {DIM}Press Ctrl+C to stop sharing{RESET}")
    print()

    # Start the server (blocking)
    import uvicorn

    from cacao.server.log import get_uvicorn_log_config

    log_config = get_uvicorn_log_config(debug=app_instance.debug)

    try:
        uvicorn.run(
            starlette_app,
            host=host,
            port=port,
            log_config=log_config,
        )
    except KeyboardInterrupt:
        pass
    finally:
        tunnel.stop()
        print(f"\n{DIM}Share stopped{RESET}")
