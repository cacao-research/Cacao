"""
Project scaffolding for the Cacao CLI.
Provides interactive project creation with template selection.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional


# Template definitions
TEMPLATES: Dict[str, Dict[str, str]] = {
    "minimal": {
        "name": "Minimal",
        "description": "A bare-bones Cacao app with a simple welcome page",
    },
    "counter": {
        "name": "Counter",
        "description": "Interactive counter app demonstrating state management",
    },
    "dashboard": {
        "name": "Dashboard",
        "description": "Dashboard layout with sidebar navigation and cards",
    },
}


def get_template_path() -> Path:
    """Get the path to the templates directory."""
    return Path(__file__).parent / "templates" / "projects"


def list_templates() -> List[str]:
    """List available project templates."""
    return list(TEMPLATES.keys())


def get_template_info(template_name: str) -> Optional[Dict[str, str]]:
    """Get information about a specific template."""
    return TEMPLATES.get(template_name)


def create_project(
    project_name: str,
    template_name: str,
    output_dir: Optional[Path] = None,
    verbose: bool = False
) -> bool:
    """
    Create a new Cacao project from a template.

    Args:
        project_name: Name of the project to create
        template_name: Name of the template to use
        output_dir: Directory to create the project in (defaults to current directory)
        verbose: Whether to print verbose output

    Returns:
        bool: True if project was created successfully, False otherwise
    """
    if template_name not in TEMPLATES:
        print(f"Error: Unknown template '{template_name}'")
        print(f"Available templates: {', '.join(TEMPLATES.keys())}")
        return False

    # Determine project directory
    if output_dir is None:
        output_dir = Path.cwd()

    project_path = output_dir / project_name

    # Check if directory already exists
    if project_path.exists():
        print(f"Error: Directory '{project_name}' already exists")
        return False

    try:
        # Create project directory structure
        project_path.mkdir(parents=True)
        (project_path / "static" / "css").mkdir(parents=True)

        if verbose:
            print(f"Created directory: {project_path}")

        # Get template content
        template_dir = get_template_path() / template_name

        # Write app.py from template
        app_template = _get_app_template(template_name)
        app_path = project_path / "app.py"
        app_path.write_text(app_template, encoding="utf-8")
        if verbose:
            print(f"Created: {app_path}")

        # Write requirements.txt
        requirements_content = _get_requirements_template()
        requirements_path = project_path / "requirements.txt"
        requirements_path.write_text(requirements_content, encoding="utf-8")
        if verbose:
            print(f"Created: {requirements_path}")

        # Write custom.css
        css_content = _get_css_template()
        css_path = project_path / "static" / "css" / "custom.css"
        css_path.write_text(css_content, encoding="utf-8")
        if verbose:
            print(f"Created: {css_path}")

        return True

    except Exception as e:
        print(f"Error creating project: {e}")
        # Clean up on failure
        if project_path.exists():
            import shutil
            shutil.rmtree(project_path)
        return False


def interactive_create() -> bool:
    """
    Interactive project creation wizard.

    Returns:
        bool: True if project was created successfully, False otherwise
    """
    print("\n  Cacao Project Creator\n")

    # Get project name
    try:
        project_name = input("Project name: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled.")
        return False

    if not project_name:
        print("Error: Project name cannot be empty")
        return False

    # Validate project name
    if not _is_valid_project_name(project_name):
        print("Error: Project name can only contain letters, numbers, hyphens, and underscores")
        return False

    # Display template options
    print("\nAvailable templates:")
    template_list = list(TEMPLATES.items())
    for i, (key, info) in enumerate(template_list, 1):
        print(f"  [{i}] {info['name']}: {info['description']}")

    # Get template selection
    try:
        selection = input(f"\nSelect template [1-{len(template_list)}]: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled.")
        return False

    try:
        selection_idx = int(selection) - 1
        if selection_idx < 0 or selection_idx >= len(template_list):
            raise ValueError()
        template_name = template_list[selection_idx][0]
    except ValueError:
        print(f"Error: Please enter a number between 1 and {len(template_list)}")
        return False

    # Create the project
    print(f"\nCreating project '{project_name}' with '{template_name}' template...")

    if create_project(project_name, template_name, verbose=True):
        print(f"\nProject '{project_name}' created successfully!")
        print("\nNext steps:")
        print(f"  cd {project_name}")
        print("  pip install -r requirements.txt")
        print("  cacao dev app.py")
        return True

    return False


def _is_valid_project_name(name: str) -> bool:
    """Check if project name is valid."""
    import re
    return bool(re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', name))


def _get_app_template(template_name: str) -> str:
    """Get the app.py template content for a given template."""
    templates = {
        "minimal": _MINIMAL_APP_TEMPLATE,
        "counter": _COUNTER_APP_TEMPLATE,
        "dashboard": _DASHBOARD_APP_TEMPLATE,
    }
    return templates.get(template_name, _MINIMAL_APP_TEMPLATE)


def _get_requirements_template() -> str:
    """Get the requirements.txt template content."""
    return "cacao\n"


def _get_css_template() -> str:
    """Get the custom.css template content."""
    return """/* Custom styles for your Cacao app */

/* Add your custom CSS here */
"""


# Template content
_MINIMAL_APP_TEMPLATE = '''"""
Minimal Cacao application.
"""
import cacao

app = cacao.App()


@app.mix("/")
def home():
    """Home page."""
    return {
        "type": "div",
        "props": {
            "style": {
                "minHeight": "100vh",
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "justifyContent": "center",
                "background": "linear-gradient(135deg, #2c1810 0%, #3a1f14 100%)",
                "fontFamily": "'Segoe UI', sans-serif"
            }
        },
        "children": [
            {
                "type": "h1",
                "props": {
                    "content": "Welcome to Cacao",
                    "style": {
                        "fontSize": "48px",
                        "color": "#f0be9b",
                        "marginBottom": "16px"
                    }
                }
            },
            {
                "type": "p",
                "props": {
                    "content": "A deliciously simple web framework for Python",
                    "style": {
                        "fontSize": "18px",
                        "color": "#d6c3b6"
                    }
                }
            }
        ]
    }


if __name__ == "__main__":
    app.brew()
'''

_COUNTER_APP_TEMPLATE = '''"""
Counter application demonstrating Cacao state management.
"""
import cacao
from cacao import State
from typing import Dict, Any, Optional

app = cacao.App()

# Create counter state
counter = State(0)


@counter.subscribe
def on_counter_change(value: int) -> None:
    """Log counter changes."""
    print(f"Counter: {value}")


@app.event("increment")
def handle_increment(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle increment button click."""
    counter.set(counter.value + 1)
    return {"counter": counter.value}


@app.event("decrement")
def handle_decrement(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle decrement button click."""
    counter.set(counter.value - 1)
    return {"counter": counter.value}


@app.mix("/")
def home() -> Dict[str, Any]:
    """Home page with counter."""
    return {
        "type": "div",
        "props": {
            "style": {
                "minHeight": "100vh",
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "justifyContent": "center",
                "background": "linear-gradient(135deg, #2c1810 0%, #3a1f14 100%)",
                "fontFamily": "'Segoe UI', sans-serif"
            }
        },
        "children": [
            {
                "type": "h1",
                "props": {
                    "content": "Cacao Counter",
                    "style": {
                        "fontSize": "36px",
                        "color": "#f0be9b",
                        "marginBottom": "40px"
                    }
                }
            },
            {
                "type": "div",
                "component_type": "counter",
                "props": {
                    "style": {
                        "display": "flex",
                        "alignItems": "center",
                        "gap": "24px",
                        "padding": "32px",
                        "background": "rgba(255, 255, 255, 0.1)",
                        "borderRadius": "16px"
                    },
                    "children": [
                        {
                            "type": "button",
                            "props": {
                                "label": "-",
                                "action": "decrement",
                                "style": {
                                    "fontSize": "24px",
                                    "width": "60px",
                                    "height": "60px",
                                    "borderRadius": "50%",
                                    "border": "2px solid rgba(255,255,255,0.3)",
                                    "background": "rgba(255,255,255,0.1)",
                                    "color": "white",
                                    "cursor": "pointer"
                                }
                            }
                        },
                        {
                            "type": "text",
                            "props": {
                                "content": str(counter.value),
                                "style": {
                                    "fontSize": "64px",
                                    "fontWeight": "bold",
                                    "color": "white",
                                    "minWidth": "120px",
                                    "textAlign": "center"
                                }
                            }
                        },
                        {
                            "type": "button",
                            "props": {
                                "label": "+",
                                "action": "increment",
                                "style": {
                                    "fontSize": "24px",
                                    "width": "60px",
                                    "height": "60px",
                                    "borderRadius": "50%",
                                    "border": "2px solid rgba(255,255,255,0.3)",
                                    "background": "rgba(255,255,255,0.1)",
                                    "color": "white",
                                    "cursor": "pointer"
                                }
                            }
                        }
                    ]
                }
            }
        ]
    }


if __name__ == "__main__":
    app.brew()
'''

_DASHBOARD_APP_TEMPLATE = '''"""
Dashboard application with sidebar navigation.
"""
import cacao
from typing import Dict, Any

app = cacao.App()


def card(title: str, value: str, description: str) -> Dict[str, Any]:
    """Create a dashboard card component."""
    return {
        "type": "div",
        "props": {
            "style": {
                "background": "white",
                "borderRadius": "12px",
                "padding": "24px",
                "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"
            },
            "children": [
                {
                    "type": "text",
                    "props": {
                        "content": title,
                        "style": {
                            "fontSize": "14px",
                            "color": "#666",
                            "marginBottom": "8px"
                        }
                    }
                },
                {
                    "type": "text",
                    "props": {
                        "content": value,
                        "style": {
                            "fontSize": "32px",
                            "fontWeight": "bold",
                            "color": "#2c1810",
                            "marginBottom": "4px"
                        }
                    }
                },
                {
                    "type": "text",
                    "props": {
                        "content": description,
                        "style": {
                            "fontSize": "12px",
                            "color": "#999"
                        }
                    }
                }
            ]
        }
    }


@app.mix("/")
def home() -> Dict[str, Any]:
    """Dashboard home page."""
    return {
        "type": "div",
        "props": {
            "style": {
                "display": "flex",
                "minHeight": "100vh",
                "fontFamily": "'Segoe UI', sans-serif"
            }
        },
        "children": [
            # Sidebar
            {
                "type": "div",
                "props": {
                    "style": {
                        "width": "250px",
                        "background": "#2c1810",
                        "padding": "24px",
                        "color": "white"
                    },
                    "children": [
                        {
                            "type": "h2",
                            "props": {
                                "content": "Dashboard",
                                "style": {
                                    "fontSize": "24px",
                                    "marginBottom": "32px",
                                    "color": "#f0be9b"
                                }
                            }
                        },
                        {
                            "type": "div",
                            "props": {
                                "style": {"display": "flex", "flexDirection": "column", "gap": "8px"},
                                "children": [
                                    {"type": "text", "props": {"content": "Overview", "style": {"padding": "12px", "borderRadius": "8px", "background": "rgba(255,255,255,0.1)"}}},
                                    {"type": "text", "props": {"content": "Analytics", "style": {"padding": "12px", "borderRadius": "8px", "cursor": "pointer"}}},
                                    {"type": "text", "props": {"content": "Reports", "style": {"padding": "12px", "borderRadius": "8px", "cursor": "pointer"}}},
                                    {"type": "text", "props": {"content": "Settings", "style": {"padding": "12px", "borderRadius": "8px", "cursor": "pointer"}}}
                                ]
                            }
                        }
                    ]
                }
            },
            # Main content
            {
                "type": "div",
                "props": {
                    "style": {
                        "flex": "1",
                        "background": "#f5f5f5",
                        "padding": "32px"
                    },
                    "children": [
                        {
                            "type": "h1",
                            "props": {
                                "content": "Overview",
                                "style": {
                                    "fontSize": "28px",
                                    "color": "#2c1810",
                                    "marginBottom": "24px"
                                }
                            }
                        },
                        {
                            "type": "div",
                            "props": {
                                "style": {
                                    "display": "grid",
                                    "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
                                    "gap": "24px"
                                },
                                "children": [
                                    card("Total Users", "1,234", "+12% from last month"),
                                    card("Revenue", "$45,678", "+8% from last month"),
                                    card("Active Sessions", "342", "Currently online"),
                                    card("Conversion Rate", "3.2%", "+0.4% from last week")
                                ]
                            }
                        }
                    ]
                }
            }
        ]
    }


if __name__ == "__main__":
    app.brew()
'''
