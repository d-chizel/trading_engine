# ClearStreet Trading Library

A Python library for interacting with the ClearStreet Trading API, featuring OAuth2 authentication, account management, order placement, and market data retrieval.

## Features

- **OAuth2 Authentication**: Secure client credentials flow
- **Account Management**: Get account details, balances, and positions
- **Order Management**: Place, cancel, and track orders
- **Market Data**: Get real-time quotes and market information
- **Type Safety**: Full type hints and data models
- **Error Handling**: Comprehensive error handling and validation

## Installation

```bash
# From source
git clone <your-repo>
cd polygon_stonks
pip install -e ./clearstreet_trading_lib
```

## Quick Start

```python
from clearstreet_trading_lib import ClearStreetClient, OrderRequest

# Initialize client
client = ClearStreetClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Get account information
account = client.get_account()
print(f"Buying Power: ${account.buying_power:.2f}")

# Get positions
positions = client.get_positions()
for position in positions:
    print(f"{position.symbol}: {position.quantity} shares")

# Get market quotes
quotes = client.get_quotes(["AAPL", "GOOGL", "MSFT"])
for quote in quotes:
    print(f"{quote.symbol}: ${quote.last_price:.2f}")

# Place orders
# Market buy
order = client.buy_market("AAPL", 10)

# Limit sell
order = client.sell_limit("AAPL", 10, 155.00)

# Custom order
order_request = OrderRequest(
    symbol="AAPL",
    side="buy",
    order_type="limit",
    quantity=10,
    price=150.00
)
order = client.place_order(order_request)
```

## API Reference

### ClearStreetClient

Main client class for API interactions.

#### Authentication
- Automatically handles OAuth2 token management
- Refreshes tokens when expired
- Includes proper error handling

#### Account Methods
- `get_account()` - Get account details
- `get_account_balance()` - Get balance information

#### Position Methods
- `get_positions()` - Get all positions
- `get_position(symbol)` - Get position for specific symbol

#### Order Methods
- `place_order(order_request)` - Place a new order
- `get_orders(status=None)` - Get orders (optionally filtered by status)
- `get_order(order_id)` - Get specific order
- `cancel_order(order_id)` - Cancel an order

#### Convenience Methods
- `buy_market(symbol, quantity)` - Market buy order
- `sell_market(symbol, quantity)` - Market sell order
- `buy_limit(symbol, quantity, price)` - Limit buy order
- `sell_limit(symbol, quantity, price)` - Limit sell order

#### Market Data Methods
- `get_quote(symbol)` - Get quote for single symbol
- `get_quotes(symbols)` - Get quotes for multiple symbols

### Data Models

#### Account
```python
@dataclass
class Account:
    account_id: str
    account_type: str
    status: str
    buying_power: float
    cash_balance: float
    equity: float
    initial_margin: float
    maintenance_margin: float
    currency: str = "USD"
```

#### Position
```python
@dataclass
class Position:
    symbol: str
    quantity: float
    market_value: float
    cost_basis: float
    unrealized_pnl: float
    average_cost: float
    side: str  # "long" or "short"
```

#### Order
```python
@dataclass
class Order:
    order_id: str
    symbol: str
    side: str  # "buy" or "sell"
    order_type: str  # "market", "limit", "stop"
    quantity: float
    price: Optional[float]
    stop_price: Optional[float]
    status: str
    filled_quantity: float
    average_fill_price: Optional[float]
    created_at: datetime
    updated_at: datetime
    time_in_force: str = "day"
```

#### OrderRequest
```python
@dataclass
class OrderRequest:
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float] = None
    stop_price: Optional[float] = None
    time_in_force: str = "day"
```

### Utility Functions

```python
from clearstreet_trading_lib.utils import (
    format_currency,
    validate_symbol,
    normalize_symbol,
    calculate_pnl,
    is_market_hours
)

# Format currency
formatted = format_currency(1234.56)  # "$1,234.56"

# Validate symbols
is_valid = validate_symbol("AAPL")  # True
normalized = normalize_symbol("aapl")  # "AAPL"

# Calculate P&L
pnl = calculate_pnl(1000, 1100)  # 100.0
pnl_pct = calculate_pnl_percentage(1000, 1100)  # 0.1 (10%)

# Check market hours
is_open = is_market_hours()  # True/False
```

## Error Handling

The library includes comprehensive error handling:

```python
try:
    account = client.get_account()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Configuration

### Environment Variables
You can set credentials as environment variables:

```bash
export CLEARSTREET_CLIENT_ID="your_client_id"
export CLEARSTREET_CLIENT_SECRET="your_client_secret"
```

### Custom Base URL
```python
client = ClearStreetClient(
    client_id="your_id",
    client_secret="your_secret",
    base_url="https://sandbox-api.clearstreet.com"  # For sandbox
)
```

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Formatting
```bash
black clearstreet_trading_lib/
flake8 clearstreet_trading_lib/
```

## Requirements

- Python 3.8+
- requests >= 2.31.0
- python-dateutil >= 2.8.0

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For issues and questions, please open an issue on the GitHub repository.

## Disclaimer

This library is for educational and development purposes. Always test thoroughly in a sandbox environment before using with real trading accounts. Trading involves financial risk.
