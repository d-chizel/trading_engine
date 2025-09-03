"""
Utility functions for ClearStreet Trading Library.
"""

import re
from typing import Optional
from datetime import datetime


def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Format a monetary amount as currency string.
    
    Args:
        amount (float): The amount to format
        currency (str): Currency code (default: USD)
        
    Returns:
        str: Formatted currency string
    """
    if currency.upper() == "USD":
        return f"${amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"


def validate_symbol(symbol: str) -> bool:
    """
    Validate if a stock symbol is properly formatted.
    
    Args:
        symbol (str): Stock symbol to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not symbol or not isinstance(symbol, str):
        return False
    
    # Basic symbol validation: 1-5 uppercase letters
    pattern = r'^[A-Z]{1,5}$'
    return bool(re.match(pattern, symbol.upper()))


def normalize_symbol(symbol: str) -> str:
    """
    Normalize a stock symbol to standard format.
    
    Args:
        symbol (str): Stock symbol to normalize
        
    Returns:
        str: Normalized symbol (uppercase, stripped)
    """
    if not symbol:
        return ""
    
    return symbol.strip().upper()


def calculate_pnl(cost_basis: float, market_value: float) -> float:
    """
    Calculate profit/loss.
    
    Args:
        cost_basis (float): Original cost
        market_value (float): Current market value
        
    Returns:
        float: Profit/loss amount
    """
    return market_value - cost_basis


def calculate_pnl_percentage(cost_basis: float, market_value: float) -> float:
    """
    Calculate profit/loss percentage.
    
    Args:
        cost_basis (float): Original cost
        market_value (float): Current market value
        
    Returns:
        float: Profit/loss percentage (as decimal, e.g., 0.1 for 10%)
    """
    if cost_basis == 0:
        return 0.0
    
    return (market_value - cost_basis) / cost_basis


def format_timestamp(timestamp: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format a datetime object as string.
    
    Args:
        timestamp (datetime): Datetime to format
        format_str (str): Format string
        
    Returns:
        str: Formatted timestamp
    """
    return timestamp.strftime(format_str)


def is_market_hours(timestamp: Optional[datetime] = None) -> bool:
    """
    Check if given time (or current time) is within market hours.
    Simplified version - assumes NYSE hours (9:30 AM - 4:00 PM ET).
    
    Args:
        timestamp (datetime, optional): Time to check (default: now)
        
    Returns:
        bool: True if within market hours
    """
    if timestamp is None:
        timestamp = datetime.now()
    
    # This is a simplified check - in reality you'd want to handle
    # timezones, holidays, etc.
    weekday = timestamp.weekday()  # 0=Monday, 6=Sunday
    hour = timestamp.hour
    minute = timestamp.minute
    
    # Not a weekday
    if weekday >= 5:  # Saturday or Sunday
        return False
    
    # Convert time to minutes since midnight for easier comparison
    time_minutes = hour * 60 + minute
    market_open = 9 * 60 + 30   # 9:30 AM
    market_close = 16 * 60      # 4:00 PM
    
    return market_open <= time_minutes <= market_close


def validate_quantity(quantity: float) -> bool:
    """
    Validate if a share quantity is valid.
    
    Args:
        quantity (float): Quantity to validate
        
    Returns:
        bool: True if valid quantity
    """
    return isinstance(quantity, (int, float)) and quantity > 0


def validate_price(price: float) -> bool:
    """
    Validate if a price is valid.
    
    Args:
        price (float): Price to validate
        
    Returns:
        bool: True if valid price
    """
    return isinstance(price, (int, float)) and price > 0


def round_to_cents(amount: float) -> float:
    """
    Round amount to nearest cent.
    
    Args:
        amount (float): Amount to round
        
    Returns:
        float: Amount rounded to 2 decimal places
    """
    return round(amount, 2)


def calculate_commission(quantity: float, price: float, commission_rate: float = 0.0) -> float:
    """
    Calculate commission for a trade.
    
    Args:
        quantity (float): Number of shares
        price (float): Price per share
        commission_rate (float): Commission rate (default: 0.0 for commission-free)
        
    Returns:
        float: Commission amount
    """
    trade_value = quantity * price
    return round_to_cents(trade_value * commission_rate)
