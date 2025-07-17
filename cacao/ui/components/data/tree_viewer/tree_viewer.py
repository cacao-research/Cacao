from typing import Any, Dict, Optional
from ...base import Component

class TreeViewer(Component):
    """
    A component to render collapsible tree structures.

    Props:
      - id: unique component ID
      - data: the object to display as a tree
      - expand_all: whether to start fully expanded
      - theme: "light" or "dark"
      - on_node_click: optional event name to fire when a key is clicked
    """
    def __init__(
        self,
        id: str,
        data: Dict[str, Any],
        expand_all: bool = False,
        theme: str = "light",
        on_node_click: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.id = id
        self.data = data
        self.expand_all = expand_all
        self.theme = theme
        self.on_node_click = on_node_click

    def validate(self) -> bool:
        return isinstance(self.data, (dict, list))

    def to_dict(self) -> Dict[str, Any]:
        props = {
            "id": self.id,
            "data": self.data,
            "expand_all": self.expand_all,
            "theme": self.theme,
        }
        if self.on_node_click:
            props["on_node_click"] = self.on_node_click

        return {
            "type": "tree_viewer",
            "props": props,
            **self.get_base_props()
        }
