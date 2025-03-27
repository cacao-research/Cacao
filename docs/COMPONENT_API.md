# Cacao Component API

This document provides an overview of the UI components available in Cacao. The components are designed to facilitate rapid development of interactive dashboards and data apps.

## Components Overview

### Base Component
- **Description:** Abstract base class for all UI components.
- **Key Method:** `render()` - returns a JSON representation of the component.

### Input Components
- **Slider:** For numeric input.
- **Form:** For collecting multiple inputs.

### Data Components
- **Table:** For displaying tabular data.
- **Plot:** For rendering charts and graphs.

### Layout Components
- **Grid:** Arranges components in a grid layout.
- **Column:** Arranges components vertically.

## Usage Example

```python
from cacao.ui import Slider, Table, Grid

slider = Slider(min_value=0, max_value=100, step=1)
table = Table(headers=["Name", "Value"], rows=[["Item 1", 10], ["Item 2", 20]])
layout = Grid(children=[slider, table], columns=2)

