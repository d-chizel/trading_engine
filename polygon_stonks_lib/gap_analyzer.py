"""
Gap Analyzer class for identifying gapped stocks using Polygon.io API.
"""

import pandas as pd
from polygon import RESTClient
from polygon.rest.models import TickerSnapshot, Agg
from .utils import calculate_overnight_change, validate_ticker_data


class GapAnalyzer:
    """
    A class for analyzing stock gaps using Polygon.io API data.
    """
    
    def __init__(self, api_key):
        """
        Initialize the GapAnalyzer with Polygon.io API key.
        
        Args:
            api_key (str): Your Polygon.io API key
        """
        self.client = RESTClient(api_key)
        self.snapshot_data = None
        
    def fetch_snapshot(self, market_type="stocks"):
        """
        Fetch snapshot data from Polygon.io API.
        
        Args:
            market_type (str): Type of market data to fetch (default: "stocks")
            
        Returns:
            The snapshot data
        """
        self.snapshot_data = self.client.get_snapshot_all(market_type)
        return self.snapshot_data
    
    def get_gapped_stocks(self, gap_threshold=0.2, gap_direction="down"):
        """
        Get stocks that have gapped based on the threshold.
        
        Args:
            gap_threshold (float): Minimum gap percentage (as decimal, e.g., 0.2 for 20%)
            gap_direction (str): Direction of gap - "down", "up", or "both"
            
        Returns:
            list: List of ticker symbols that meet the gap criteria
        """
        if not self.snapshot_data:
            raise ValueError("No snapshot data available. Call fetch_snapshot() first.")
            
        gapped_stocks = []
        
        for item in self.snapshot_data:
            if isinstance(item, TickerSnapshot) and isinstance(item.prev_day, Agg):
                if (isinstance(item.prev_day.open, float) and 
                    isinstance(item.prev_day.close, float) and
                    validate_ticker_data(item)):
                    
                    overnight_change = calculate_overnight_change(
                        item.min.close, item.prev_day.close
                    )
                    
                    # Check gap direction
                    if gap_direction == "down" and overnight_change < -gap_threshold:
                        gapped_stocks.append(item.ticker)
                    elif gap_direction == "up" and overnight_change > gap_threshold:
                        gapped_stocks.append(item.ticker)
                    elif gap_direction == "both" and abs(overnight_change) > gap_threshold:
                        gapped_stocks.append(item.ticker)
        
        return gapped_stocks
    
    def create_dataframe(self):
        """
        Create a pandas DataFrame from the snapshot data.
        
        Returns:
            pd.DataFrame: DataFrame containing stock data
        """
        if not self.snapshot_data:
            raise ValueError("No snapshot data available. Call fetch_snapshot() first.")
            
        data_rows = []
        
        for item in self.snapshot_data:
            if isinstance(item, TickerSnapshot) and isinstance(item.prev_day, Agg):
                if (isinstance(item.prev_day.open, float) and 
                    isinstance(item.prev_day.close, float)):
                    
                    overnight_change = 0
                    if validate_ticker_data(item):
                        overnight_change = calculate_overnight_change(
                            item.min.close, item.prev_day.close
                        )
                    
                    row_data = {
                        'ticker': item.ticker,
                        'prev_open': item.prev_day.open,
                        'prev_close': item.prev_day.close,
                        'prev_high': getattr(item.prev_day, 'high', None),
                        'prev_low': getattr(item.prev_day, 'low', None),
                        'prev_volume': getattr(item.prev_day, 'volume', None),
                        'min_close': getattr(item.min, 'close', None) if hasattr(item, 'min') else None,
                        'overnight_change': overnight_change,
                    }
                    data_rows.append(row_data)
        
        return pd.DataFrame(data_rows)
    
    def analyze_gaps(self, gap_threshold=0.2, gap_direction="down"):
        """
        Perform complete gap analysis and return both gapped stocks and DataFrame.
        
        Args:
            gap_threshold (float): Minimum gap percentage (as decimal)
            gap_direction (str): Direction of gap - "down", "up", or "both"
            
        Returns:
            dict: Dictionary containing 'gapped_stocks' list and 'dataframe'
        """
        if not self.snapshot_data:
            self.fetch_snapshot()
            
        gapped_stocks = self.get_gapped_stocks(gap_threshold, gap_direction)
        dataframe = self.create_dataframe()
        
        return {
            'gapped_stocks': gapped_stocks,
            'dataframe': dataframe,
            'total_stocks': len(dataframe),
            'gapped_count': len(gapped_stocks)
        }
