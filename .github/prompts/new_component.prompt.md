# Cacao UI Component Generator

**Goal:** Create a new UI component following framework conventions

1. Inherit from `ui.components.base.Component`
2. Implement required methods:
```python
def render(self) -> str:
    # Return HTML template

def update(self, state: State):
    # Handle state changes
```
3. Add TypeScript type definitions in `static/js/types.d.ts`
4. Register component in `ui/component_manager.py`

Example reference: [ui/components/table.py](../cacao/ui/components/table.py)