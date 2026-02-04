"""
Desktop app with pandas DataFrame table integration using Cacao
Combines the desktop app functionality with pandas table demo
"""

import pandas as pd
import cacao
from cacao.ui.components.data.table.table import Table

# Create the Cacao app
app = cacao.App()

# Create sample pandas DataFrame
sample_data = pd.DataFrame({
    'id': range(1, 101),
    'name': [f'User {i}' for i in range(1, 101)],
    'age': [20 + (i % 50) for i in range(1, 101)],
    'city': ['New York', 'London', 'Paris', 'Tokyo', 'Berlin'] * 20,
    'salary': [40000 + (i * 1000) for i in range(1, 101)],
    'department': ['Engineering', 'Marketing', 'Sales', 'HR', 'Finance'] * 20
})

@app.mix("/")
def home():
    return {
        "type": "div",
        "props": {
            "style": {
                "padding": "20px",
                "fontFamily": "Arial, sans-serif",
                "backgroundColor": "#f8f9fa"
            }
        },
        "children": [
            {
                "type": "h1",
                "props": {
                    "children": "Pandas DataFrame Table - Desktop App",
                    "style": {
                        "color": "#f0be9b",
                        "marginBottom": "20px",
                        "textAlign": "center"
                    }
                }
            },
            {
                "type": "p",
                "props": {
                    "children": "This desktop app demonstrates automatic pandas DataFrame integration with server-side processing.",
                    "style": {
                        "color": "#495057",
                        "marginBottom": "30px",
                        "textAlign": "center",
                        "fontSize": "16px"
                    }
                }
            },
            
            # Basic pandas table section
            {
                "type": "div",
                "props": {
                    "style": {
                        "marginBottom": "40px",
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"
                    }
                },
                "children": [
                    {
                        "type": "h2",
                        "props": {
                            "children": "Auto-Generated Table",
                            "style": {
                                "color": "#D4A76A",
                                "marginBottom": "15px"
                            }
                        }
                    },
                    Table(
                        dataSource=sample_data,
                        show_length_menu=True
                    ).render()
                ]
            },
            
            # Custom column configuration section
            {
                "type": "div",
                "props": {
                    "style": {
                        "marginBottom": "40px",
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"
                    }
                },
                "children": [
                    {
                        "type": "h2",
                        "props": {
                            "children": "Custom Column Configuration",
                            "style": {
                                "color": "#D4A76A",
                                "marginBottom": "15px"
                            }
                        }
                    },
                    Table(
                        dataSource=sample_data,
                        columns=[
                            {"title": "ID", "dataIndex": "id", "width": "60px"},
                            {"title": "Full Name", "dataIndex": "name"},
                            {"title": "Age", "dataIndex": "age", "width": "80px"},
                            {"title": "Location", "dataIndex": "city"},
                            {"title": "Department", "dataIndex": "department"},
                            {"title": "Annual Salary", "dataIndex": "salary", "width": "120px"}
                        ],
                        show_length_menu=True,
                        page_length=25,
                        length_menu=[10, 25, 50, 100],
                        buttons=["copy", "csv", "excel"]
                    ).render()
                ]
            },
            
            # Features list
            {
                "type": "div",
                "props": {
                    "style": {
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"
                    }
                },
                "children": [
                    {
                        "type": "h2",
                        "props": {
                            "children": "Features Demonstrated",
                            "style": {
                                "color": "#D4A76A",
                                "marginBottom": "15px"
                            }
                        }
                    },
                    {
                        "type": "ul",
                        "props": {
                            "style": {
                                "color": "#495057",
                                "lineHeight": "1.8"
                            },
                            "children": [
                                {"type": "li", "props": {"children": "✅ Automatic pandas DataFrame detection"}},
                                {"type": "li", "props": {"children": "🔄 Server-side processing (pagination, search, sort)"}},
                                {"type": "li", "props": {"children": "📊 Auto-generated column definitions"}},
                                {"type": "li", "props": {"children": "🔒 Thread-safe data operations"}},
                                {"type": "li", "props": {"children": "🎛️ DataTables integration"}},
                                {"type": "li", "props": {"children": "📤 Export functionality"}},
                                {"type": "li", "props": {"children": "📱 Responsive design"}},
                                {"type": "li", "props": {"children": "🖥️ Desktop application support"}}
                            ]
                        }
                    }
                ]
            }
        ]
    }

if __name__ == "__main__":
    # Launch as desktop application
    app.brew(
        type="web",
        title="Pandas Table Desktop Demo",
        width=1200,
        height=800,
        resizable=True,
        fullscreen=False,
        icon="cacao/core/static/icons/icon-512.png"
    )