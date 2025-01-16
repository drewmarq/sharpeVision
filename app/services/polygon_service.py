import os
from typing import Dict, Any, Optional
import requests
from datetime import datetime, timedelta

class PolygonService:
    def __init__(self):
        api_key = os.getenv('POLYGON_API_KEY')
        if not api_key:
            raise ValueError("POLYGON_API_KEY environment variable is not set")
            
        self.base_url = "https://api.polygon.io/v3"
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/json'
        }
    
    def get_ticker_details(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get basic ticker information"""
        try:
            response = requests.get(
                f"{self.base_url}/reference/tickers/{symbol}",
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()['results']
            
            return {
                'name': data.get('name'),
                'market': data.get('market'),
                'sector': data.get('sic_description'),  # Using SIC description for sector
                'industry': data.get('industry'),
                'market_cap': data.get('market_cap')
            }
        except Exception as e:
            print(f"Error fetching ticker details: {e}")
            return None
    
    def get_latest_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get latest trading data"""
        try:
            response = requests.get(
                f"{self.base_url}/last/trade/{symbol}",
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()['results']
            
            return {
                'price': data.get('p'),  # price
                'size': data.get('s'),   # size
                'timestamp': data.get('t') # timestamp
            }
        except Exception as e:
            print(f"Error fetching latest price: {e}")
            return None
    
    def get_daily_bars(self, symbol: str, days: int = 30) -> Optional[Dict[str, Any]]:
        """Get daily OHLCV data"""
        try:
            end = datetime.now()
            start = end - timedelta(days=days)
            
            response = requests.get(
                f"{self.base_url}/aggs/ticker/{symbol}/range/1/day/{start.strftime('%Y-%m-%d')}/{end.strftime('%Y-%m-%d')}",
                headers=self.headers
            )
            response.raise_for_status()
            bars = response.json()['results']
            
            return {
                'dates': [bar['t'] for bar in bars],
                'open': [bar['o'] for bar in bars],
                'high': [bar['h'] for bar in bars],
                'low': [bar['l'] for bar in bars],
                'close': [bar['c'] for bar in bars],
                'volume': [bar['v'] for bar in bars]
            }
        except Exception as e:
            print(f"Error fetching daily bars: {e}")
            return None 