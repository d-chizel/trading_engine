"""
Authentication module for ClearStreet Trading API using OAuth2.
"""

import requests
import base64
from datetime import datetime, timedelta
import json


class OAuth2Handler:
    """
    Handle OAuth2 authentication for ClearStreet Trading API.
    """
    
    def __init__(self, client_id, client_secret, base_url="https://api.clearstreet.io"):
        """
        Initialize OAuth2 handler.
        
        Args:
            client_id (str): Your ClearStreet client ID
            client_secret (str): Your ClearStreet client secret
            base_url (str): Base URL for ClearStreet API
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.token_url = "https://auth.clearstreet.io/oauth/token"
        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = None
    
    def get_access_token(self, scope="trading:read trading:write"):
        """
        Get access token using client credentials flow.
        
        Args:
            scope (str): Requested permissions scope
            
        Returns:
            str: Access token if successful, None otherwise
        """
        # Prepare Basic Auth header        
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        
        payload = {
            'grant_type': 'client_credentials',
            "audience": "https://api.clearstreet.io",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        try:
            response = requests.post(
                self.token_url,
                json=payload,
                headers=headers
            )
            
            response.raise_for_status()
            token_data = response.json()
            
            self.access_token = token_data.get('access_token')
            self.refresh_token = token_data.get('refresh_token')
            
            # Calculate expiration time
            expires_in = token_data.get('expires_in', 86400)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
            
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            print(f"Error obtaining access token: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text}")
            return None
    
    def is_token_valid(self):
        """
        Check if current token is still valid.
        
        Returns:
            bool: True if token is valid, False otherwise
        """
        if not self.access_token or not self.token_expires_at:
            return False
        
        # Add 5 minute buffer
        return datetime.now() < (self.token_expires_at - timedelta(minutes=5))
    
    def get_valid_token(self):
        """
        Get a valid access token, refreshing if necessary.
        
        Returns:
            str: Valid access token
        """
        if not self.is_token_valid():
            return self.get_access_token()

        return self.access_token
    
    def get_auth_headers(self):
        """
        Get headers with valid authorization token.
        
        Returns:
            dict: Headers with Authorization bearer token
        """
        token = self.get_valid_token()

        if not token:
            raise Exception("Unable to obtain valid access token")
        
        return {
            'authorization': f'Bearer {token}',
            'accept': 'application/json'
        }
