"""
Utility functions for polygon_stonks library.
"""
import argparse
from datetime import datetime, date, timedelta, timezone
import pytz


def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Analyze stock gaps using Polygon.io API")
    
    # Required arguments
    parser.add_argument(
        "--api-key", 
        type=str, 
        default="oPNvU_u9B3eHFJrSG7ppDrnP4HGmgPqU",
        help="Polygon.io API key"
    )
    
    parser.add_argument(
        "--mac", 
        type=str, 
        action="store_true",
        help="Specify if running on Mac (default is PC)"
    )

    # Optional arguments        
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--print-data-to-file", 
        action="store_true",
        help="Enable printing data to a file"
    )

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
        default=5e5,
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
        "--pre-market", 
        action="store_true",
        help="Enable pre-market analysis"
    )
    
    parser.add_argument(
        "--short-size", 
        type=float, 
        default=1000,
        help="Amount to short. Default: 1000"
    )
    
    parser.add_argument(
        "--autorun",
        action="store_true",
        help="Enable automatic trading. Default: no"
    )
    
    parser.add_argument(
        "--port-value", 
        type=float, 
        default=30000,
        help="Market value of portfolio. Default: 30000"
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
    return (hasattr(item.last_quote, 'bid_price') and 
            item.last_quote.bid_price != 0 and 
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

def timestamp_to_ny_time(timestamp_ms):
    """
    Convert Unix timestamp in milliseconds to New York time.
    
    Args:
        timestamp_ms (int): Unix timestamp in milliseconds
        
    Returns:
        datetime: DateTime object in New York timezone
    """
    # Convert milliseconds to seconds
    timestamp_s = timestamp_ms / 1000
    
    # Create UTC datetime
    utc_dt = datetime.fromtimestamp(timestamp_s, tz=timezone.utc)
    
    # Convert to New York timezone
    ny_tz = pytz.timezone('America/New_York')
    ny_dt = utc_dt.astimezone(ny_tz)
    
    return ny_dt

def is_target_time(ny_datetime, reference_time):
    """
    Check if the NY datetime matches any of our target times.
    
    Args:
        ny_datetime (datetime): DateTime in NY timezone
        reference_time (list): List of reference times as (hour, minute) tuples

    Returns:
        str or None: Description of matched time, or None if no match
    """
    current_time = (ny_datetime.hour, ny_datetime.minute)

    if (abs(current_time[0] - reference_time[0]) == 0 and
        abs(current_time[1] - reference_time[1]) == 0):
        return True
    
    return False

def is_within_hours(ny_datetime, start_time, end_time):
    """
    Check if the NY datetime is within specified hours.
    
    Args:
        ny_datetime (datetime): DateTime in NY timezone

    Returns:
        boolean or None: True if current_time is within specified hours
    """
    current_time = (ny_datetime.hour, ny_datetime.minute)

    # Check if current_time is between the specified hours
    #start_time = (9, 30)
    #end_time = (16, 0)
    if ((current_time[0] > start_time[0] or (current_time[0] == start_time[0] and current_time[1] >= start_time[1])) and
        (current_time[0] < end_time[0] or (current_time[0] == end_time[0] and current_time[1] <= end_time[1]))):
        return True
    
    return False

def find_ny_times_in_data(ticker, bars_data):
    """
    Find close prices at specific NY times in the data.
    
    Args:
        bars_data: DataFrame containing timestamp and close price information
            
    Returns:
        list: List of matching records with NY time and close price
    """    
    results = []
    day_high = 0
    day_low = float('inf')
    high_before_1030 = 0
    high_before_1200 = 0
    first_10_mins_turnover = 0
    total_turnover = 0
    total_volume = 0

    # Add NY timestamp to dataframe by looping through each row
    ny_timestamps = []

    bars_data['turnover'] = bars_data['volume'] * bars_data['vwap']

    last_close_price = 0
    price_at_1030 = 0
    price_at_1200 = 0
    high_time = None
    low_time = None

    for index, row in bars_data.iterrows():
        timestamp = row['timestamp']
        close_price = row['close']
        ny_time = timestamp_to_ny_time(timestamp)
        ny_timestamps.append(ny_time)
        is_trading_hours = is_within_hours(ny_time, (9, 30), (16, 0))
        is_before_1030 = is_within_hours(ny_time, (9, 30), (10, 30))
        is_before_1200 = is_within_hours(ny_time, (9, 30), (12, 0))
        is_first_10_mins = is_within_hours(ny_time, (9, 30), (9, 40))

        if is_trading_hours:
            high_price = row['high']
            if high_price > day_high:
                high_time = ny_time.time()
            day_high = max(day_high, high_price)
            low_price = row['low']
            if low_price < day_low:
                low_time = ny_time.time()
            day_low = min(day_low, low_price)
            total_turnover += row['turnover']
            total_volume += row['volume']
        if is_before_1030:
            high_before_1030 = max(high_before_1030, high_price)
        if is_before_1200:
            high_before_1200 = max(high_before_1200, high_price)
        if is_first_10_mins:
            first_10_mins_turnover += row['turnover']
        if is_before_1030:
            price_at_1030 = close_price
        if is_before_1200:
            price_at_1200 = close_price
            
    results = {
        'date': ny_time.date(),
        'ticker': ticker,
        'vwap': total_turnover / total_volume if total_volume > 0 else 0,
        'total_turnover': total_turnover,
        'first_10_mins_turnover': first_10_mins_turnover,
        'high_before_1030': high_before_1030,
        'high_before_1200': high_before_1200,
        'price_at_1030': price_at_1030,
        'price_at_1200': price_at_1200,
        'high_time': high_time,
        'low_time': low_time
    }

    # Add the new column to the dataframe
    bars_data['ny_timestamp'] = ny_timestamps

    return results

def get_daily_ohlc(bars_data):
    """
    Calculate daily OHLC (Open, High, Low, Close) from intraday bars data.

    Args:
        bars_data (pd.DataFrame): DataFrame containing intraday bars data with columns ['timestamp', 'open', 'high', 'low', 'close']

    Returns:
        dict: Dictionary with daily OHLC values
    """
    if bars_data is None:
        return None

    ticker = bars_data['symbol']
    date = bars_data['from_']
    daily_open = bars_data['open']
    daily_high = bars_data['high']
    daily_low = bars_data['low']
    daily_close = bars_data['close']

    return {
        'date': date,
        'ticker': ticker,
        'open': daily_open,
        'high': daily_high,
        'low': daily_low,
        'close': daily_close
    }

