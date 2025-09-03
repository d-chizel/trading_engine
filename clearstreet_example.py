"""
Example usage of ClearStreet Trading Library.
"""

from clearstreet_trading_lib import ClearStreetClient
from clearstreet_trading_lib.utils import format_currency, normalize_symbol, validate_symbol


def main():
    """
    Example usage of ClearStreet Trading API.
    """
    # Initialize client with your credentials
    client = ClearStreetClient(
        client_id="peHRscbk4tio7g4fPpe1XK8cOAlXqTvL",
        client_secret="bGeu70ZimnTdw7oXUcDfXeAKibQwpKHcpaLLi_5RTaijW2iTOMpTHo6Ul2Tr5Dvm"
    )
    
    try:
        # Get Instrument
        print("=== Instrument ===")
        instrument = client.get_instruments('AAPL')
        
        '''
        # Get account information
        print("=== Account Information ===")
        account = client.get_account()
        print(f"Account ID: {account.account_id}")
        print(f"Account Type: {account.account_type}")
        print(f"Status: {account.status}")
        print(f"Buying Power: {format_currency(account.buying_power)}")
        print(f"Cash Balance: {format_currency(account.cash_balance)}")
        print(f"Equity: {format_currency(account.equity)}")
        
        # Get positions
        print("\n=== Current Positions ===")
        positions = client.get_positions()
        
        if positions:
            for position in positions:
                print(f"Symbol: {position.symbol}")
                print(f"Quantity: {position.quantity}")
                print(f"Market Value: {format_currency(position.market_value)}")
                print(f"Unrealized P&L: {format_currency(position.unrealized_pnl)}")
                print(f"Side: {position.side}")
                print("-" * 30)
        else:
            print("No positions found")
        
        # Get quotes
        print("\n=== Market Quotes ===")
        symbols = ["AAPL", "GOOGL", "MSFT"]
        quotes = client.get_quotes(symbols)
        
        for quote in quotes:
            print(f"{quote.symbol}: ${quote.last_price:.2f} "
                  f"(Bid: ${quote.bid_price:.2f}, Ask: ${quote.ask_price:.2f})")
        
        # Get orders
        print("\n=== Recent Orders ===")
        orders = client.get_orders()
        
        if orders:
            for order in orders[-5:]:  # Show last 5 orders
                print(f"Order ID: {order.order_id}")
                print(f"Symbol: {order.symbol}")
                print(f"Side: {order.side}")
                print(f"Type: {order.order_type}")
                print(f"Quantity: {order.quantity}")
                print(f"Status: {order.status}")
                print(f"Created: {order.created_at}")
                print("-" * 30)
        else:
            print("No orders found")
        
        # Example: Place a limit buy order (commented out for safety)
        """
        print("\n=== Placing Order ===")
        order_request = OrderRequest(
            symbol="AAPL",
            side="buy",
            order_type="limit",
            quantity=10,
            price=150.00
        )
        
        new_order = client.place_order(order_request)
        print(f"Order placed: {new_order.order_id}")
        """
        
        # Example: Using convenience methods (commented out for safety)
        """
        # Market buy
        order = client.buy_market("AAPL", 10)
        
        # Limit sell
        order = client.sell_limit("AAPL", 10, 155.00)
        
        # Cancel order
        success = client.cancel_order(order.order_id)
        """
        '''
        
    except Exception as e:
        print(f"Error: {e}")


def test_utils():
    """
    Test utility functions.
    """
    print("\n=== Testing Utility Functions ===")
    
    # Test currency formatting
    print(f"Currency formatting: {format_currency(1234.56)}")
    print(f"Currency formatting (EUR): {format_currency(1234.56, 'EUR')}")
    
    # Test symbol validation
    symbols_to_test = ["AAPL", "aapl", "INVALID123", ""]
    for symbol in symbols_to_test:
        normalized = normalize_symbol(symbol)
        is_valid = validate_symbol(normalized) if normalized else False
        print(f"Symbol '{symbol}' -> '{normalized}' (Valid: {is_valid})")


if __name__ == "__main__":
    print("ClearStreet Trading Library Example")
    print("=" * 50)
    
    # Test utility functions first
    main()
    
    # Main API example (uncomment when you have real credentials)
    # main()
