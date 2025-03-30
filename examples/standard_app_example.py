from cacao import mix, run_desktop, State, Component
from typing import Dict, Any, Optional, List
from datetime import datetime
import random

# Create reactive states
tasks_state = State([
    {"id": 1, "title": "Learn Cacao", "completed": False},
    {"id": 2, "title": "Build an app", "completed": False},
    {"id": 3, "title": "Share with friends", "completed": False}
])
new_task_title = State("")

class TaskList(Component):
    def __init__(self) -> None:
        """Initialize task list component."""
        super().__init__()
        
    def render(self, ui_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Render the task list component.
        
        Args:
            ui_state: Optional state from the UI definition
            
        Returns:
            JSON UI definition for the task list
        """
        tasks = tasks_state.value
        
        task_items = []
        for task in tasks:
            task_items.append({
                "type": "task-item",
                "props": {
                    "id": task["id"],
                    "title": task["title"],
                    "completed": task["completed"],
                    "onToggle": {"action": "toggle_task", "params": {"id": task["id"]}}
                }
            })
        
        return {
            "type": "card",
            "props": {
                "title": "My Tasks",
                "children": [
                    {
                        "type": "list",
                        "props": {
                            "children": task_items if task_items else [
                                {
                                    "type": "text",
                                    "props": {
                                        "content": "No tasks yet! Add one below."
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }

class TaskForm(Component):
    def __init__(self) -> None:
        """Initialize task form component."""
        super().__init__()
    
    def render(self, ui_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Render the task form component.
        
        Args:
            ui_state: Optional state from the UI definition
            
        Returns:
            JSON UI definition for the task form
        """
        return {
            "type": "form",
            "props": {
                "children": [
                    {
                        "type": "input",
                        "props": {
                            "placeholder": "Enter a new task...",
                            "value": new_task_title.value,
                            "onChange": "update_new_task_title"
                        }
                    },
                    {
                        "type": "button",
                        "props": {
                            "label": "Add Task",
                            "action": "add_task",
                            "disabled": len(new_task_title.value.strip()) == 0
                        }
                    }
                ]
            }
        }

# Event handlers
@mix.event("update_new_task_title")
async def handle_update_title(event: Dict[str, Any]) -> None:
    """
    Handle task title input changes.
    
    Args:
        event: Event data containing the new title
    """
    new_task_title.update(event.get("value", ""))

@mix.event("add_task")
async def handle_add_task(event: Dict[str, Any]) -> None:
    """
    Handle adding a new task.
    
    Args:
        event: Event data
    """
    if len(new_task_title.value.strip()) == 0:
        return
        
    new_id = max([task["id"] for task in tasks_state.value]) + 1 if tasks_state.value else 1
    new_task = {
        "id": new_id,
        "title": new_task_title.value,
        "completed": False
    }
    
    tasks_state.update(tasks_state.value + [new_task])
    new_task_title.update("")

@mix.event("toggle_task")
async def handle_toggle_task(event: Dict[str, Any]) -> None:
    """
    Handle toggling a task's completed status.
    
    Args:
        event: Event data containing task ID
    """
    task_id = event.get("params", {}).get("id")
    if task_id:
        updated_tasks = []
        for task in tasks_state.value:
            if task["id"] == task_id:
                updated_tasks.append({**task, "completed": not task["completed"]})
            else:
                updated_tasks.append(task)
        
        tasks_state.update(updated_tasks)

@mix("/")
def home() -> Dict[str, Any]:
    """
    Main page handler for the task app.
    
    Returns:
        JSON UI definition for the home page
    """
    task_list = TaskList()
    task_form = TaskForm()
    
    return {
        "layout": "column",
        "children": [
            {
                "type": "header",
                "props": {
                    "title": "Cacao Task Manager",
                    "subtitle": f"Today is {datetime.now().strftime('%A, %B %d')}"
                }
            },
            {
                "type": "container",
                "props": {
                    "maxWidth": "800px",
                    "padding": "16px",
                    "children": [
                        task_list.render(),
                        task_form.render()
                    ]
                }
            },
            {
                "type": "footer",
                "props": {
                    "text": "© 2025 Cacao Framework - Standard Desktop App"
                }
            }
        ]
    }

if __name__ == "__main__":
    # Run as a desktop application
    run_desktop(
        title="Cacao Task Manager",
        width=800,
        height=600,
        resizable=True,
        fullscreen=False
    )