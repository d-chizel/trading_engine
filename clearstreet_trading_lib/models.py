"""
Data models for ClearStreet Trading API.
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Account:
    """
    Represents a trading account.
    """
    account_id: str
    account_type: str
    status: str
    buying_power: float
    cash_balance: float
    equity: float
    initial_margin: float
    maintenance_margin: float
    currency: str = "USD"
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Account from API response data."""
        return cls(
            account_id=data.get('account_id', ''),
            account_type=data.get('account_type', ''),
            status=data.get('status', ''),
            buying_power=float(data.get('buying_power', 0)),
            cash_balance=float(data.get('cash_balance', 0)),
            equity=float(data.get('equity', 0)),
            initial_margin=float(data.get('initial_margin', 0)),
            maintenance_margin=float(data.get('maintenance_margin', 0)),
            currency=data.get('currency', 'USD')
        )


@dataclass
class Position:
    """
    Represents a stock position.
    """
    symbol: str
    quantity: float
    market_value: float
    cost_basis: float
    unrealized_pnl: float
    average_cost: float
    side: str  # "long" or "short"
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Position from API response data."""
        return cls(
            symbol=data.get('symbol', ''),
            quantity=float(data.get('quantity', 0)),
            market_value=float(data.get('market_value', 0)),
            cost_basis=float(data.get('cost_basis', 0)),
            unrealized_pnl=float(data.get('unrealized_pnl', 0)),
            average_cost=float(data.get('average_cost', 0)),
            side=data.get('side', 'long')
        )


@dataclass
class Order:
    """
    Represents a trading order.
    """
    order_id: str
    symbol: str
    side: str  # "buy" or "sell"
    order_type: str  # "market", "limit", "stop", etc.
    quantity: float
    price: Optional[float]
    stop_price: Optional[float]
    status: str
    filled_quantity: float
    average_fill_price: Optional[float]
    created_at: datetime
    updated_at: datetime
    time_in_force: str = "day"
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Order from API response data."""
        return cls(
            order_id=data.get('order_id', ''),
            symbol=data.get('symbol', ''),
            side=data.get('side', ''),
            order_type=data.get('order_type', ''),
            quantity=float(data.get('quantity', 0)),
            price=float(data['price']) if data.get('price') else None,
            stop_price=float(data['stop_price']) if data.get('stop_price') else None,
            status=data.get('status', ''),
            filled_quantity=float(data.get('filled_quantity', 0)),
            average_fill_price=float(data['average_fill_price']) if data.get('average_fill_price') else None,
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get('updated_at', datetime.now().isoformat())),
            time_in_force=data.get('time_in_force', 'day')
        )


@dataclass
class OrderRequest:
    """
    Represents an order request to be sent to the API.
    """
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float] = None
    stop_price: Optional[float] = None
    time_in_force: str = "day"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API request."""
        data = {
            'symbol': self.symbol,
            'side': self.side,
            'order_type': self.order_type,
            'quantity': self.quantity,
            'time_in_force': self.time_in_force
        }
        
        if self.price is not None:
            data['price'] = self.price
        
        if self.stop_price is not None:
            data['stop_price'] = self.stop_price
        
        return data


@dataclass
class Quote:
    """
    Represents a stock quote.
    """
    symbol: str
    bid_price: float
    ask_price: float
    bid_size: int
    ask_size: int
    last_price: float
    last_size: int
    timestamp: datetime
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Quote from API response data."""
        return cls(
            symbol=data.get('symbol', ''),
            bid_price=float(data.get('bid_price', 0)),
            ask_price=float(data.get('ask_price', 0)),
            bid_size=int(data.get('bid_size', 0)),
            ask_size=int(data.get('ask_size', 0)),
            last_price=float(data.get('last_price', 0)),
            last_size=int(data.get('last_size', 0)),
            timestamp=datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat()))
        )
