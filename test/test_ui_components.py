import pytest
from cacao.ui.components.base import Component
from cacao.ui.components.layout import Grid, Column
from cacao.ui.components.data import (
    Table, Plot, Table, List, Card, Image, Badge, Avatar, Tag, Timeline
)
from cacao.ui.components.inputs import Slider, Input, TextArea, SearchInput, Select, Checkbox, Radio, Switch, DatePicker, TimePicker
from cacao.ui.components.forms import Form, FormItem
from cacao.ui.components.navigation import Menu, Tabs, Dropdown, Pagination, Steps
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

def test_enhanced_table_component():
    columns = [
        {"title": "Name", "dataIndex": "name", "key": "name"},
        {"title": "Age", "dataIndex": "age", "key": "age"},
        {"title": "Address", "dataIndex": "address", "key": "address"}
    ]
    data_source = [
        {"key": "1", "name": "John Brown", "age": 32, "address": "New York No. 1 Lake Park"},
        {"key": "2", "name": "Jim Green", "age": 42, "address": "London No. 1 Lake Park"}
    ]
    pagination = {"page_size": 10, "current": 1}

    table = Table(columns=columns, data_source=data_source, pagination=pagination)
    rendered = table.render()
    
    assert rendered["type"] == "table"
    assert rendered["props"]["columns"] == columns
    assert rendered["props"]["dataSource"] == data_source
    assert rendered["props"]["pagination"] == pagination

def test_list_component():
    items = [
        {"title": "Item 1", "description": "Description 1"},
        {"title": "Item 2", "description": "Description 2"}
    ]
    
    list_component = List(items=items, bordered=True)
    rendered = list_component.render()
    
    assert rendered["type"] == "list"
    assert rendered["props"]["items"] == items
    assert rendered["props"]["bordered"] == True

def test_card_component():
    card = Card(
        children="Card content",
        title="Card Title",
        bordered=True
    )
    rendered = card.render()
    
    assert rendered["type"] == "card"
    assert rendered["props"]["children"] == "Card content"
    assert rendered["props"]["title"] == "Card Title"
    assert rendered["props"]["bordered"] == True

def test_image_component():
    image = Image(
        src="https://example.com/image.jpg",
        alt="Example Image",
        width=200,
        height=150
    )
    rendered = image.render()
    
    assert rendered["type"] == "image"
    assert rendered["props"]["src"] == "https://example.com/image.jpg"
    assert rendered["props"]["alt"] == "Example Image"
    assert rendered["props"]["width"] == 200
    assert rendered["props"]["height"] == 150

def test_badge_component():
    badge = Badge(
        count=5,
        children=TestText("Notifications"),
        dot=False
    )
    rendered = badge.render()
    
    assert rendered["type"] == "badge"
    assert rendered["props"]["count"] == 5
    assert rendered["props"]["children"]["type"] == "text"
    assert rendered["props"]["dot"] == False

def test_avatar_component():
    avatar = Avatar(
        src="https://example.com/avatar.jpg",
        shape="circle",
        size="large"
    )
    rendered = avatar.render()
    
    assert rendered["type"] == "avatar"
    assert rendered["props"]["src"] == "https://example.com/avatar.jpg"
    assert rendered["props"]["shape"] == "circle"
    assert rendered["props"]["size"] == "large"

def test_tag_component():
    tag = Tag(
        content="New",
        color="blue",
        closable=True
    )
    rendered = tag.render()
    
    assert rendered["type"] == "tag"
    assert rendered["props"]["content"] == "New"
    assert rendered["props"]["color"] == "blue"
    assert rendered["props"]["closable"] == True

def test_timeline_component():
    items = [
        {"label": "2015", "content": "Created"},
        {"label": "2020", "content": "Updated"},
        {"label": "2025", "content": "Completed"}
    ]
    
    timeline = Timeline(
        items=items,
        mode="left",
        reverse=False
    )
    rendered = timeline.render()
    
    assert rendered["type"] == "timeline"
    assert rendered["props"]["items"] == items
    assert rendered["props"]["mode"] == "left"
    assert rendered["props"]["reverse"] == False

def test_input_component():
    input_field = Input(
        input_type="text",
        value="test value",
        placeholder="Enter text",
        disabled=False
    )
    rendered = input_field.render()
    assert rendered["type"] == "input"
    assert rendered["props"]["inputType"] == "text"
    assert rendered["props"]["value"] == "test value"
    assert rendered["props"]["placeholder"] == "Enter text"
    assert rendered["props"]["disabled"] == False

def test_textarea_component():
    textarea = TextArea(
        value="sample text",
        placeholder="Enter description",
        rows=5
    )
    rendered = textarea.render()
    assert rendered["type"] == "textarea"
    assert rendered["props"]["value"] == "sample text"
    assert rendered["props"]["placeholder"] == "Enter description"
    assert rendered["props"]["rows"] == 5

def test_search_input_component():
    search = SearchInput(
        value="search term",
        placeholder="Search..."
    )
    rendered = search.render()
    assert rendered["type"] == "search"
    assert rendered["props"]["value"] == "search term"
    assert rendered["props"]["placeholder"] == "Search..."

def test_select_component():
    options = [
        {"label": "Option 1", "value": 1},
        {"label": "Option 2", "value": 2}
    ]
    select = Select(
        options=options,
        value=1,
        placeholder="Select an option"
    )
    rendered = select.render()
    assert rendered["type"] == "select"
    assert rendered["props"]["options"] == options
    assert rendered["props"]["value"] == 1
    assert rendered["props"]["placeholder"] == "Select an option"

def test_checkbox_component():
    checkbox = Checkbox(
        label="Accept terms",
        checked=True
    )
    rendered = checkbox.render()
    assert rendered["type"] == "checkbox"
    assert rendered["props"]["label"] == "Accept terms"
    assert rendered["props"]["checked"] == True

def test_radio_component():
    options = [
        {"label": "Option A", "value": "a"},
        {"label": "Option B", "value": "b"}
    ]
    radio = Radio(
        options=options,
        value="a"
    )
    rendered = radio.render()
    assert rendered["type"] == "radio"
    assert rendered["props"]["options"] == options
    assert rendered["props"]["value"] == "a"

def test_switch_component():
    switch = Switch(checked=True)
    rendered = switch.render()
    assert rendered["type"] == "switch"
    assert rendered["props"]["checked"] == True

def test_datepicker_component():
    datepicker = DatePicker(
        value="2025-04-13",
        range=False
    )
    rendered = datepicker.render()
    assert rendered["type"] == "datepicker"
    assert rendered["props"]["value"] == "2025-04-13"
    assert rendered["props"]["range"] == False

def test_timepicker_component():
    timepicker = TimePicker(value="14:30")
    rendered = timepicker.render()
    assert rendered["type"] == "timepicker"
    assert rendered["props"]["value"] == "14:30"

def test_enhanced_form_component():
    fields = [
        {"name": "username", "label": "Username", "type": "text"},
        {"name": "password", "label": "Password", "type": "password"}
    ]
    validation_rules = {
        "username": [{"required": True, "message": "Username is required"}]
    }
    form = Form(
        fields=fields,
        layout="vertical",
        validation_rules=validation_rules
    )
    rendered = form.render()
    assert rendered["type"] == "form"
    assert rendered["props"]["fields"] == fields
    assert rendered["props"]["layout"] == "vertical"
    assert rendered["props"]["validationRules"] == validation_rules

def test_menu_component():
    items = [
        {"key": "home", "label": "Home"},
        {"key": "about", "label": "About"}
    ]
    menu = Menu(
        items=items,
        mode="horizontal",
        selected_keys=["home"]
    )
    rendered = menu.render()
    assert rendered["type"] == "menu"
    assert rendered["props"]["items"] == items
    assert rendered["props"]["mode"] == "horizontal"
    assert rendered["props"]["selectedKeys"] == ["home"]

def test_tabs_component():
    items = [
        {"key": "tab1", "label": "Tab 1", "content": "Content 1"},
        {"key": "tab2", "label": "Tab 2", "content": "Content 2"}
    ]
    tabs = Tabs(
        items=items,
        active_key="tab1"
    )
    rendered = tabs.render()
    assert rendered["type"] == "tabs"
    assert rendered["props"]["items"] == items
    assert rendered["props"]["activeKey"] == "tab1"

def test_dropdown_component():
    items = [
        {"key": "item1", "label": "Item 1"},
        {"key": "item2", "label": "Item 2"}
    ]
    dropdown = Dropdown(
        items=items,
        trigger="click",
        placement="bottomLeft"
    )
    rendered = dropdown.render()
    assert rendered["type"] == "dropdown"
    assert rendered["props"]["items"] == items
    assert rendered["props"]["trigger"] == "click"
    assert rendered["props"]["placement"] == "bottomLeft"

def test_pagination_component():
    pagination = Pagination(
        total=100,
        current=1,
        page_size=10
    )
    rendered = pagination.render()
    assert rendered["type"] == "pagination"
    assert rendered["props"]["total"] == 100
    assert rendered["props"]["current"] == 1
    assert rendered["props"]["pageSize"] == 10