"""Configuration loader for Cacao.

Reads app-level settings from cacao.yaml / cacao.yml files.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

# Keys that map directly to c.config() parameters
_KNOWN_KEYS = {"title", "theme", "host", "port", "debug", "branding"}

# File names to search for, in priority order
_CONFIG_FILENAMES = ["cacao.yaml", "cacao.yml", ".cacao.yaml", ".cacao.yml"]


def find_config_file(search_dir: str | Path | None = None) -> Path | None:
    """Find a cacao.yaml config file.

    Searches the given directory (or cwd) for known config filenames.

    Args:
        search_dir: Directory to search in. Defaults to cwd.

    Returns:
        Path to the config file, or None if not found.
    """
    base = Path(search_dir) if search_dir else Path.cwd()
    for name in _CONFIG_FILENAMES:
        path = base / name
        if path.is_file():
            return path
    return None


def load_config_file(path: str | Path) -> dict[str, Any]:
    """Load and parse a cacao.yaml file.

    Args:
        path: Path to the YAML config file.

    Returns:
        Parsed configuration dictionary.
    """
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    if not isinstance(data, dict):
        return {}

    return data


def extract_app_config(data: dict[str, Any]) -> dict[str, Any]:
    """Extract Cacao app settings from parsed YAML data.

    Only returns keys that c.config() understands, with correct types.

    Args:
        data: Full parsed YAML dictionary.

    Returns:
        Dictionary of validated app config values.
    """
    result: dict[str, Any] = {}

    if "title" in data and isinstance(data["title"], str):
        result["title"] = data["title"]

    if "theme" in data:
        theme = data["theme"]
        # theme can be a string ("dark"/"light"/"auto") or a dict (CacaoDocs-style)
        if isinstance(theme, str) and theme in ("dark", "light", "auto"):
            result["theme"] = theme

    if "host" in data and isinstance(data["host"], str):
        result["host"] = data["host"]

    if "port" in data and isinstance(data["port"], int):
        result["port"] = data["port"]

    if "debug" in data and isinstance(data["debug"], bool):
        result["debug"] = data["debug"]

    if "branding" in data:
        val = data["branding"]
        if isinstance(val, (bool, str)):
            result["branding"] = val

    return result


def load_app_config(search_dir: str | Path | None = None) -> tuple[dict[str, Any], Path | None]:
    """Find and load Cacao app config from a cacao.yaml file.

    Convenience function that combines find + load + extract.

    Args:
        search_dir: Directory to search for config file. Defaults to cwd.

    Returns:
        Tuple of (app_config_dict, config_file_path).
        If no config file found, returns ({}, None).
    """
    path = find_config_file(search_dir)
    if path is None:
        return {}, None

    data = load_config_file(path)
    app_config = extract_app_config(data)
    return app_config, path
