#!/usr/bin/env python3
"""
Quick test to debug the TableDataServer import issue
"""

import sys
import traceback

print("Testing TableDataServer import...")
print(f"Python path: {sys.path}")
print()

try:
    print("Step 1: Testing basic imports...")
    import pandas as pd
    print("✅ pandas import successful")
    
    print("Step 2: Testing core imports...")
    from cacao.core.server import CacaoServer
    print("✅ CacaoServer import successful")
    
    from cacao.core.mixins.logging import LoggingMixin
    print("✅ LoggingMixin import successful")
    
    from cacao.core.decorators import register_route
    print("✅ register_route function import successful")
    
    print("Step 3: Testing server.py import...")
    from cacao.ui.components.data.table.server import TableDataServer
    print("✅ TableDataServer import successful")
    
    print("Step 4: Testing create_table_data_server function...")
    from cacao.ui.components.data.table.server import create_table_data_server
    print("✅ create_table_data_server import successful")
    
    print("\n🎉 All imports successful! The issue might be elsewhere.")
    
except ImportError as e:
    print(f"❌ ImportError: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    print("\nFull traceback:")
    traceback.print_exc()