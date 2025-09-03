"""
Simple tests for ClearStreet Trading Library.
"""

from clearstreet_trading_lib import ClearStreetClient, OrderRequest, Account, Position
from clearstreet_trading_lib.utils import format_currency, validate_symbol, normalize_symbol


def test_models():
    """Test data models."""
    print("Testing data models...")
    
    # Test Account model
    account_data = {
        'account_id': 'ACC123',
        'account_type': 'MARGIN',
        'status': 'ACTIVE',
        'buying_power': 10000.00,
        'cash_balance': 5000.00,
        'equity': 15000.00,
        'initial_margin': 2000.00,
        'maintenance_margin': 1000.00
    }
    
    account = Account.from_dict(account_data)
    print(f"✓ Account created: {account.account_id}, Buying Power: {format_currency(account.buying_power)}")
    
    # Test OrderRequest
    order_request = OrderRequest(
        symbol="AAPL",
        side="buy",
        order_type="limit",
        quantity=100,
        price=150.00
    )
    
    order_dict = order_request.to_dict()
    print(f"✓ OrderRequest created: {order_dict}")


def test_utils():
    """Test utility functions."""
    print("\nTesting utility functions...")
    
    # Test currency formatting
    assert format_currency(1234.56) == "$1,234.56"
    print("✓ Currency formatting works")
    
    # Test symbol validation
    assert validate_symbol("AAPL") == True
    assert validate_symbol("INVALID123") == False
    print("✓ Symbol validation works")
    
    # Test symbol normalization
    assert normalize_symbol("aapl") == "AAPL"
    assert normalize_symbol(" msft ") == "MSFT"
    print("✓ Symbol normalization works")


def test_oauth_handler():
    """Test OAuth handler (without making actual requests)."""
    print("\nTesting OAuth handler...")
    
    from clearstreet_trading_lib.auth import OAuth2Handler
    
    oauth = OAuth2Handler("test_id", "test_secret")
    
    # Test token validation
    assert oauth.is_token_valid() == False  # No token set
    print("✓ OAuth handler created and token validation works")


if __name__ == "__main__":
    print("ClearStreet Trading Library Tests")
    print("=" * 50)
    
    try:
        test_models()
        test_utils()
        test_oauth_handler()
        
        print("\n🎉 All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise
