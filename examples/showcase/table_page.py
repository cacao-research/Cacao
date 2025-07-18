"""
Table Page for the components showcase.
Demonstrates the unified table component with both simple and advanced functionality.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from cacao.ui.components.data import Table, create_simple_table, create_advanced_table
from cacao.extensions.plugins.pandas_table import PandasTablePlugin

class TablePage:
    def render(self):
        return {
            "type": "div",
            "props": {
                "style": {
                    "padding": "20px",
                    "backgroundColor": "#FAFAFA"
                },
                "children": [
                    {
                        "type": "h1",
                        "props": {
                            "content": "Unified Table Component Showcase",
                            "style": {
                                "color": "#6B4226",
                                "marginBottom": "30px",
                                "textAlign": "center"
                            }
                        }
                    },
                    
                    # 1. Basic Table - Legacy API (headers/rows) - Simple Mode
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#FFFFFF",
                                "borderRadius": "8px",
                                "padding": "20px",
                                "marginBottom": "30px",
                                "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"
                            },
                            "children": [
                                {
                                    "type": "h3",
                                    "props": {
                                        "content": "1. Basic Table (Legacy API - Simple Mode)",
                                        "style": {
                                            "color": "#8B4513",
                                            "marginBottom": "10px"
                                        }
                                    }
                                },
                                {
                                    "type": "p",
                                    "props": {
                                        "content": "Simple table using legacy API with headers and rows (advanced=False)",
                                        "style": {
                                            "color": "#666",
                                            "marginBottom": "15px"
                                        }
                                    }
                                },
                                Table(
                                    headers=["Employee", "Department", "Role"],
                                    rows=[
                                        ["Sarah Johnson", "Engineering", "Frontend Developer"],
                                        ["Mike Chen", "Engineering", "Backend Developer"],
                                        ["Lisa Rodriguez", "Design", "UI/UX Designer"],
                                        ["David Kim", "Marketing", "Content Manager"]
                                    ],
                                    advanced=False
                                ).render()
                            ]
                        }
                    },
                    
                    # 2. Enhanced DataFrame Conversion - Small Dataset
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#FFFFFF",
                                "borderRadius": "8px",
                                "padding": "20px",
                                "marginBottom": "30px",
                                "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"
                            },
                            "children": [
                                {
                                    "type": "h3",
                                    "props": {
                                        "content": "2. Enhanced DataFrame Conversion - Small Dataset",
                                        "style": {
                                            "color": "#8B4513",
                                            "marginBottom": "10px"
                                        }
                                    }
                                },
                                {
                                    "type": "p",
                                    "props": {
                                        "content": "Pandas DataFrame with enhanced conversion (in-memory processing)",
                                        "style": {
                                            "color": "#666",
                                            "marginBottom": "15px"
                                        }
                                    }
                                },
                                self._create_enhanced_dataframe_demo(small=True)
                            ]
                        }
                    },
                    
                    # 3. Enhanced DataFrame Conversion - Large Dataset
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#FFFFFF",
                                "borderRadius": "8px",
                                "padding": "20px",
                                "marginBottom": "30px",
                                "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"
                            },
                            "children": [
                                {
                                    "type": "h3",
                                    "props": {
                                        "content": "3. Enhanced DataFrame Conversion - Large Dataset",
                                        "style": {
                                            "color": "#8B4513",
                                            "marginBottom": "10px"
                                        }
                                    }
                                },
                                {
                                    "type": "p",
                                    "props": {
                                        "content": "Pandas DataFrame with enhanced conversion (server-side processing)",
                                        "style": {
                                            "color": "#666",
                                            "marginBottom": "15px"
                                        }
                                    }
                                },
                                self._create_enhanced_dataframe_demo(small=False)
                            ]
                        }
                    },
                    
                    # 4. DataFrame Type Preservation Demo
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#FFFFFF",
                                "borderRadius": "8px",
                                "padding": "20px",
                                "marginBottom": "30px",
                                "boxShadow": "0 2px 8px rgba(0,0,0,0.1)"
                            },
                            "children": [
                                {
                                    "type": "h3",
                                    "props": {
                                        "content": "4. DataFrame Type Preservation Demo",
                                        "style": {
                                            "color": "#8B4513",
                                            "marginBottom": "10px"
                                        }
                                    }
                                },
                                {
                                    "type": "p",
                                    "props": {
                                        "content": "Demonstrates preservation of pandas dtypes and handling of missing values",
                                        "style": {
                                            "color": "#666",
                                            "marginBottom": "15px"
                                        }
                                    }
                                },
                                self._create_dtype_preservation_demo()
                            ]
                        }
                    }
                ]
            }
        }
    
    def _create_enhanced_dataframe_demo(self, small=True):
        """Create a demo DataFrame with enhanced conversion."""
        if small:
            # Small dataset (in-memory processing)
            df = pd.DataFrame({
                'employee_id': range(1, 6),
                'name': ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 'Eve Brown'],
                'department': pd.Categorical(['Engineering', 'Marketing', 'Sales', 'Engineering', 'HR']),
                'salary': [85000.0, 65000.0, 55000.0, 92000.0, 48000.0],
                'start_date': pd.date_range('2020-01-01', periods=5, freq='3M'),
                'is_active': [True, True, False, True, True],
                'bonus': [5000.0, np.nan, 2000.0, 7500.0, np.nan]
            })
            plugin = PandasTablePlugin(enhanced_mode=True, row_threshold=100, memory_threshold_mb=1)
        else:
            # Large dataset (server-side processing)
            np.random.seed(42)
            n_rows = 15000  # Exceeds threshold
            df = pd.DataFrame({
                'id': range(1, n_rows + 1),
                'name': [f'Employee_{i}' for i in range(1, n_rows + 1)],
                'department': pd.Categorical(np.random.choice(['Engineering', 'Marketing', 'Sales', 'HR'], n_rows)),
                'salary': np.random.normal(75000, 20000, n_rows),
                'start_date': pd.date_range('2015-01-01', periods=n_rows, freq='1D'),
                'is_active': np.random.choice([True, False], n_rows, p=[0.9, 0.1]),
                'performance_score': np.random.uniform(1.0, 5.0, n_rows)
            })
            plugin = PandasTablePlugin(enhanced_mode=True, row_threshold=10000, memory_threshold_mb=5)
        
        # Process the DataFrame
        table_component = plugin.process(df)
        
        # Add processing strategy info
        if hasattr(table_component, 'metadata') and 'processing_strategy' in table_component.metadata:
            strategy_info = table_component.metadata['processing_strategy']
            info_text = f"Processing Strategy: {strategy_info['strategy']}"
            info_text += f" | Rows: {strategy_info['memory_stats']['row_count']:,}"
            info_text += f" | Memory: {strategy_info['memory_stats']['total_memory_mb']:.2f} MB"
            
            return {
                "type": "div",
                "props": {
                    "children": [
                        {
                            "type": "div",
                            "props": {
                                "style": {
                                    "backgroundColor": "#f0f8ff",
                                    "padding": "10px",
                                    "borderRadius": "4px",
                                    "marginBottom": "10px",
                                    "border": "1px solid #add8e6"
                                },
                                "children": [
                                    {
                                        "type": "p",
                                        "props": {
                                            "content": info_text,
                                            "style": {"fontSize": "14px", "color": "#333", "margin": "0"}
                                        }
                                    }
                                ]
                            }
                        },
                        table_component.render()
                    ]
                }
            }
        
        return table_component.render()
    
    def _create_dtype_preservation_demo(self):
        """Create a demo showing dtype preservation."""
        # Create DataFrame with various dtypes and missing values
        df = pd.DataFrame({
            'integer_col': [1, 2, 3, None, 5],
            'float_col': [1.1, 2.2, np.nan, 4.4, 5.5],
            'string_col': ['A', 'B', None, 'D', 'E'],
            'bool_col': [True, False, None, True, False],
            'datetime_col': pd.date_range('2024-01-01', periods=5, freq='D'),
            'category_col': pd.Categorical(['X', 'Y', 'Z', 'X', 'Y'])
        })
        
        # Add some NaN values
        df.loc[2, 'datetime_col'] = pd.NaT
        df.loc[4, 'category_col'] = None
        
        # Process with enhanced plugin
        plugin = PandasTablePlugin(enhanced_mode=True)
        table_component = plugin.process(df)
        
        # Create info about dtypes
        dtype_info = []
        for col in df.columns:
            dtype_info.append(f"{col}: {df[col].dtype}")
        
        return {
            "type": "div",
            "props": {
                "children": [
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "backgroundColor": "#f0f8ff",
                                "padding": "10px",
                                "borderRadius": "4px",
                                "marginBottom": "10px",
                                "border": "1px solid #add8e6"
                            },
                            "children": [
                                {
                                    "type": "p",
                                    "props": {
                                        "content": "DataFrame dtypes: " + " | ".join(dtype_info),
                                        "style": {"fontSize": "14px", "color": "#333", "margin": "0"}
                                    }
                                }
                            ]
                        }
                    },
                    table_component.render()
                ]
            }
        }