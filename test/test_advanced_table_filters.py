"""
Test Advanced Table Filter Panel Functionality
Tests the new column-specific and advanced filtering capabilities
"""

import unittest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from cacao.ui.components.data.table.table import Table
from cacao.ui.components.data.table.server import TableDataServer, create_table_data_server

class TestAdvancedTableFilters(unittest.TestCase):
    """Test cases for advanced table filtering functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create sample DataFrame
        np.random.seed(42)
        self.test_data = pd.DataFrame({
            'name': ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince', 'Edward Norton'],
            'department': ['Engineering', 'Sales', 'Engineering', 'Marketing', 'Sales'],
            'salary': [85000, 65000, 92000, 58000, 78000],
            'age': [28, 35, 31, 29, 42],
            'city': ['New York', 'San Francisco', 'New York', 'Chicago', 'Boston'],
            'active': [True, True, False, True, True]
        })
        
        self.columns = [
            {"title": "Name", "dataIndex": "name", "key": "name"},
            {"title": "Department", "dataIndex": "department", "key": "department"},
            {"title": "Salary", "dataIndex": "salary", "key": "salary", "type": "number"},
            {"title": "Age", "dataIndex": "age", "key": "age", "type": "number"},
            {"title": "City", "dataIndex": "city", "key": "city"},
            {"title": "Active", "dataIndex": "active", "key": "active"}
        ]
    
    def test_column_specific_filtering(self):
        """Test column-specific filtering functionality."""
        server = TableDataServer(self.test_data, "test_table", self.columns)
        
        # Test string filtering
        column_filters = {1: "eng"}  # Filter department column for "eng"
        filtered_df = server._apply_column_filters(self.test_data, column_filters)
        
        # Should return rows with "Engineering" department
        self.assertEqual(len(filtered_df), 2)
        self.assertTrue(all("Engineering" in dept for dept in filtered_df['department']))
    
    def test_numeric_range_filtering(self):
        """Test numeric range filtering."""
        server = TableDataServer(self.test_data, "test_table", self.columns)
        
        # Test salary range filtering: 60000-80000
        column_filters = {2: "60000-80000"}  # Salary column
        filtered_df = server._apply_column_filters(self.test_data, column_filters)
        
        # Should return rows with salary between 60000 and 80000
        self.assertEqual(len(filtered_df), 3)  # Bob (65000), Diana (58000), Edward (78000)
        self.assertTrue(all(58000 <= salary <= 80000 for salary in filtered_df['salary']))
    
    def test_advanced_filtering_contains(self):
        """Test advanced filtering with 'contains' filter type."""
        server = TableDataServer(self.test_data, "test_table", self.columns)
        
        advanced_filters = {
            "name": {"type": "contains", "value": "son"}
        }
        
        filtered_df = server._apply_advanced_filters(self.test_data, advanced_filters)
        
        # Should return Alice Johnson
        self.assertEqual(len(filtered_df), 1)
        self.assertEqual(filtered_df.iloc[0]['name'], 'Alice Johnson')
    
    def test_advanced_filtering_equals(self):
        """Test advanced filtering with 'equals' filter type."""
        server = TableDataServer(self.test_data, "test_table", self.columns)
        
        advanced_filters = {
            "department": {"type": "equals", "value": "Sales"}
        }
        
        filtered_df = server._apply_advanced_filters(self.test_data, advanced_filters)
        
        # Should return Bob and Edward
        self.assertEqual(len(filtered_df), 2)
        self.assertTrue(all(dept == "Sales" for dept in filtered_df['department']))
    
    def test_advanced_filtering_greater_than(self):
        """Test advanced filtering with 'greater_than' filter type."""
        server = TableDataServer(self.test_data, "test_table", self.columns)
        
        advanced_filters = {
            "salary": {"type": "greater_than", "value": "80000"}
        }
        
        filtered_df = server._apply_advanced_filters(self.test_data, advanced_filters)
        
        # Should return Alice (85000) and Charlie (92000)
        self.assertEqual(len(filtered_df), 2)
        self.assertTrue(all(salary > 80000 for salary in filtered_df['salary']))
    
    def test_advanced_filtering_range(self):
        """Test advanced filtering with 'range' filter type."""
        server = TableDataServer(self.test_data, "test_table", self.columns)
        
        advanced_filters = {
            "age": {"type": "range", "min": 30, "max": 40}
        }
        
        filtered_df = server._apply_advanced_filters(self.test_data, advanced_filters)
        
        # Should return Bob (35) and Charlie (31)
        self.assertEqual(len(filtered_df), 2)
        self.assertTrue(all(30 <= age <= 40 for age in filtered_df['age']))
    
    def test_multiple_advanced_filters(self):
        """Test applying multiple advanced filters simultaneously."""
        server = TableDataServer(self.test_data, "test_table", self.columns)
        
        advanced_filters = {
            "department": {"type": "equals", "value": "Engineering"},
            "salary": {"type": "greater_than", "value": "80000"}
        }
        
        filtered_df = server._apply_advanced_filters(self.test_data, advanced_filters)
        
        # Should return only Charlie (Engineering + salary > 80000)
        self.assertEqual(len(filtered_df), 1)
        self.assertEqual(filtered_df.iloc[0]['name'], 'Charlie Brown')
    
    def test_filter_request_handling(self):
        """Test complete filter request handling with DataTables protocol."""
        server = TableDataServer(self.test_data, "test_table", self.columns)
        
        # Simulate DataTables request with advanced filters
        request_data = {
            'draw': ['1'],
            'start': ['0'],
            'length': ['10'],
            'search[value]': [''],
            'advanced_filters': ['{"name": {"type": "contains", "value": "o"}}']
        }
        
        response = server.handle_request(request_data)
        
        # Should return proper DataTables response
        self.assertIn('draw', response)
        self.assertIn('recordsTotal', response)
        self.assertIn('recordsFiltered', response)
        self.assertIn('data', response)
        
        # Should filter for names containing "o" (Bob, Charlie, Norton)
        self.assertEqual(response['recordsFiltered'], 3)
        self.assertEqual(len(response['data']), 3)
    
    @patch('cacao.core.server.CacaoServer')
    def test_table_with_filter_panel_integration(self, mock_server):
        """Test Table component integration with filter panel."""
        # Mock server instance
        mock_server._instance = Mock()
        
        # Create table with pandas DataFrame
        table = Table(
            columns=self.columns,
            dataSource=self.test_data,
            advanced=True,
            show_length_menu=True
        )
        
        # Render the table
        result = table.render()
        
        # Should auto-enable advanced mode and server-side processing
        self.assertTrue(result['props']['advanced'])
        self.assertTrue(result['props']['server_side'])
        self.assertIsNotNone(result['props']['ajax_url'])
        
        # Should include pandas server info
        self.assertIn('pandas_server', result['props'])
        self.assertTrue(result['props']['pandas_server']['enabled'])
    
    def test_filter_panel_with_empty_dataframe(self):
        """Test filter panel behavior with empty DataFrame."""
        empty_df = pd.DataFrame(columns=['name', 'value'])
        server = TableDataServer(empty_df, "empty_table", [])
        
        # Should handle empty DataFrame gracefully
        filtered_df = server._apply_column_filters(empty_df, {0: "test"})
        self.assertTrue(filtered_df.empty)
        
        advanced_filters = {"name": {"type": "contains", "value": "test"}}
        filtered_df = server._apply_advanced_filters(empty_df, advanced_filters)
        self.assertTrue(filtered_df.empty)
    
    def test_filter_error_handling(self):
        """Test error handling in filter operations."""
        server = TableDataServer(self.test_data, "test_table", self.columns)
        
        # Test with invalid column index
        column_filters = {999: "test"}  # Invalid column index
        filtered_df = server._apply_column_filters(self.test_data, column_filters)
        
        # Should return original DataFrame when filter fails
        self.assertEqual(len(filtered_df), len(self.test_data))
        
        # Test with invalid advanced filter
        advanced_filters = {
            "nonexistent_column": {"type": "contains", "value": "test"}
        }
        filtered_df = server._apply_advanced_filters(self.test_data, advanced_filters)
        
        # Should return original DataFrame
        self.assertEqual(len(filtered_df), len(self.test_data))

def run_filter_tests():
    """Run all filter panel tests."""
    unittest.main(verbosity=2)

if __name__ == '__main__':
    run_filter_tests()