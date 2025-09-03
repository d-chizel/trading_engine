"""
Main client for ClearStreet Trading API.
"""

import requests
from typing import List, Optional, Dict, Any
from .auth import OAuth2Handler
from .models import Account, Position, Order, OrderRequest, Quote


class ClearStreetClient:
    """
    Main client for interacting with ClearStreet Trading API.
    """

    def __init__(self, client_id: str, client_secret: str, base_url: str = "https://api.clearstreet.io"):
        """
        Initialize ClearStreet client.
        
        Args:
            client_id (str): Your ClearStreet client ID
            client_secret (str): Your ClearStreet client secret
            base_url (str): Base URL for ClearStreet API
        """
        self.base_url = base_url
        self.auth = OAuth2Handler(client_id, client_secret, base_url)
    
    def _make_get_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Make authenticated request to API.
        
        Args:
            method (str): HTTP method
            endpoint (str): API endpoint
            **kwargs: Additional arguments for requests
            
        Returns:
            requests.Response: API response
        """
        url = f"{self.base_url}{endpoint}"
        headers = self.auth.get_auth_headers()
        
        # Merge any additional headers
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        kwargs['headers'] = headers
        
        response = requests.get(url, headers)
        response.raise_for_status()
        return response
    
    # Account Methods
    def get_account(self) -> Account:
        """
        Get account information.
        
        Returns:
            Account: Account details
        """
        response = self._make_get_request('get', '/studio/v2/accounts')
        return Account.from_dict(response.json())
    
    def get_account_balance(self) -> Dict[str, float]:
        """
        Get account balance information.
        
        Returns:
            dict: Balance information
        """
        response = self._make_get_request('get', '/v1/account/balance')
        return response.json()
    
    # Position Methods
    def get_positions(self) -> List[Position]:
        """
        Get all positions.
        
        Returns:
            List[Position]: List of current positions
        """
        response = self._make_get_request('get', '/v1/positions')
        positions_data = response.json()
        return [Position.from_dict(pos) for pos in positions_data.get('positions', [])]
    
    def get_position(self, symbol: str) -> Optional[Position]:
        """
        Get position for specific symbol.
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Position or None: Position details if exists
        """
        try:
            response = self._make_get_request('GET', f'/v1/positions/{symbol}')
            return Position.from_dict(response.json())
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise
    
    # Order Methods
    def get_instruments(self, ticker: str):
        """
        Get a list of available trading instruments.
        
        Returns:
            List[str]: List of available trading instruments
        """
        response = self._make_get_request('get', f'/studio/v2/instruments/{ticker}')
        return response.json()
    
    def place_order(self, order_request: OrderRequest) -> Order:
        """
        Place a new order.
        
        Args:
            order_request (OrderRequest): Order details
            
        Returns:
            Order: Created order details
        """
        response = self._make_request(
            'POST', 
            '/v1/orders',
            json=order_request.to_dict()
        )
        return Order.from_dict(response.json())
    
    def get_orders(self, status: Optional[str] = None) -> List[Order]:
        """
        Get orders, optionally filtered by status.
        
        Args:
            status (str, optional): Filter by order status
            
        Returns:
            List[Order]: List of orders
        """
        params = {}
        if status:
            params['status'] = status
        
        response = self._make_get_request('GET', '/v1/orders', params=params)
        orders_data = response.json()
        return [Order.from_dict(order) for order in orders_data.get('orders', [])]
    
    def get_order(self, order_id: str) -> Order:
        """
        Get specific order by ID.
        
        Args:
            order_id (str): Order ID
            
        Returns:
            Order: Order details
        """
        response = self._make_get_request('GET', f'/v1/orders/{order_id}')
        return Order.from_dict(response.json())
    
    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel an order.
        
        Args:
            order_id (str): Order ID to cancel
            
        Returns:
            bool: True if successful
        """
        try:
            self._make_get_request('DELETE', f'/v1/orders/{order_id}')
            return True
        except requests.exceptions.HTTPError:
            return False
    
    # Market Data Methods
    def get_quote(self, symbol: str) -> Quote:
        """
        Get current quote for a symbol.
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            Quote: Current quote data
        """
        response = self._make_get_request('GET', f'/v1/quotes/{symbol}')
        return Quote.from_dict(response.json())
    
    def get_quotes(self, symbols: List[str]) -> List[Quote]:
        """
        Get quotes for multiple symbols.
        
        Args:
            symbols (List[str]): List of stock symbols
            
        Returns:
            List[Quote]: List of quote data
        """
        params = {'symbols': ','.join(symbols)}
        response = self._make_get_request('GET', '/v1/quotes', params=params)
        quotes_data = response.json()
        return [Quote.from_dict(quote) for quote in quotes_data.get('quotes', [])]
    
    # Convenience Methods
    def buy_market(self, symbol: str, quantity: float) -> Order:
        """
        Place a market buy order.
        
        Args:
            symbol (str): Stock symbol
            quantity (float): Number of shares
            
        Returns:
            Order: Created order
        """
        order_request = OrderRequest(
            symbol=symbol,
            side="buy",
            order_type="market",
            quantity=quantity
        )
        return self.place_order(order_request)
    
    def sell_market(self, symbol: str, quantity: float) -> Order:
        """
        Place a market sell order.
        
        Args:
            symbol (str): Stock symbol
            quantity (float): Number of shares
            
        Returns:
            Order: Created order
        """
        order_request = OrderRequest(
            symbol=symbol,
            side="sell",
            order_type="market",
            quantity=quantity
        )
        return self.place_order(order_request)
    
    def buy_limit(self, symbol: str, quantity: float, price: float) -> Order:
        """
        Place a limit buy order.
        
        Args:
            symbol (str): Stock symbol
            quantity (float): Number of shares
            price (float): Limit price
            
        Returns:
            Order: Created order
        """
        order_request = OrderRequest(
            symbol=symbol,
            side="buy",
            order_type="limit",
            quantity=quantity,
            price=price
        )
        return self.place_order(order_request)
    
    def sell_limit(self, symbol: str, quantity: float, price: float) -> Order:
        """
        Place a limit sell order.
        
        Args:
            symbol (str): Stock symbol
            quantity (float): Number of shares
            price (float): Limit price
            
        Returns:
            Order: Created order
        """
        order_request = OrderRequest(
            symbol=symbol,
            side="sell",
            order_type="limit",
            quantity=quantity,
            price=price
        )
        return self.place_order(order_request)
