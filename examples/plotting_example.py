"""
Cacao Plotting Example

Demonstrates:
- Interactive data visualization
- Reactive state management
- Component-based plotting
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from cacao import mix, State, Component
from datetime import datetime, timedelta

class DataVisualization(Component):
    def __init__(self):
        super().__init__()
        # Generate sample time series data
        np.random.seed(42)
        dates = pd.date_range(end=datetime.now(), periods=100)
        
        # Create sample DataFrame
        self.df = pd.DataFrame({
            'Date': dates,
            'Sales A': np.cumsum(np.random.normal(5, 2, 100)),
            'Sales B': np.cumsum(np.random.normal(4, 1.5, 100)),
            'Category': np.random.choice(['Online', 'Offline'], 100)
        })
        
        # Reactive states for visualization
        self.plot_type = State('line')
        self.x_column = State('Date')
        self.y_column = State('Sales A')

    def generate_plot(self):
        """Generate plot based on current state"""
        plt.figure(figsize=(10, 6))
        plt.title(f"{self.plot_type.value.capitalize()} Plot")
        
        if self.plot_type.value == 'line':
            plt.plot(self.df[self.x_column.value], self.df[self.y_column.value], label=self.y_column.value)
            plt.xlabel(self.x_column.value)
            plt.ylabel(self.y_column.value)
        
        elif self.plot_type.value == 'scatter':
            plt.scatter(self.df[self.x_column.value], self.df[self.y_column.value], alpha=0.6)
            plt.xlabel(self.x_column.value)
            plt.ylabel(self.y_column.value)
        
        elif self.plot_type.value == 'boxplot':
            sns.boxplot(x='Category', y=self.y_column.value, data=self.df)
        
        plt.legend()
        plt.tight_layout()
        plt.savefig('visualization.png')
        plt.close()

    def render(self):
        # Prepare column options
        numeric_columns = list(self.df.select_dtypes(include=[np.number]).columns)
        
        return {
            "type": "section",
            "props": {
                "children": [
                    {
                        "type": "text",
                        "props": {
                            "content": "Interactive Data Visualization",
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
                                        "label": "Plot Type",
                                        "options": [
                                            {"value": "line", "label": "Line Plot"},
                                            {"value": "scatter", "label": "Scatter Plot"},
                                            {"value": "boxplot", "label": "Box Plot"}
                                        ],
                                        "value": self.plot_type.value,
                                        "onChange": lambda v: [
                                            self.plot_type.set(v),
                                            self.generate_plot()
                                        ]
                                    }
                                },
                                {
                                    "type": "select",
                                    "props": {
                                        "label": "X Axis Column",
                                        "options": [{"value": col, "label": col} for col in self.df.columns],
                                        "value": self.x_column.value,
                                        "onChange": lambda v: [
                                            self.x_column.set(v),
                                            self.generate_plot()
                                        ]
                                    }
                                },
                                {
                                    "type": "select",
                                    "props": {
                                        "label": "Y Axis Column",
                                        "options": [{"value": col, "label": col} for col in numeric_columns],
                                        "value": self.y_column.value,
                                        "onChange": lambda v: [
                                            self.y_column.set(v),
                                            self.generate_plot()
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "type": "button",
                        "props": {
                            "label": "Generate Plot",
                            "onClick": self.generate_plot
                        }
                    },
                    {
                        "type": "image",
                        "props": {
                            "src": "visualization.png",
                            "alt": "Generated Visualization",
                            "style": {
                                "max-width": "100%",
                                "height": "auto",
                                "margin-top": "20px"
                            }
                        }
                    }
                ]
            }
        }

@mix("/")
def plotting_example_route():
    # Initial plot generation
    data_viz = DataVisualization()
    data_viz.generate_plot()  # Generate initial plot
    
    return {
        "layout": "column",
        "children": [
            {
                "type": "navbar",
                "props": {
                    "brand": "Cacao Plotting Example",
                    "links": [
                        {"name": "Home", "url": "/"}
                    ]
                }
            },
            data_viz,
            {
                "type": "footer",
                "props": {"text": "© 2025 Cacao Framework"}
            }
        ]
    }

# Optional: Print DataFrame info for CLI users
if __name__ == "__main__":
    data_viz = DataVisualization()
    print("Sample DataFrame:")
    print(data_viz.df.head())
    print("\nDataFrame Info:")
    data_viz.df.info()
    
    # Generate initial plot for CLI
    data_viz.generate_plot()
    print("\nPlot saved as visualization.png")
