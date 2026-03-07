"""
JSON Viewer
===========
Demonstrates the JSON tree viewer component for exploring
nested data structures. Includes sample data and the ability
to load custom JSON from a text input.
"""

import json
import cacao as c

c.config(title="JSON Data Explorer", theme="dark")

sample_data = {
    "company": "Acme Corp",
    "founded": 2018,
    "active": True,
    "departments": [
        {
            "name": "Engineering",
            "head": "Alice Chen",
            "team_size": 42,
            "projects": ["Platform", "Mobile App", "API v3"],
        },
        {
            "name": "Marketing",
            "head": "Bob Rivera",
            "team_size": 15,
            "projects": ["Brand Refresh", "Q1 Campaign"],
        },
        {
            "name": "Sales",
            "head": "Carol Yang",
            "team_size": 28,
            "projects": ["Enterprise Push", "Partner Program"],
        },
    ],
    "config": {
        "region": "us-west-2",
        "features": {"dark_mode": True, "beta_access": False},
        "limits": {"api_calls": 10000, "storage_gb": 500},
    },
}

json_input = c.signal(json.dumps(sample_data, indent=2), name="json_input")

c.title("JSON Data Explorer")
c.text("Browse structured data with the collapsible tree viewer.")

with c.tabs(default="viewer"):
    with c.tab("viewer", label="Tree Viewer"):
        c.text("Expand and collapse nodes to explore the data.", size="sm", color="gray")
        c.spacer(size=2)
        c.json(sample_data)

    with c.tab("editor", label="Custom JSON"):
        c.text("Paste your own JSON below and click Parse to view it.", size="sm", color="gray")
        c.textarea(
            label="JSON Input",
            signal="json_input",
            placeholder='{"key": "value"}',
        )
        c.button("Parse JSON", variant="primary", on_click="parse_json")
        c.spacer(size=2)
        c.json(signal="parsed_output")

    with c.tab("samples", label="Sample Datasets"):
        c.text("Quick-load different data structures.", size="sm", color="gray")
        c.spacer(size=1)

        with c.row():
            c.button("Company Data", variant="secondary", on_click="load_company")
            c.button("API Response", variant="secondary", on_click="load_api")
            c.button("Nested Config", variant="secondary", on_click="load_config")

        c.spacer(size=2)
        c.json(signal="sample_output")


@c.on("parse_json")
async def parse_json(session, event):
    try:
        data = json.loads(json_input.value)
        session.set("parsed_output", data)
        c.toast("JSON parsed successfully!", variant="success")
    except json.JSONDecodeError as e:
        c.toast(f"Invalid JSON: {e}", variant="error")


@c.on("load_company")
async def load_company(session, event):
    session.set("sample_output", sample_data)


@c.on("load_api")
async def load_api(session, event):
    session.set("sample_output", {
        "status": 200,
        "data": [
            {"id": 1, "name": "Widget A", "price": 29.99, "in_stock": True},
            {"id": 2, "name": "Widget B", "price": 49.99, "in_stock": False},
        ],
        "pagination": {"page": 1, "total_pages": 5, "per_page": 20},
    })


@c.on("load_config")
async def load_config(session, event):
    session.set("sample_output", {
        "database": {
            "primary": {"host": "db-1.example.com", "port": 5432, "pool_size": 20},
            "replica": {"host": "db-2.example.com", "port": 5432, "read_only": True},
        },
        "cache": {"driver": "redis", "ttl": 3600, "prefix": "app:"},
        "logging": {"level": "INFO", "format": "json", "outputs": ["stdout", "file"]},
    })
