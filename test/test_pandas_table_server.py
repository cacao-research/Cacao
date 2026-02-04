"""
Test suite for pandas DataFrame integration with Cacao Table component
"""

import unittest
import sys
import os
import json
import threading
import time
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path so we can import cacao modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    pd = None

from cacao.ui.components.data.table.table import Table
if HAS_PANDAS:
    from cacao.ui.components.data.table.server import TableDataServer, create_table_data_server


@unittest.skipIf(not HAS_PANDAS, "pandas not available")
class TestTableDataServer(unittest.TestCase):
    """Test TableDataServer functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.sample_data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'age': [25, 30, 35, 40, 45],
            'city': ['New York', 'London', 'Paris', 'Tokyo', 'Berlin'],
            'salary': [50000, 60000, 70000, 80000, 90000]
        })
        
        self.columns = [
            {"title": "ID", "dataIndex": "id"},
            {"title": "Name", "dataIndex": "name"},
            {"title": "Age", "dataIndex": "age"},
            {"title": "City", "dataIndex": "city"},
            {"title": "Salary", "dataIndex": "salary"}
        ]
    
    def test_server_creation(self):
        """Test TableDataServer creation."""
        server = TableDataServer(self.sample_data, "test_table", self.columns)
        
        self.assertEqual(server.table_id, "test_table")
        self.assertEqual(len(server.dataframe), 5)
        self.assertEqual(len(server.columns), 5)
        self.assertTrue(server.endpoint.startswith("/api/table-data/"))
    
    def test_search_functionality(self):
        """Test search functionality."""
        server = TableDataServer(self.sample_data, "test_table", self.columns)
        
        # Test search for "Alice"
        filtered_df = server._apply_search(server.dataframe, "Alice")
        self.assertEqual(len(filtered_df), 1)
        self.assertEqual(filtered_df.iloc[0]['name'], 'Alice')
        
        # Test search for "New"
        filtered_df = server._apply_search(server.dataframe, "New")
        self.assertEqual(len(filtered_df), 1)
        self.assertEqual(filtered_df.iloc[0]['city'], 'New York')
        
        # Test numeric search
        filtered_df = server._apply_search(server.dataframe, "25")
        self.assertEqual(len(filtered_df), 1)
        self.assertEqual(filtered_df.iloc[0]['age'], 25)
    
    def test_sorting_functionality(self):
        """Test sorting functionality."""
        server = TableDataServer(self.sample_data, "test_table", self.columns)
        
        # Test ascending sort by name (column 1)
        order_params = [{'column': 1, 'dir': 'asc'}]
        sorted_df = server._apply_sorting(server.dataframe, order_params)
        names = sorted_df['name'].tolist()
        self.assertEqual(names, ['Alice', 'Bob', 'Charlie', 'David', 'Eve'])
        
        # Test descending sort by age (column 2)
        order_params = [{'column': 2, 'dir': 'desc'}]
        sorted_df = server._apply_sorting(server.dataframe, order_params)
        ages = sorted_df['age'].tolist()
        self.assertEqual(ages, [45, 40, 35, 30, 25])
    
    def test_pagination_functionality(self):
        """Test pagination functionality."""
        server = TableDataServer(self.sample_data, "test_table", self.columns)
        
        # Test first page (2 records per page)
        paginated_df = server._apply_pagination(server.dataframe, 0, 2)
        self.assertEqual(len(paginated_df), 2)
        self.assertEqual(paginated_df.iloc[0]['id'], 1)
        self.assertEqual(paginated_df.iloc[1]['id'], 2)
        
        # Test second page
        paginated_df = server._apply_pagination(server.dataframe, 2, 2)
        self.assertEqual(len(paginated_df), 2)
        self.assertEqual(paginated_df.iloc[0]['id'], 3)
        self.assertEqual(paginated_df.iloc[1]['id'], 4)
        
        # Test last page (partial)
        paginated_df = server._apply_pagination(server.dataframe, 4, 2)
        self.assertEqual(len(paginated_df), 1)
        self.assertEqual(paginated_df.iloc[0]['id'], 5)
    
    def test_handle_request(self):
        """Test request handling."""
        server = TableDataServer(self.sample_data, "test_table", self.columns)
        
        # Mock request data
        request_data = {
            'draw': 1,
            'start': 0,
            'length': 3,
            'search[value]': '',
            'order[0][column]': 1,
            'order[0][dir]': 'asc'
        }
        
        response = server.handle_request(request_data)
        
        self.assertEqual(response['draw'], 1)
        self.assertEqual(response['recordsTotal'], 5)
        self.assertEqual(response['recordsFiltered'], 5)
        self.assertEqual(len(response['data']), 3)
        
        # Check that data is sorted by name (Alice, Bob, Charlie)
        self.assertEqual(response['data'][0][1], 'Alice')  # name column
        self.assertEqual(response['data'][1][1], 'Bob')
        self.assertEqual(response['data'][2][1], 'Charlie')
    
    def test_handle_request_with_search(self):
        """Test request handling with search."""
        server = TableDataServer(self.sample_data, "test_table", self.columns)
        
        # Mock request data with search
        request_data = {
            'draw': 2,
            'start': 0,
            'length': 10,
            'search[value]': 'London',
        }
        
        response = server.handle_request(request_data)
        
        self.assertEqual(response['draw'], 2)
        self.assertEqual(response['recordsTotal'], 5)
        self.assertEqual(response['recordsFiltered'], 1)
        self.assertEqual(len(response['data']), 1)
        self.assertEqual(response['data'][0][1], 'Bob')  # Bob lives in London
    
    def test_thread_safety(self):
        """Test thread safety of the server."""
        server = TableDataServer(self.sample_data, "test_table", self.columns)
        results = []
        errors = []
        
        def worker():
            try:
                request_data = {
                    'draw': 1,
                    'start': 0,
                    'length': 5,
                    'search[value]': '',
                }
                response = server.handle_request(request_data)
                results.append(response)
            except Exception as e:
                errors.append(e)
        
        # Create multiple threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        self.assertEqual(len(errors), 0, f"Errors occurred: {errors}")
        self.assertEqual(len(results), 10)
        
        # All results should be identical
        for result in results:
            self.assertEqual(result['recordsTotal'], 5)
            self.assertEqual(result['recordsFiltered'], 5)
            self.assertEqual(len(result['data']), 5)
    
    def test_data_update(self):
        """Test data update functionality."""
        server = TableDataServer(self.sample_data, "test_table", self.columns)
        
        # Update data
        new_data = pd.DataFrame({
            'id': [6, 7, 8],
            'name': ['Frank', 'Grace', 'Henry'],
            'age': [50, 55, 60],
            'city': ['Sydney', 'Mumbai', 'Cairo'],
            'salary': [100000, 110000, 120000]
        })
        
        server.update_data(new_data)
        
        self.assertEqual(len(server.dataframe), 3)
        self.assertEqual(len(server.original_dataframe), 3)
        
        # Test request with updated data
        request_data = {
            'draw': 1,
            'start': 0,
            'length': 10,
            'search[value]': '',
        }
        
        response = server.handle_request(request_data)
        self.assertEqual(response['recordsTotal'], 3)
        self.assertEqual(response['recordsFiltered'], 3)


@unittest.skipIf(not HAS_PANDAS, "pandas not available")
class TestTablePandasIntegration(unittest.TestCase):
    """Test Table component integration with pandas DataFrames."""
    
    def setUp(self):
        """Set up test data."""
        self.sample_data = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'city': ['New York', 'London', 'Paris']
        })
    
    def test_pandas_dataframe_detection(self):
        """Test pandas DataFrame detection."""
        table = Table(dataSource=self.sample_data)
        self.assertTrue(table._is_pandas_dataframe(self.sample_data))
        self.assertFalse(table._is_pandas_dataframe([]))
        self.assertFalse(table._is_pandas_dataframe({}))
    
    def test_column_generation_from_dataframe(self):
        """Test automatic column generation from DataFrame."""
        table = Table(dataSource=self.sample_data)
        columns = table._generate_columns_from_dataframe(self.sample_data)
        
        self.assertEqual(len(columns), 3)
        self.assertEqual(columns[0]['title'], 'name')
        self.assertEqual(columns[0]['dataIndex'], 'name')
        self.assertEqual(columns[1]['title'], 'age')
        self.assertEqual(columns[2]['title'], 'city')
    
    def test_pandas_server_setup(self):
        """Test pandas server setup."""
        table = Table(dataSource=self.sample_data)
        
        # Mock the server setup to avoid actual server registration
        with patch.object(table, '_setup_pandas_server') as mock_setup:
            mock_setup.return_value = {
                "table_id": "test_table_123",
                "endpoint": "/api/table-data/test_table_123",
                "server": Mock()
            }
            
            result = table.render()
            
            # Verify that advanced mode was enabled
            self.assertTrue(result['props']['advanced'])
            self.assertTrue(result['props']['server_side'])
    
    def test_render_with_pandas_dataframe(self):
        """Test rendering with pandas DataFrame (without server setup)."""
        # Create table with DataFrame
        table = Table(dataSource=self.sample_data)
        
        # Mock the server setup to avoid actual registration
        with patch.object(table, '_setup_pandas_server') as mock_setup:
            mock_setup.return_value = {
                "table_id": "test_table_456",
                "endpoint": "/api/table-data/test_table_456",
                "server": Mock()
            }
            
            result = table.render()
            
            # Verify structure
            self.assertEqual(result['type'], 'table')
            self.assertTrue(result['props']['advanced'])
            self.assertTrue(result['props']['server_side'])
            self.assertEqual(len(result['props']['columns']), 3)
            
            # Verify pandas server info is included
            self.assertIn('pandas_server', result['props'])
            self.assertEqual(result['props']['pandas_server']['table_id'], 'test_table_456')
            self.assertTrue(result['props']['pandas_server']['enabled'])


class TestCreateTableDataServer(unittest.TestCase):
    """Test the create_table_data_server factory function."""
    
    @unittest.skipIf(not HAS_PANDAS, "pandas not available")
    def test_create_table_data_server(self):
        """Test create_table_data_server function."""
        sample_data = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })
        
        server = create_table_data_server(sample_data)
        
        self.assertIsInstance(server, TableDataServer)
        self.assertEqual(len(server.dataframe), 3)
        self.assertTrue(server.table_id.startswith("table_"))


if __name__ == '__main__':
    unittest.main()