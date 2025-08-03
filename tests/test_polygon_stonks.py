"""
Tests for polygon_stonks library.
"""

import unittest
from unittest.mock import Mock, patch
from polygon_stonks_lib import GapAnalyzer, calculate_overnight_change


class TestUtils(unittest.TestCase):
    
    def test_calculate_overnight_change(self):
        # Test normal case
        result = calculate_overnight_change(80, 100)
        self.assertEqual(result, -0.2)
        
        # Test zero previous close
        result = calculate_overnight_change(80, 0)
        self.assertEqual(result, 0)
        
        # Test positive change
        result = calculate_overnight_change(120, 100)
        self.assertEqual(result, 0.2)


class TestGapAnalyzer(unittest.TestCase):
    
    def setUp(self):
        self.analyzer = GapAnalyzer("test_api_key")
    
    def test_initialization(self):
        self.assertIsNotNone(self.analyzer.client)
        self.assertIsNone(self.analyzer.snapshot_data)
    
    @patch('polygon_stonks.gap_analyzer.RESTClient')
    def test_fetch_snapshot(self, mock_client):
        mock_data = [Mock()]
        mock_client.return_value.get_snapshot_all.return_value = mock_data
        
        result = self.analyzer.fetch_snapshot()
        
        self.assertEqual(result, mock_data)
        self.assertEqual(self.analyzer.snapshot_data, mock_data)


if __name__ == '__main__':
    unittest.main()
