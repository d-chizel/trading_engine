"""
Utility functions for polygon_stonks library.
"""
import argparse
from datetime import datetime, date, timedelta

def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Analyze stock gaps using Polygon.io API")
    
    # Required arguments
    parser.add_argument(
        "--api-key", 
        type=str, 
        default="8N6bwNZ7awkAPNHQySbg8eQVI_yM6OTD",
        help="Polygon.io API key"
    )
    
    # Optional arguments
    parser.add_argument(
        "--start-date", 
        type=str, 
        default="2020-01-01",
        help="Start date for historical data (YYYY-MM-DD). Default: 2020-01-01"
    )
    
    parser.add_argument(
        "--end-date", 
        type=str, 
        default="2025-08-01",
        help="End date for historical data (YYYY-MM-DD). Default: 2025-08-01"
    )
    
    parser.add_argument(
        "--gap-threshold", 
        type=float, 
        default=0.2,
        help="Gap threshold as decimal (e.g., 0.2 for 20%%). Default: 0.2"
    )
    
    parser.add_argument(
        "--gap-direction", 
        type=str, 
        choices=["up", "down", "both"], 
        default="up",
        help="Direction of gap to analyze. Default: up"
    )
    
    parser.add_argument(
        "--min-market-cap", 
        type=float, 
        default=1e6,
        help="Minimum market cap filter. Default: 1,000,000"
    )
    
    parser.add_argument(
        "--max-market-cap", 
        type=float, 
        default=2e9,
        help="Maximum market cap filter. Default: 2,000,000,000"
    )
    
    parser.add_argument(
        "--output-csv", 
        type=str, 
        help="Save results to CSV file (optional)"
    )
    
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser.parse_args()

def parse_date(date_string):
    """
    Parse date string to date object.
    Supports formats: YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY
    """
    if not date_string:
        return None
        
    # Try different date formats
    date_formats = [
        "%Y-%m-%d",     # 2024-12-31
        "%d/%m/%Y",     # 31/12/2024
        "%d-%m-%Y",     # 31-12-2024
        "%Y/%m/%d",     # 2024/12/31
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_string, fmt).date()
        except ValueError:
            continue
    
    raise ValueError(f"Unable to parse date: {date_string}. Use format YYYY-MM-DD")

def get_next_weekday(input_date):
    """
    Get the next weekday (Monday-Friday) from the given date.
    If the input date is already a weekday, returns the input date.
    If it's a weekend, returns the next Monday.
    
    Args:
        input_date (date): The input date
        
    Returns:
        date: The next weekday date
    """
    # Monday = 0, Tuesday = 1, ..., Sunday = 6
    weekday = input_date.weekday()
    
    # If it's already a weekday (Monday-Friday), return as is
    if weekday < 5:  # 0-4 are Monday-Friday
        return input_date
    
    # If it's Saturday (5), add 2 days to get to Monday
    if weekday == 5:
        return input_date + timedelta(days=2)
    
    # If it's Sunday (6), add 1 day to get to Monday
    if weekday == 6:
        return input_date + timedelta(days=1)

def is_weekday(input_date):
    """
    Check if the given date is a weekday (Monday-Friday).
    
    Args:
        input_date (date): The date to check
        
    Returns:
        bool: True if it's a weekday, False if it's a weekend
    """
    return input_date.weekday() < 5

def get_weekday_range(start_date, end_date):
    """
    Get all weekdays between start_date and end_date (inclusive).
    
    Args:
        start_date (date): Start date
        end_date (date): End date
        
    Returns:
        list: List of date objects for all weekdays in the range
    """
    weekdays = []
    current_date = start_date
    
    while current_date <= end_date:
        if is_weekday(current_date):
            weekdays.append(current_date)
        current_date += timedelta(days=1)
    
    return weekdays

def calculate_overnight_change(current_price, previous_close):
    """
    Calculate the overnight change percentage between current price and previous close.
    
    Args:
        current_price (float): Current stock price
        previous_close (float): Previous day's closing price
        
    Returns:
        float: Overnight change as a decimal (e.g., -0.2 for -20%)
    """
    if previous_close == 0:
        return 0
    return (current_price / previous_close) - 1


def validate_ticker_data(item):
    """
    Validate that a ticker snapshot item has the required data.
    
    Args:
        item: TickerSnapshot object
        
    Returns:
        bool: True if item has valid data, False otherwise
    """
    return (hasattr(item.min, 'close') and 
            item.min.close != 0 and 
            hasattr(item.prev_day, 'close') and 
            item.prev_day.close != 0)
    
def get_results_outputs(ticker, daily_agg_item, dod_gap):
    """
    Get the results outputs for the analysis.
    
    Returns:
        dict: Dictionary containing the results
    """
    return {
        'ticker': ticker,
        'open': daily_agg_item.open,
        'high': getattr(daily_agg_item, 'high', None),
        'low': getattr(daily_agg_item, 'low', None),
        'close': daily_agg_item.close,
        'volume': getattr(daily_agg_item, 'volume', None),
        'overnight_change': dod_gap
    }
