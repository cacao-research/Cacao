import pytest
from cacao.ui.components.base import Component
from cacao.ui.components.layout import Grid, Column
from cacao.ui.components.data import Table, Plot
from cacao.ui.components.inputs import Slider, Form
from typing import Dict, Any

class TestButton(Component):
    __test__ = False  # Prevent pytest from collecting this class
    def __init__(self, label="Test Button"):
        super().__init__()
        self.label = label
    
    def render(self) -> Dict[str, Any]:
        return {"type": "button", "props": {"label": self.label}}

class TestText(Component):
    __test__ = False  # Prevent pytest from collecting this class
    def __init__(self, content="Test Content"):
        super().__init__()
        self.content = content
    
    def render(self) -> Dict[str, Any]:
        return {"type": "text", "props": {"content": self.content}}

def test_grid_component():
    button = TestButton("Click me")
    
    grid = Grid(children=[button], columns=2)
    rendered = grid.render()
    
    assert rendered["type"] == "grid"
    assert rendered["props"]["columns"] == 2
    assert len(rendered["props"]["children"]) == 1
    assert rendered["props"]["children"][0]["type"] == "button"

def test_column_component():
    text1 = TestText("First item")
    text2 = TestText("Second item")
    
    column = Column(children=[text1, text2])
    rendered = column.render()
    
    assert rendered["type"] == "column"
    assert len(rendered["props"]["children"]) == 2
    assert rendered["props"]["children"][0]["props"]["content"] == "First item"
    assert rendered["props"]["children"][1]["props"]["content"] == "Second item"

def test_table_component():
    table = Table(
        headers=["Name", "Age", "Location"],
        rows=[
            ["Alice", "30", "New York"],
            ["Bob", "25", "San Francisco"]
        ]
    )
    
    rendered = table.render()
    assert rendered["type"] == "table"
    assert "headers" in rendered["props"]
    assert "rows" in rendered["props"]
    assert len(rendered["props"]["headers"]) == 3
    assert len(rendered["props"]["rows"]) == 2

def test_plot_component():
    plot_data = {
        "x": [1, 2, 3, 4, 5],
        "y": [10, 15, 13, 17, 20]
    }
    
    plot = Plot(data=plot_data, title="Sample Plot")
    
    rendered = plot.render()
    assert rendered["type"] == "plot"
    assert rendered["props"]["title"] == "Sample Plot"
    assert "data" in rendered["props"]
    assert "x" in rendered["props"]["data"]
    assert "y" in rendered["props"]["data"]

def test_slider_component():
    slider = Slider(min_value=0, max_value=100, step=1, value=50)
    rendered = slider.render()
    assert rendered["type"] == "slider"
    assert rendered["props"]["min"] == 0
    assert rendered["props"]["max"] == 100
    assert rendered["props"]["step"] == 1
    assert rendered["props"]["value"] == 50

def test_form_component():
    form = Form(fields={"username": {"type": "text", "placeholder": "Enter your name"}})
    rendered = form.render()
    assert rendered["type"] == "form"
    assert "fields" in rendered["props"]
    assert "username" in rendered["props"]["fields"]
    assert rendered["props"]["fields"]["username"]["type"] == "text"