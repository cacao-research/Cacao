"""
Code generation tool for Cacao.
Generates boilerplate files based on predefined templates.
"""

import os
import shutil
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / "templates"
OUTPUT_DIR = Path.cwd() / "generated_app"

def copy_template(template_path: Path, target_path: Path) -> None:
    """
    Copies a template file or directory to the target path.
    """
    if template_path.is_dir():
        shutil.copytree(template_path, target_path, dirs_exist_ok=True)
    else:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(template_path, target_path)
    print(f"Generated: {target_path}")

def generate_project() -> None:
    """
    Generates a new project structure based on Cacao templates.
    """
    if OUTPUT_DIR.exists():
        print(f"Output directory '{OUTPUT_DIR}' already exists. Aborting generation.")
        return

    # Create base output directory
    OUTPUT_DIR.mkdir(parents=True)
    
    # Copy the cacao.json config template
    config_template = TEMPLATES_DIR / "cacao.json"
    copy_template(config_template, OUTPUT_DIR / "cacao.json")
    
    # Copy docs blueprint
    docs_template = TEMPLATES_DIR / "docs"
    copy_template(docs_template, OUTPUT_DIR / "docs")
    
    print("Project generation complete.")

if __name__ == "__main__":
    generate_project()
