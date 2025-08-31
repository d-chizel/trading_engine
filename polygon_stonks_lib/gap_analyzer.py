"""
Gap Analyzer class for identifying gapped stocks using Polygon.io API.
"""

from tracemalloc import start
from xmlrpc import client
import pandas as pd
from polygon import RESTClient
from polygon.rest.models import TickerSnapshot, Agg
from .utils import calculate_overnight_change, validate_ticker_data, find_ny_times_in_data
import json


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
        
    def fetch_snapshot(self, market_type="stocks", include_otc='false'):
        """
        Fetch snapshot data from Polygon.io API.
        
        Args:
            market_type (str): Type of market data to fetch (default: "stocks")
            include_otc (str): Whether to include OTC stocks (default: 'false')

        Returns:
            The snapshot data
        """
        self.snapshot_data = self.client.get_snapshot_all(market_type, include_otc=include_otc)
        return self.snapshot_data
    
    def fetch_daily_aggs(self, date):
        """
        Fetch grouped_daily_aggs data from Polygon.io API.
        
        Args:
            date (str): Date to look up (format: YYYY-MM-DD)

        Returns:
            The object with all open high low close for all tickers
        """
        self.daily_aggs = self.client.get_grouped_daily_aggs(date, include_otc='false')
        return self.daily_aggs

    def fetch_ticker_details(self, ticker):
        """
        Fetch ticker_overview data from Polygon.io API.
        
        Args:
            ticker (str): Ticker symbol to look up
            
        Returns:
            The ticker details
        """
        self.ticker_details = self.client.get_ticker_details(ticker)
        return self.ticker_details
    
    def get_market_cap_for_ticker(self, ticker):
        """
        Get the market cap for a specific ticker.
        
        Args:
            ticker (str): Ticker symbol
            
        Returns:
            float: Market cap of the ticker
        """
        try:
            details = self.fetch_ticker_details(ticker)
        except Exception as e:
            # Optionally log the exception e
            return None
        if not details:
            return None
        if hasattr(details, 'market_cap'):
            return {"market_cap": details.market_cap, "type": details.type}
        else:
            return {"market_cap": None, "type": details.type}

    def filter_tickers_by_market_cap(self, tickers_array, min_market_cap=1e5, max_market_cap=2e9):
        """
        Filter snapshot data by minimum market cap.
        
        Args:
            min_market_cap (float): Minimum market cap to filter by
            max_market_cap (float): Maximum market cap to filter by

        Returns:
            list: List of ticker symbols with market cap above the threshold
        """
        if not self.snapshot_data:
            raise ValueError("No snapshot data available. Call fetch_snapshot() first.")
        
        filtered_tickers = []

        for ticker in tickers_array:
            ticker_market_cap = self.get_market_cap_for_ticker(ticker)
            if ticker_market_cap is None:
                print(f"Ticker {ticker} not found or no market cap data available.")
            else:
                market_cap = self.get_market_cap_for_ticker(ticker)["market_cap"]
                stock_type = self.get_market_cap_for_ticker(ticker)["type"]
            if (stock_type == 'CS' or stock_type == 'ADRC'):
                if market_cap and market_cap >= min_market_cap and market_cap <= max_market_cap:
                    filtered_tickers.append(ticker)
                else: 
                    print(f"Ticker {ticker} filtered out due to market cap: {market_cap}")
            else:
                print(f"Ticker {ticker} filtered out due to type: {stock_type}")

        return filtered_tickers

    def get_premarket_gapped_stocks(self, gap_threshold=0.2, gap_direction="up"):
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

                if ((isinstance(item.last_quote.bid_price, float) or isinstance(item.last_quote.bid_price, int)) and
                    (isinstance(item.prev_day.close, float) or isinstance(item.prev_day.close, int)) and
                    validate_ticker_data(item)):

                    overnight_change = calculate_overnight_change(
                        item.last_quote.bid_price, item.prev_day.close
                    )
                    
                    # Check gap direction
                    if gap_direction == "down" and overnight_change < -gap_threshold:
                        gapped_stocks.append(item.ticker)
                    elif gap_direction == "up" and overnight_change > gap_threshold:
                        gapped_stocks.append(item.ticker)
                    elif gap_direction == "both" and abs(overnight_change) > gap_threshold:
                        gapped_stocks.append(item.ticker)
        
        return gapped_stocks
    
    def get_overnight_gapped_stocks(self, gap_threshold=0.2, gap_direction="up"):
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

                if ((isinstance(item.last_quote.bid_price, float) or isinstance(item.last_quote.bid_price, int)) and
                    (isinstance(item.prev_day.close, float) or isinstance(item.prev_day.close, int)) and
                    validate_ticker_data(item)):

                    overnight_change = calculate_overnight_change(
                        item.day.open, item.prev_day.close
                    )
                    
                    # Check gap direction
                    if gap_direction == "down" and overnight_change < -gap_threshold:
                        gapped_stocks.append(item.ticker)
                    elif gap_direction == "up" and overnight_change > gap_threshold:
                        gapped_stocks.append(item.ticker)
                    elif gap_direction == "both" and abs(overnight_change) > gap_threshold:
                        gapped_stocks.append(item.ticker)
        
        print(gapped_stocks)
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
                            item.last_trade.price, item.prev_day.close
                        )
                    
                    row_data = {
                        'ticker': item.ticker,
                        'prev_open': item.prev_day.open,
                        'prev_close': item.prev_day.close,
                        'prev_high': getattr(item.prev_day, 'high', None),
                        'prev_low': getattr(item.prev_day, 'low', None),
                        'prev_volume': getattr(item.prev_day, 'volume', None),
                        'last_trade_close': getattr(item.last_trade, 'price', None) if hasattr(item, 'last_trade') else None,
                        'overnight_change': overnight_change,
                    }
                    data_rows.append(row_data)
        
        return pd.DataFrame(data_rows)
    
    def analyze_gaps(self, gap_threshold=0.2, gap_direction="up", pre_market="true"):
        """
        Perform complete gap analysis and return both gapped stocks and DataFrame.
        
        Args:
            gap_threshold (float): Minimum gap percentage (as decimal)
            gap_direction (str): Direction of gap - "down", "up", or "both"
            
        Returns:
            dict: Dictionary containing 'gapped_stocks' list
        """
        if not self.snapshot_data:
           self.fetch_snapshot()
        
        if pre_market.lower() == "true":
            gapped_stocks = self.get_premarket_gapped_stocks(gap_threshold, gap_direction)
            #dataframe = self.create_dataframe()
        else:
            gapped_stocks = self.get_overnight_gapped_stocks(gap_threshold, gap_direction)

        return {
            #'dataframe': dataframe,
            #'total_stocks': len(dataframe),
            'gapped_stocks': gapped_stocks,
            'gapped_count': len(gapped_stocks)
        }

    def get_overnight_reference_time_prices(self, tickers, start_date, print_data_to_file=False, verbose=False):
        """
        Get close prices at specific NY times for a given ticker.
        
        Args:
            tickers (list): List of ticker symbols to look up
            reference_times (list): List of (hour, minute) tuples for target times
            
        Returns:
            list: List of matching records with NY time and close price
        """

        # Load historical data for the ticker
        ticker_reference_prices = []
        for ticker in tickers:
            ticker_1m_bars = []
            for bar in self.client.list_aggs(
                ticker,
                1,
                "minute",
                start_date,
                start_date,
                adjusted="true",
                sort="asc",
                limit=5000,
            ):
                ticker_1m_bars.append(bar)
            
            # Convert ticker_1m_bars to a list of dicts for easier handling
            bars_as_dicts = [bar.__dict__ if hasattr(bar, '__dict__') else dict(bar) for bar in ticker_1m_bars]
            one_min_bars_df = pd.DataFrame(bars_as_dicts)
            ticker_reference_prices.append(find_ny_times_in_data(ticker, one_min_bars_df))
            if (print_data_to_file):
                with open(f"{ticker}_quotes_{start_date}.json", "w") as jsonfile:
                    if ticker_1m_bars and hasattr(ticker_1m_bars[0], '__dict__'):
                        json.dump([quote.__dict__ for quote in ticker_1m_bars], jsonfile, indent=2)
                    else:
                        json.dump([str(quote) for quote in ticker_1m_bars], jsonfile, indent=2)

            if (verbose):
                print(one_min_bars_df)
        
        # Find matching records

        return ticker_reference_prices