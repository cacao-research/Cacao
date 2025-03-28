"""
Cacao Pandas Table Plugin Example

Demonstrates:
- Interactive DataFrame rendering
- Pagination
- Sorting
- Plugin-based table visualization
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from cacao import mix, Component

def create_sample_dataframe():
    """
    Create a comprehensive sample DataFrame for table demonstration.
    
    Includes various data types and complex structures to showcase
    the pandas table plugin's capabilities.
    """
    np.random.seed(42)
    
    # Generate dates
    dates = [datetime.now() - timedelta(days=x) for x in range(100)]
    
    # Create DataFrame with diverse data
    df = pd.DataFrame({
        'Date': dates,
        'Customer ID': np.random.randint(1000, 9999, 100),
        'Product Category': np.random.choice([
            'Electronics', 'Clothing', 'Books', 
            'Home & Kitchen', 'Sports'
        ], 100),
        'Sales Amount': np.random.normal(500, 150, 100),
        'Quantity': np.random.randint(1, 10, 100),
        'Discount %': np.round(np.random.uniform(0, 0.3, 100), 2),
        'Is Repeat Customer': np.random.choice([True, False], 100),
        'Rating': np.round(np.random.uniform(1, 5, 100), 1)
    })
    
    # Add calculated columns
    df['Total Revenue'] = df['Sales Amount'] * (1 - df['Discount %'])
    df['Profit Margin'] = np.round(np.random.uniform(0.1, 0.4, 100), 2)
    
    return df

@mix("/")
def pandas_table_route():
    """
    Main route for the Pandas Table Example.
    Demonstrates plugin-based table rendering.
    """
    # Create sample DataFrame
    df = create_sample_dataframe()
    
    return {
        "layout": "column",
        "children": [
            {
                "type": "navbar",
                "props": {
                    "brand": "Cacao Pandas Table Plugin",
                    "links": [
                        {"name": "Home", "url": "/"}
                    ]
                }
            },
            {
                "type": "section",
                "props": {
                    "children": [
                        {
                            "type": "text",
                            "props": {
                                "content": "Sales Data Interactive Table",
                                "style": {
                                    "font-size": "24px",
                                    "margin-bottom": "20px"
                                }
                            }
                        },
                        df  # This will be automatically converted by the pandas table plugin
                    ]
                }
            },
            {
                "type": "footer",
                "props": {"text": "© 2025 Cacao Framework"}
            }
        ]
    }

# Optional: Print DataFrame info for CLI users
if __name__ == "__main__":
    df = create_sample_dataframe()
    print("Sample Sales DataFrame:")
    print(df.head())
    print("\nDataFrame Information:")
    df.info()
    print("\nBasic Statistics:")
    print(df.describe())
