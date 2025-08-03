"""
Utility functions for polygon_stonks library.
"""

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
