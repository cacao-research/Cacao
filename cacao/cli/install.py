"""
CLI commands for the Cacao extension system.

Provides ``cacao install``, ``cacao uninstall``, and ``cacao extensions``
commands for managing community extensions, themes, and handler plugins.
"""

from __future__ import annotations

import argparse
import sys

# ANSI color codes (matching commands.py)
BROWN = "\033[38;5;130m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def install_command(args: list[str]) -> None:
    """Install a Cacao extension or theme from PyPI.

    Usage:
        cacao install <extension>          Install an extension
        cacao install <extension> --upgrade Upgrade an extension
        cacao install --theme <name>       Install a marketplace theme
    """
    parser = argparse.ArgumentParser(
        prog="cacao install",
        description="Install a Cacao extension or theme",
    )
    parser.add_argument("name", nargs="?", help="Extension name (e.g. 'my-widget' or 'cacao-my-widget')")
    parser.add_argument("--upgrade", "-U", action="store_true", help="Upgrade if already installed")
    parser.add_argument("--theme", metavar="THEME", help="Install a theme from the marketplace")

    parsed = parser.parse_args(args)

    if parsed.theme:
        _install_theme(parsed.theme)
        return

    if not parsed.name:
        parser.print_help()
        sys.exit(1)

    _install_extension(parsed.name, upgrade=parsed.upgrade)


def _install_extension(name: str, *, upgrade: bool = False) -> None:
    """Install an extension package."""
    from cacao.extensions import install_extension

    pkg = name if name.startswith("cacao-") else f"cacao-{name}"
    action = "Upgrading" if upgrade else "Installing"
    print(f"{CYAN}{action} extension: {pkg}...{RESET}")

    if install_extension(name, upgrade=upgrade):
        print(f"  {GREEN}Successfully installed {pkg}{RESET}")
        print()

        # Try to discover the extension
        from cacao.extensions import discover_extensions

        exts = discover_extensions()
        ext_name = name.removeprefix("cacao-")
        if ext_name in exts:
            info = exts[ext_name]
            print(f"  Extension: {BOLD}{info.name}{RESET} v{info.version}")
            if info.description:
                print(f"  {info.description}")
        print()
        print(f"  The extension will be loaded automatically when your app starts.")
        print(f"  You can verify with: {CYAN}cacao extensions{RESET}")
    else:
        print(f"  {RED}Failed to install {pkg}{RESET}")
        print(f"  Make sure the package exists on PyPI: pip install {pkg}")
        sys.exit(1)


def _install_theme(name: str) -> None:
    """Install a marketplace theme."""
    from cacao.extensions import get_marketplace_themes, install_theme

    # Check if it's a built-in theme
    themes = get_marketplace_themes()
    builtin = next((t for t in themes if t.name == name), None)

    if builtin:
        print(f"{GREEN}Theme '{name}' is a built-in community theme — ready to use!{RESET}")
        print()
        print(f"  {BOLD}{builtin.display_name}{RESET}")
        if builtin.description:
            print(f"  {builtin.description}")
        if builtin.preview_colors:
            print(f"  Colors: {', '.join(builtin.preview_colors)}")
        print()
        print(f"  Use it with: {CYAN}c.config(theme=\"{name}\"){RESET}")
        return

    print(f"{CYAN}Installing theme: {name}...{RESET}")
    if install_theme(name):
        print(f"  {GREEN}Theme '{name}' installed{RESET}")
        print(f"  Use it with: {CYAN}c.config(theme=\"{name}\"){RESET}")
    else:
        print(f"  {RED}Theme '{name}' not found{RESET}")
        print(f"  Available themes: {CYAN}cacao extensions --themes{RESET}")
        sys.exit(1)


def uninstall_command(args: list[str]) -> None:
    """Uninstall a Cacao extension.

    Usage: cacao uninstall <extension>
    """
    parser = argparse.ArgumentParser(
        prog="cacao uninstall",
        description="Uninstall a Cacao extension",
    )
    parser.add_argument("name", help="Extension name to uninstall")

    parsed = parser.parse_args(args)

    from cacao.extensions import uninstall_extension

    pkg = parsed.name if parsed.name.startswith("cacao-") else f"cacao-{parsed.name}"
    print(f"{CYAN}Uninstalling: {pkg}...{RESET}")

    if uninstall_extension(parsed.name):
        print(f"  {GREEN}Successfully uninstalled {pkg}{RESET}")
    else:
        print(f"  {RED}Failed to uninstall {pkg}{RESET}")
        sys.exit(1)


def extensions_command(args: list[str]) -> None:
    """List installed extensions and available themes.

    Usage:
        cacao extensions              List installed extensions
        cacao extensions --themes     Show theme marketplace
        cacao extensions --handlers   Show registered handler plugins
        cacao extensions --create <name>  Create extension template
    """
    parser = argparse.ArgumentParser(
        prog="cacao extensions",
        description="Manage Cacao extensions",
    )
    parser.add_argument("--themes", action="store_true", help="Show theme marketplace")
    parser.add_argument("--handlers", action="store_true", help="Show registered handler plugins")
    parser.add_argument("--create", metavar="NAME", help="Create a new extension template")

    parsed = parser.parse_args(args)

    if parsed.create:
        _create_extension(parsed.create)
        return

    if parsed.themes:
        _show_themes()
        return

    if parsed.handlers:
        _show_handlers()
        return

    _show_extensions()


def _show_extensions() -> None:
    """List installed extensions."""
    from cacao.extensions import discover_extensions

    extensions = discover_extensions()

    print(f"\n{BOLD}Installed Extensions{RESET}")
    print(f"{'-' * 50}")

    if not extensions:
        print(f"  {DIM}No extensions installed{RESET}")
        print()
        print(f"  Install one with: {CYAN}cacao install <name>{RESET}")
        print(f"  Create your own:  {CYAN}cacao extensions --create my-ext{RESET}")
    else:
        for name, info in extensions.items():
            print(f"  {GREEN}{name}{RESET} v{info.version}")
            if info.description:
                print(f"    {DIM}{info.description}{RESET}")
        print()
        print(f"  {DIM}{len(extensions)} extension(s) installed{RESET}")

    print()


def _show_themes() -> None:
    """Show the theme marketplace."""
    from cacao.extensions import get_marketplace_themes

    themes = get_marketplace_themes()

    print(f"\n{BOLD}Theme Marketplace{RESET}")
    print(f"{'-' * 50}")

    for theme in themes:
        tags_str = f" [{', '.join(theme.tags)}]" if theme.tags else ""
        print(f"  {CYAN}{theme.display_name}{RESET} ({theme.name}){DIM}{tags_str}{RESET}")
        if theme.description:
            print(f"    {theme.description}")
        if theme.preview_colors:
            print(f"    Preview: {' '.join(theme.preview_colors)}")
        print()

    print(f"  {DIM}Use a theme: c.config(theme=\"<name>\"){RESET}")
    print(f"  {DIM}Install external: cacao install --theme <name>{RESET}")
    print()


def _show_handlers() -> None:
    """Show registered handler plugins."""
    from cacao.extensions import get_handler_plugins

    plugins = get_handler_plugins()

    print(f"\n{BOLD}Handler Plugins (Static Builds){RESET}")
    print(f"{'-' * 50}")

    # Always show built-in handlers
    print(f"  {GREEN}built-in{RESET} (always available)")
    print(f"    encoders: base64, url, html, jwt, hex, csv")
    print(f"    generators: uuid, password, lorem, random")
    print(f"    converters: yaml, case, number bases")
    print(f"    text: stats, regex, reverse, word wrap")
    print(f"    crypto: sha256, md5, hmac")
    print()

    if plugins:
        for name, data in plugins.items():
            handler_count = len(data.get("handlers", {}))
            desc = data.get("description", "")
            print(f"  {GREEN}{name}{RESET} ({handler_count} handlers)")
            if desc:
                print(f"    {DIM}{desc}{RESET}")
            handler_names = list(data.get("handlers", {}).keys())
            if handler_names:
                print(f"    {', '.join(handler_names)}")
            print()
    else:
        print(f"  {DIM}No handler plugins registered{RESET}")
        print()

    print(f"  {DIM}Register handlers: c.register_handler_plugin(name, handlers){RESET}")
    print()


def _create_extension(name: str) -> None:
    """Create a new extension template."""
    from cacao.extensions import create_extension_template

    print(f"{CYAN}Creating extension template: {name}...{RESET}")

    ext_dir = create_extension_template(name)

    print(f"  {GREEN}Created extension at: {ext_dir}{RESET}")
    print()
    print("  Files created:")
    print(f"    {ext_dir}/pyproject.toml")
    pkg_name = name.replace("-", "_")
    print(f"    {ext_dir}/{pkg_name}/__init__.py")
    print()
    print("  Next steps:")
    dir_name = f"cacao-{name}" if not name.startswith("cacao-") else name
    print(f"    1. cd {dir_name}")
    print(f"    2. Edit {pkg_name}/__init__.py to add your extension logic")
    print(f"    3. pip install -e .     (install locally for development)")
    print(f"    4. cacao extensions     (verify it's loaded)")
    print()
