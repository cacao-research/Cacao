"""
Cacao Pandas Example

Demonstrates:
- DataFrame manipulation
- Data visualization
- Reactive state management
- Component-based UI
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from cacao import mix, State, Component
from datetime import datetime, timedelta

class DataFrameViewer(Component):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.current_view = State(df)
        self.group_by_column = State(None)
        self.aggregation_method = State('mean')

    def render(self):
        # Prepare grouping options
        columns = list(self.df.select_dtypes(include=[np.number]).columns)
        
        return {
            "type": "section",
            "props": {
                "children": [
                    {
                        "type": "text",
                        "props": {
                            "content": "DataFrame Viewer",
                            "style": {"font-size": "24px", "margin-bottom": "20px"}
                        }
                    },
                    {
                        "type": "section",
                        "props": {
                            "children": [
                                {
                                    "type": "select",
                                    "props": {
                                        "label": "Group By Column",
                                        "options": [{"value": col, "label": col} for col in columns],
                                        "value": self.group_by_column.value,
                                        "onChange": lambda v: self.group_by_column.set(v)
                                    }
                                },
                                {
                                    "type": "select",
                                    "props": {
                                        "label": "Aggregation Method",
                                        "options": [
                                            {"value": "mean", "label": "Mean"},
                                            {"value": "sum", "label": "Sum"},
                                            {"value": "count", "label": "Count"},
                                            {"value": "max", "label": "Max"},
                                            {"value": "min", "label": "Min"}
                                        ],
                                        "value": self.aggregation_method.value,
                                        "onChange": lambda v: self.aggregation_method.set(v)
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "type": "button",
                        "props": {
                            "label": "Apply Grouping",
                            "onClick": self.apply_grouping
                        }
                    },
                    {
                        "type": "table",
                        "props": {
                            "headers": list(self.current_view.value.columns),
                            "rows": self.current_view.value.head(10).values.tolist()
                        }
                    }
                ]
            }
        }

    def apply_grouping(self):
        """Apply grouping and aggregation to the DataFrame"""
        if self.group_by_column.value:
            grouped_df = self.df.groupby(self.group_by_column.value).agg({
                col: self.aggregation_method.value 
                for col in self.df.select_dtypes(include=[np.number]).columns 
                if col != self.group_by_column.value
            }).reset_index()
            self.current_view.set(grouped_df)
        else:
            self.current_view.set(self.df)

def create_sample_dataframe():
    """Create a sample DataFrame with various data types and complexity"""
    np.random.seed(42)
    
    # Generate dates
    dates = [datetime.now() - timedelta(days=x) for x in range(100)]
    
    # Create DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Category': np.random.choice(['A', 'B', 'C', 'D'], 100),
        'Sales': np.random.normal(1000, 200, 100),
        'Quantity': np.random.randint(1, 50, 100),
        'Discount': np.random.uniform(0, 0.2, 100),
        'IsPromotion': np.random.choice([True, False], 100)
    })
    
    # Add calculated columns
    df['Revenue'] = df['Sales'] * (1 - df['Discount'])
    df['ProfitMargin'] = np.random.uniform(0.1, 0.3, 100)
    
    return df

@mix("/")
def pandas_example_route():
    # Create sample DataFrame
    df = create_sample_dataframe()
    
    return {
        "layout": "column",
        "children": [
            {
                "type": "navbar",
                "props": {
                    "brand": "Cacao Pandas Example",
                    "links": [
                        {"name": "Home", "url": "/"}
                    ]
                }
            },
            DataFrameViewer(df),
            {
                "type": "footer",
                "props": {"text": "© 2025 Cacao Framework"}
            }
        ]
    }

# Optional: Print DataFrame info for CLI users
if __name__ == "__main__":
    df = create_sample_dataframe()
    print("Sample DataFrame:")
    print(df.head())
    print("\nDataFrame Info:")
    df.info()
