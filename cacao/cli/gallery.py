"""
App Gallery for Cacao — public registry for discovering and publishing apps.

Supports:
- Local gallery index at ~/.cacao/gallery.json
- Remote gallery fetching from a configurable URL
- Publishing apps with metadata (title, description, tags, URLs)
- Browsing/searching the gallery from CLI
- Embed snippet generation for iframe embedding
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

from .commands import (
    BOLD,
    BROWN,
    CYAN,
    DARK_BROWN,
    DIM,
    GREEN,
    RED,
    RESET,
    YELLOW,
    _get_logo,
    find_app_instance,
    load_app_module,
)

# ---------------------------------------------------------------------------
# Gallery paths & constants
# ---------------------------------------------------------------------------

GALLERY_DIR = Path.home() / ".cacao"
GALLERY_FILE = GALLERY_DIR / "gallery.json"
GALLERY_REMOTE_URL = "https://raw.githubusercontent.com/cacao-research/gallery/main/gallery.json"


# ---------------------------------------------------------------------------
# Gallery entry schema
# ---------------------------------------------------------------------------

def _make_entry(
    *,
    name: str,
    title: str,
    description: str = "",
    author: str = "",
    tags: list[str] | None = None,
    url: str = "",
    source_url: str = "",
    embed_url: str = "",
    thumbnail: str = "",
    published_at: float | None = None,
    version: str = "",
) -> dict[str, Any]:
    """Create a gallery entry dict."""
    entry_id = hashlib.sha256(f"{name}:{author}".encode()).hexdigest()[:12]
    return {
        "id": entry_id,
        "name": name,
        "title": title,
        "description": description,
        "author": author,
        "tags": tags or [],
        "url": url,
        "source_url": source_url,
        "embed_url": embed_url,
        "thumbnail": thumbnail,
        "published_at": published_at or time.time(),
        "version": version,
    }


# ---------------------------------------------------------------------------
# Gallery storage
# ---------------------------------------------------------------------------

def _load_gallery() -> dict[str, Any]:
    """Load the local gallery index."""
    if not GALLERY_FILE.exists():
        return {"apps": [], "updated_at": 0}
    try:
        return json.loads(GALLERY_FILE.read_text(encoding="utf-8"))  # type: ignore[no-any-return]
    except (json.JSONDecodeError, OSError):
        return {"apps": [], "updated_at": 0}


def _save_gallery(gallery: dict[str, Any]) -> None:
    """Save the local gallery index."""
    GALLERY_DIR.mkdir(parents=True, exist_ok=True)
    gallery["updated_at"] = time.time()
    GALLERY_FILE.write_text(
        json.dumps(gallery, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def _fetch_remote_gallery(url: str = GALLERY_REMOTE_URL) -> dict[str, Any] | None:
    """Fetch the remote gallery index. Returns None on failure."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Cacao-CLI"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))  # type: ignore[no-any-return]
    except Exception:
        return None


def _merge_galleries(local: dict[str, Any], remote: dict[str, Any]) -> dict[str, Any]:
    """Merge remote entries into local gallery (remote entries are read-only)."""
    local_ids = {app["id"] for app in local.get("apps", [])}
    merged_apps = list(local.get("apps", []))

    for app in remote.get("apps", []):
        if app["id"] not in local_ids:
            app["_source"] = "remote"
            merged_apps.append(app)

    return {"apps": merged_apps, "updated_at": time.time()}


# ---------------------------------------------------------------------------
# Embed snippet generation
# ---------------------------------------------------------------------------

def generate_embed_snippet(
    url: str,
    width: str = "100%",
    height: str = "600px",
    title: str = "Cacao App",
) -> str:
    """Generate an HTML iframe embed snippet."""
    return (
        f'<iframe\n'
        f'  src="{url}"\n'
        f'  width="{width}"\n'
        f'  height="{height}"\n'
        f'  title="{title}"\n'
        f'  frameborder="0"\n'
        f'  allow="clipboard-write; cross-origin-isolated"\n'
        f'  style="border: 1px solid #2a2a4a; border-radius: 8px;"\n'
        f'></iframe>'
    )


def generate_embed_markdown(url: str, title: str = "Cacao App") -> str:
    """Generate a Markdown-compatible embed reference."""
    return (
        f'<!-- Cacao App Embed -->\n'
        f'<iframe src="{url}" width="100%" height="600" '
        f'title="{title}" frameborder="0" '
        f'style="border: 1px solid #2a2a4a; border-radius: 8px;">'
        f'</iframe>'
    )


# ---------------------------------------------------------------------------
# `cacao publish` command
# ---------------------------------------------------------------------------

def publish_command(args: list[str]) -> None:
    """
    Publish a Cacao app to the gallery.

    Usage: cacao publish app.py [options]

    This command:
    1. Reads app metadata (title, description) from the app file
    2. Optionally builds a static version for hosting
    3. Registers the app in the local gallery (~/.cacao/gallery.json)
    4. Generates an embed snippet for docs/blogs
    """
    parser = argparse.ArgumentParser(
        prog="cacao publish",
        description="Publish a Cacao app to the gallery",
    )
    parser.add_argument("app_file", help="Path to the app file (e.g., app.py)")
    parser.add_argument(
        "--name", type=str, default=None,
        help="App name/slug (auto-detected if omitted)",
    )
    parser.add_argument(
        "--title", type=str, default=None,
        help="Display title (auto-detected if omitted)",
    )
    parser.add_argument(
        "--description", "-d", type=str, default="",
        help="Short description of the app",
    )
    parser.add_argument(
        "--author", "-a", type=str, default="",
        help="Author name",
    )
    parser.add_argument(
        "--tags", type=str, default="",
        help="Comma-separated tags (e.g., dashboard,ml,demo)",
    )
    parser.add_argument(
        "--url", type=str, default="",
        help="Live URL where the app is hosted",
    )
    parser.add_argument(
        "--source", type=str, default="",
        help="Source code URL (e.g., GitHub repo)",
    )
    parser.add_argument(
        "--build", action="store_true",
        help="Build a static version before publishing",
    )
    parser.add_argument(
        "--base-path", type=str, default="",
        help="Base path for static build (used with --build)",
    )
    parser.add_argument(
        "--embed", action="store_true",
        help="Print embed snippet after publishing",
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

    # Print header
    print(_get_logo())
    print(f"  {DARK_BROWN}{'Publishing':<12}{RESET}{app_path.resolve()}")
    print()

    # Detect app metadata
    app_name = parsed.name or app_path.stem.replace("_", "-").lower()
    app_title = parsed.title
    app_version = ""

    try:
        import os

        app_dir = app_path.parent.resolve()
        original_cwd = os.getcwd()
        os.chdir(app_dir)
        try:
            module = load_app_module(app_path)
            app_instance = find_app_instance(module)
            if not app_title and hasattr(app_instance, "_title"):
                app_title = str(app_instance._title)
        finally:
            os.chdir(original_cwd)
    except Exception:
        pass

    if not app_title:
        app_title = app_name.replace("-", " ").replace("_", " ").title()

    try:
        from cacao import __version__

        app_version = __version__
    except ImportError:
        pass

    # Parse tags
    tags = [t.strip() for t in parsed.tags.split(",") if t.strip()] if parsed.tags else []

    # Optionally build static version
    if parsed.build:
        print(f"  {DIM}Building static version...{RESET}")
        from .commands import build_command

        build_args = [parsed.app_file]
        if parsed.base_path:
            build_args.extend(["--base-path", parsed.base_path])
        build_command(build_args)
        print()

    # Determine embed URL
    embed_url = ""
    if parsed.url:
        embed_url = parsed.url

    # Create gallery entry
    entry = _make_entry(
        name=app_name,
        title=app_title,
        description=parsed.description,
        author=parsed.author,
        tags=tags,
        url=parsed.url,
        source_url=parsed.source,
        embed_url=embed_url,
        version=app_version,
    )

    # Load gallery and add/update entry
    gallery = _load_gallery()
    apps = gallery.get("apps", [])

    # Replace existing entry with same name+author, or append
    updated = False
    for i, existing in enumerate(apps):
        if existing.get("name") == app_name and existing.get("author") == parsed.author:
            apps[i] = entry
            updated = True
            break

    if not updated:
        apps.append(entry)

    gallery["apps"] = apps
    _save_gallery(gallery)

    # Print success
    print(f"  {GREEN}Published to gallery!{RESET}")
    print()
    print(f"  {DARK_BROWN}{'Name':<12}{RESET}{app_name}")
    print(f"  {DARK_BROWN}{'Title':<12}{RESET}{app_title}")
    if parsed.description:
        print(f"  {DARK_BROWN}{'Description':<12}{RESET}{parsed.description}")
    if parsed.author:
        print(f"  {DARK_BROWN}{'Author':<12}{RESET}{parsed.author}")
    if tags:
        print(f"  {DARK_BROWN}{'Tags':<12}{RESET}{', '.join(tags)}")
    if parsed.url:
        print(f"  {DARK_BROWN}{'URL':<12}{RESET}{CYAN}{parsed.url}{RESET}")
    if parsed.source:
        print(f"  {DARK_BROWN}{'Source':<12}{RESET}{CYAN}{parsed.source}{RESET}")
    print(f"  {DARK_BROWN}{'Gallery':<12}{RESET}{DIM}{GALLERY_FILE}{RESET}")
    print()

    # Print embed snippet if requested or if URL is available
    if parsed.embed or parsed.url:
        _print_embed_info(parsed.url or "YOUR_APP_URL", app_title)

    print(f"  {DIM}View gallery: cacao gallery{RESET}")
    print()


def _print_embed_info(url: str, title: str) -> None:
    """Print embed snippet information."""
    print(f"  {BOLD}Embed snippet:{RESET}")
    print()
    snippet = generate_embed_snippet(url, title=title)
    for line in snippet.split("\n"):
        print(f"    {DIM}{line}{RESET}")
    print()


# ---------------------------------------------------------------------------
# `cacao gallery` command
# ---------------------------------------------------------------------------

def gallery_command(args: list[str]) -> None:
    """
    Browse the Cacao app gallery.

    Usage: cacao gallery [options]
    """
    parser = argparse.ArgumentParser(
        prog="cacao gallery",
        description="Browse the Cacao app gallery",
    )
    parser.add_argument(
        "search", nargs="?", default=None,
        help="Search term to filter apps",
    )
    parser.add_argument(
        "--tag", "-t", type=str, default=None,
        help="Filter by tag",
    )
    parser.add_argument(
        "--author", "-a", type=str, default=None,
        help="Filter by author",
    )
    parser.add_argument(
        "--remote", action="store_true",
        help="Also fetch apps from the remote gallery",
    )
    parser.add_argument(
        "--json", action="store_true", dest="output_json",
        help="Output as JSON",
    )
    parser.add_argument(
        "--embed", type=str, default=None, metavar="APP_NAME",
        help="Show embed snippet for an app",
    )

    parsed = parser.parse_args(args)

    # Load gallery
    gallery = _load_gallery()

    # Optionally fetch remote
    if parsed.remote:
        print(f"  {DIM}Fetching remote gallery...{RESET}")
        remote = _fetch_remote_gallery()
        if remote:
            gallery = _merge_galleries(gallery, remote)
            print(f"  {GREEN}Merged {len(remote.get('apps', []))} remote app(s){RESET}")
        else:
            print(f"  {YELLOW}Could not fetch remote gallery{RESET}")
        print()

    apps = gallery.get("apps", [])

    # Handle embed snippet request
    if parsed.embed:
        matching = [a for a in apps if a.get("name") == parsed.embed]
        if not matching:
            print(f"{RED}App '{parsed.embed}' not found in gallery{RESET}")
            sys.exit(1)
        app_entry = matching[0]
        url = app_entry.get("url") or app_entry.get("embed_url") or "YOUR_APP_URL"
        title = app_entry.get("title", parsed.embed)
        print()
        _print_embed_info(url, title)
        return

    # Apply filters
    if parsed.search:
        term = parsed.search.lower()
        apps = [
            a for a in apps
            if term in a.get("name", "").lower()
            or term in a.get("title", "").lower()
            or term in a.get("description", "").lower()
            or any(term in tag.lower() for tag in a.get("tags", []))
        ]

    if parsed.tag:
        tag = parsed.tag.lower()
        apps = [a for a in apps if any(tag == t.lower() for t in a.get("tags", []))]

    if parsed.author:
        author = parsed.author.lower()
        apps = [a for a in apps if parsed.author.lower() in a.get("author", "").lower()]

    # Output
    if parsed.output_json:
        print(json.dumps(apps, indent=2, ensure_ascii=False))
        return

    # Print header
    print(_get_logo())
    print(f"  {BOLD}Cacao App Gallery{RESET}")
    print(f"  {DIM}{len(apps)} app(s) found{RESET}")
    print()

    if not apps:
        print(f"  {DIM}No apps in gallery yet.{RESET}")
        print(f"  {DIM}Publish your first app: cacao publish app.py{RESET}")
        print()
        return

    # Sort by published_at descending
    apps.sort(key=lambda a: a.get("published_at", 0), reverse=True)

    for app_entry in apps:
        name = app_entry.get("name", "untitled")
        title = app_entry.get("title", name)
        desc = app_entry.get("description", "")
        author = app_entry.get("author", "")
        tags = app_entry.get("tags", [])
        url = app_entry.get("url", "")
        source_flag = " [remote]" if app_entry.get("_source") == "remote" else ""

        # Title line
        print(f"  {BROWN}{title}{RESET}{DIM}{source_flag}{RESET}")

        # Details
        if desc:
            print(f"    {desc}")
        meta_parts = []
        if author:
            meta_parts.append(f"by {author}")
        if tags:
            meta_parts.append(" ".join(f"#{t}" for t in tags))
        if meta_parts:
            print(f"    {DIM}{' · '.join(meta_parts)}{RESET}")
        if url:
            print(f"    {CYAN}{url}{RESET}")

        # Published date
        published_at = app_entry.get("published_at")
        if published_at:
            from datetime import datetime, timezone

            dt = datetime.fromtimestamp(published_at, tz=timezone.utc)
            print(f"    {DIM}Published {dt.strftime('%Y-%m-%d')}{RESET}")

        print()

    # Footer
    print(f"  {DIM}Publish: cacao publish app.py --url https://your-app.com{RESET}")
    print(f"  {DIM}Embed:   cacao gallery --embed <app-name>{RESET}")
    print()
