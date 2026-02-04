"""
Advanced Desktop app with pandas DataFrame table and filter panel
Combines the desktop app functionality with advanced pandas table filtering
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import cacao
from cacao.ui.components.data.table.table import Table

# Create the Cacao app
app = cacao.App()

def create_sample_data():
    """Create a comprehensive sample dataset for demonstration."""
    np.random.seed(42)
    
    # Generate sample data with various data types
    n_records = 200
    
    data = {
        'employee_id': range(1, n_records + 1),
        'name': [f"Employee {i}" for i in range(1, n_records + 1)],
        'department': np.random.choice(['Engineering', 'Sales', 'Marketing', 'HR', 'Finance'], n_records),
        'position': np.random.choice(['Manager', 'Senior', 'Junior', 'Lead', 'Intern'], n_records),
        'salary': np.random.randint(30000, 150000, n_records),
        'age': np.random.randint(22, 65, n_records),
        'experience_years': np.random.randint(0, 40, n_records),
        'performance_score': np.round(np.random.uniform(1.0, 5.0, n_records), 1),
        'city': np.random.choice(['New York', 'San Francisco', 'Chicago', 'Austin', 'Seattle'], n_records),
        'hire_date': [
            (datetime.now() - timedelta(days=np.random.randint(30, 3650))).strftime('%Y-%m-%d')
            for _ in range(n_records)
        ],
        'active': np.random.choice([True, False], n_records, p=[0.85, 0.15]),
        'bonus_eligible': np.random.choice(['Yes', 'No'], n_records, p=[0.7, 0.3])
    }
    
    return pd.DataFrame(data)

# Create sample DataFrame
sample_data = create_sample_data()

@app.mix("/")
def home():
    # Define custom columns with enhanced metadata for filtering
    columns = [
        {
            "title": "ID",
            "dataIndex": "employee_id",
            "key": "employee_id",
            "width": "80px",
            "type": "number",
            "sortable": True,
            "searchable": True
        },
        {
            "title": "Employee Name",
            "dataIndex": "name", 
            "key": "name",
            "width": "150px",
            "sortable": True,
            "searchable": True
        },
        {
            "title": "Department",
            "dataIndex": "department",
            "key": "department",
            "width": "120px",
            "sortable": True,
            "searchable": True
        },
        {
            "title": "Position",
            "dataIndex": "position",
            "key": "position", 
            "width": "100px",
            "sortable": True,
            "searchable": True
        },
        {
            "title": "Salary ($)",
            "dataIndex": "salary",
            "key": "salary",
            "width": "100px",
            "type": "number",
            "sortable": True,
            "searchable": True
        },
        {
            "title": "Age",
            "dataIndex": "age",
            "key": "age",
            "width": "80px", 
            "type": "number",
            "sortable": True,
            "searchable": True
        },
        {
            "title": "Experience",
            "dataIndex": "experience_years",
            "key": "experience_years",
            "width": "100px",
            "type": "number",
            "sortable": True,
            "searchable": True
        },
        {
            "title": "Performance",
            "dataIndex": "performance_score",
            "key": "performance_score",
            "width": "100px",
            "type": "number",
            "sortable": True,
            "searchable": True
        },
        {
            "title": "City",
            "dataIndex": "city",
            "key": "city",
            "width": "120px",
            "sortable": True,
            "searchable": True
        },
        {
            "title": "Hire Date",
            "dataIndex": "hire_date",
            "key": "hire_date",
            "width": "120px",
            "type": "date",
            "sortable": True,
            "searchable": True
        },
        {
            "title": "Active",
            "dataIndex": "active",
            "key": "active",
            "width": "80px",
            "sortable": True,
            "searchable": True
        },
        {
            "title": "Bonus Eligible",
            "dataIndex": "bonus_eligible",
            "key": "bonus_eligible",
            "width": "120px",
            "sortable": True,
            "searchable": True
        }
    ]

    return {
        "type": "div",
        "props": {
            "style": {
                "padding": "20px",
                "fontFamily": "Arial, sans-serif",
                "backgroundColor": "#f8f9fa",
                "minHeight": "100vh"
            }
        },
        "children": [
            {
                "type": "h1",
                "props": {
                    "content": "Advanced Pandas Table with Filter Panel - Desktop App",
                    "style": {
                        "color": "#f0be9b",
                        "marginBottom": "20px",
                        "textAlign": "center",
                        "fontSize": "28px"
                    }
                }
            },
            {
                "type": "p",
                "props": {
                    "content": "This desktop app showcases the advanced filter panel that slides in from the right. Click the 'Advanced Filters' button to open the filter panel.",
                    "style": {
                        "color": "#495057",
                        "marginBottom": "20px",
                        "textAlign": "center",
                        "fontSize": "16px",
                        "maxWidth": "800px",
                        "margin": "0 auto 20px auto"
                    }
                }
            },
            
            # Features section
            {
                "type": "div",
                "props": {
                    "style": {
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                        "marginBottom": "30px"
                    }
                },
                "children": [
                    {
                        "type": "h3",
                        "props": {
                            "content": "🔍 Features:",
                            "style": {
                                "color": "#D4A76A",
                                "marginBottom": "15px",
                                "fontWeight": "600"
                            }
                        }
                    },
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "display": "grid",
                                "gridTemplateColumns": "repeat(auto-fit, minmax(300px, 1fr))",
                                "gap": "10px",
                                "color": "#495057"
                            }
                        },
                        "children": [
                            {"type": "div", "props": {"content": "• Right-side sliding filter panel"}},
                            {"type": "div", "props": {"content": "• Column-specific filtering with multiple filter types"}},
                            {"type": "div", "props": {"content": "• Numeric range filtering"}},
                            {"type": "div", "props": {"content": "• Text filtering (contains, equals, starts with, ends with)"}},
                            {"type": "div", "props": {"content": "• Real-time server-side filtering with pandas DataFrames"}},
                            {"type": "div", "props": {"content": "• Visual indicator when filters are active"}},
                            {"type": "div", "props": {"content": "• Responsive design for desktop applications"}},
                            {"type": "div", "props": {"content": "• Export functionality (CSV, Excel, PDF)"}}
                        ]
                    }
                ]
            },
            
            # Advanced table section
            {
                "type": "div",
                "props": {
                    "style": {
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                        "marginBottom": "20px"
                    }
                },
                "children": [
                    {
                        "type": "h2",
                        "props": {
                            "content": "Employee Data Table",
                            "style": {
                                "color": "#D4A76A",
                                "marginBottom": "20px"
                            }
                        }
                    },
                    Table(
                        columns=columns,
                        dataSource=sample_data,
                        advanced=True,
                        show_length_menu=True,
                        page_length=25,
                        length_menu=[10, 25, 50, 100],
                        searching=True,
                        ordering=True,
                        info=True,
                        responsive=True,
                        buttons=["copy", "csv", "excel", "pdf"],
                        theme="default"
                    ).render()
                ]
            }
        ]
    }

if __name__ == "__main__":
    # Launch as desktop application with larger window for better table viewing
    app.brew(
        type="web",
        title="Advanced Filter Panel Desktop Demo",
        width=1400,
        height=900,
        resizable=True,
        fullscreen=False,
        icon="cacao/core/static/icons/icon-512.png"
    )