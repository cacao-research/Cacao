"""
Generate API reference documentation pages from docstrings.

This script is used by MkDocs to auto-generate API documentation
from the Cacao source code.

Usage:
    python scripts/gen_ref_pages.py

Or configure in mkdocs.yml with mkdocs-gen-files plugin.
"""

from pathlib import Path
import os


def generate_api_docs(
    src_dir: str = "cacao",
    output_dir: str = "docs/api",
    exclude_patterns: list = None
) -> None:
    """
    Generate API reference markdown files from Python source files.

    Args:
        src_dir: Source directory containing Python modules
        output_dir: Output directory for generated markdown
        exclude_patterns: List of patterns to exclude (e.g., ["__pycache__", "test_"])
    """
    if exclude_patterns is None:
        exclude_patterns = ["__pycache__", "test_", ".pyc"]

    src_path = Path(src_dir)
    output_path = Path(output_dir)

    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)

    # Track generated modules for nav
    modules = []

    for py_file in src_path.rglob("*.py"):
        # Skip excluded patterns
        if any(pattern in str(py_file) for pattern in exclude_patterns):
            continue

        # Skip private modules (except __init__)
        if py_file.name.startswith("_") and py_file.name != "__init__.py":
            continue

        # Calculate module path
        rel_path = py_file.relative_to(src_path)
        module_parts = list(rel_path.with_suffix("").parts)

        # Handle __init__.py
        if module_parts[-1] == "__init__":
            module_parts = module_parts[:-1]
            if not module_parts:
                module_parts = [src_dir]

        module_name = ".".join([src_dir] + module_parts)

        # Generate output path
        if len(module_parts) == 0:
            out_file = output_path / f"{src_dir}.md"
        else:
            out_file = output_path / f"{'.'.join(module_parts)}.md"

        # Generate markdown content
        content = generate_module_doc(module_name, py_file)

        if content:
            out_file.write_text(content, encoding="utf-8")
            modules.append((module_name, out_file.name))
            print(f"Generated: {out_file}")

    # Generate index if modules were created
    if modules:
        generate_index(output_path, modules)


def generate_module_doc(module_name: str, source_file: Path) -> str:
    """
    Generate markdown documentation for a single module.

    Args:
        module_name: Full module name (e.g., "cacao.core.state")
        source_file: Path to the source file

    Returns:
        Markdown content string
    """
    # Read source file to check if it has content
    try:
        content = source_file.read_text(encoding="utf-8")
    except Exception:
        return ""

    # Skip empty or minimal files
    lines = [l for l in content.split("\n") if l.strip() and not l.strip().startswith("#")]
    if len(lines) < 3:
        return ""

    # Generate mkdocstrings reference
    doc = f"""# {module_name}

::: {module_name}
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2
      members_order: source
"""
    return doc


def generate_index(output_path: Path, modules: list) -> None:
    """
    Generate an index page listing all API modules.

    Args:
        output_path: Output directory path
        modules: List of (module_name, filename) tuples
    """
    content = """# API Reference

Auto-generated API documentation for Cacao.

## Modules

"""
    # Group by top-level module
    groups = {}
    for module_name, filename in sorted(modules):
        parts = module_name.split(".")
        if len(parts) > 1:
            group = parts[1]  # e.g., "core", "ui", "cli"
        else:
            group = "main"

        if group not in groups:
            groups[group] = []
        groups[group].append((module_name, filename))

    # Generate grouped listing
    for group, group_modules in sorted(groups.items()):
        content += f"### {group.title()}\n\n"
        for module_name, filename in group_modules:
            content += f"- [{module_name}]({filename})\n"
        content += "\n"

    # Write index
    index_path = output_path / "modules.md"
    index_path.write_text(content, encoding="utf-8")
    print(f"Generated index: {index_path}")


def main():
    """Main entry point."""
    # Get project root (parent of scripts directory)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    os.chdir(project_root)

    print("Generating API documentation...")
    generate_api_docs(
        src_dir="cacao",
        output_dir="docs/api/reference",
        exclude_patterns=["__pycache__", "test_", ".pyc", "templates"]
    )
    print("Done!")


if __name__ == "__main__":
    main()
