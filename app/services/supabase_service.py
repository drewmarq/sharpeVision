from supabase import create_client
import os
from typing import Dict, Any, List
from datetime import datetime

class SupabaseService:
    def __init__(self):
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        if not url or not key:
            raise ValueError("Supabase credentials not set")
        self.client = create_client(url, key)
    
    async def upsert_company_data(self, ticker: str, data: Dict[str, Any]):
        """Store or update company data"""
        return await self.client.table('companies').upsert({
            'ticker': ticker,
            'cik': data['cik'],
            'name': data.get('name'),
            'sector': data.get('sector'),
            'last_updated': datetime.utcnow().isoformat(),
            'metrics': data.get('metrics'),
            'market_data': data.get('market_data')
        }).execute()
    
    async def get_company_data(self, ticker: str):
        """Get company data from cache"""
        return await self.client.table('companies')\
            .select('*')\
            .eq('ticker', ticker)\
            .single()\
            .execute() 