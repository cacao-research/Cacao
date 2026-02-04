#!/usr/bin/env python3
"""
Debug script to test TableDataServer route registration issue.
This script will help validate our diagnosis by showing diagnostic logs.
"""

import sys
import os
import pandas as pd
import asyncio
import json
from urllib.parse import parse_qs

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cacao.ui.components.data.table.server import TableDataServer
from cacao.core.server import CacaoServer
from cacao.core.decorators import ROUTES, register_route

def test_route_registration():
    """Test route registration and see what diagnostic logs show."""
    print("🔍 Testing TableDataServer route registration...")
    
    # Create sample data
    test_data = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'city': ['New York', 'London', 'Tokyo']
    })
    
    # Create columns definition
    columns = [
        {"title": "Name", "dataIndex": "name"},
        {"title": "Age", "dataIndex": "age"},
        {"title": "City", "dataIndex": "city"}
    ]
    
    print(f"📋 Current ROUTES before registration: {list(ROUTES.keys())}")
    
    # Create TableDataServer instance
    table_id = "table_debug_test"
    server = TableDataServer(test_data, table_id, columns)
    
    print(f"📊 Created TableDataServer for {table_id}")
    print(f"🔗 Expected endpoint: {server.endpoint}")
    
    # Create a mock CacaoServer instance
    mock_server = CacaoServer()
    CacaoServer._instance = mock_server
    
    # Register the endpoint
    print("🔧 Registering endpoint...")
    server.register_endpoint(mock_server)
    
    print(f"📋 ROUTES after registration: {list(ROUTES.keys())}")
    print(f"🎯 Route handler: {ROUTES.get(server.endpoint)}")
    
    # Test if the route is registered
    if server.endpoint in ROUTES:
        print("✅ Route successfully registered!")
        
        # Test calling the route handler directly with different data formats
        print("\n🧪 Testing route handler calls...")
        
        # Test 1: Call with None (current server behavior)
        print("Test 1: Calling with (None, response_obj)")
        try:
            class MockResponse:
                def __init__(self):
                    self.headers = {}
            
            result = ROUTES[server.endpoint](None, MockResponse())
            print(f"❌ Unexpected success: {result}")
        except Exception as e:
            print(f"❌ Error (expected): {str(e)}")
        
        # Test 2: Call with proper request data
        print("\nTest 2: Calling with proper request data")
        try:
            test_request_data = {
                'draw': ['1'],
                'start': ['0'],
                'length': ['10'],
                'search[value]': ['']
            }
            result = ROUTES[server.endpoint](test_request_data)
            print(f"✅ Success: {type(result)}")
            print(f"📊 Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        # Test 3: Simulate POST data parsing
        print("\nTest 3: Simulating POST data")
        try:
            # Simulate what the server should parse from POST body
            post_body = "draw=1&start=0&length=10&search%5Bvalue%5D="
            parsed_data = parse_qs(post_body)
            print(f"📝 Parsed POST data: {parsed_data}")
            
            result = ROUTES[server.endpoint](parsed_data)
            print(f"✅ Success with POST data: {type(result)}")
            
            if isinstance(result, dict):
                print(f"📊 Response structure:")
                for key, value in result.items():
                    if key == 'data':
                        print(f"  {key}: {len(value)} records")
                    else:
                        print(f"  {key}: {value}")
        except Exception as e:
            print(f"❌ Error with POST data: {str(e)}")
            import traceback
            traceback.print_exc()
            
    else:
        print("❌ Route NOT registered!")
    
    print(f"\n📈 Final state:")
    print(f"  Registered routes: {list(ROUTES.keys())}")
    print(f"  Target endpoint: {server.endpoint}")
    print(f"  Registration status: {'✅ SUCCESS' if server.endpoint in ROUTES else '❌ FAILED'}")

if __name__ == "__main__":
    test_route_registration()