#!/usr/bin/env python3
"""
Test the Table component's server import in the same context as the running app
"""

import pandas as pd
import traceback

print("Testing Table component's server import in application context...")

# Create sample data like the example does
sample_data = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['NYC', 'LA', 'Chicago']
})

try:
    print("Step 1: Import Table component...")
    from cacao.ui.components.data.table.table import Table
    print("✅ Table component imported successfully")
    
    print("Step 2: Create Table instance with pandas DataFrame...")
    columns = [
        {"title": "Name", "dataIndex": "name", "key": "name"},
        {"title": "Age", "dataIndex": "age", "key": "age"},
        {"title": "City", "dataIndex": "city", "key": "city"}
    ]
    
    table = Table(
        columns=columns,
        dataSource=sample_data,
        advanced=True
    )
    print("✅ Table instance created successfully")
    
    print("Step 3: Test server import within Table context...")
    # This mimics what happens in _setup_pandas_server
    from cacao.ui.components.data.table.server import create_table_data_server
    print("✅ create_table_data_server imported successfully in Table context")
    
    print("Step 4: Test the actual _setup_pandas_server method...")
    server_info = table._setup_pandas_server(sample_data)
    print(f"✅ _setup_pandas_server succeeded: {server_info}")
    
    print("Step 5: Test table rendering...")
    rendered = table.render()
    print("✅ Table rendering successful")
    print(f"Pandas server enabled: {rendered['props'].get('pandas_server', {}).get('enabled', False)}")
    
    print("\n🎉 All table operations successful!")
    
except ImportError as e:
    print(f"❌ ImportError: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    
except Exception as e:
    print(f"❌ Runtime error: {e}")
    print("\nFull traceback:")
    traceback.print_exc()