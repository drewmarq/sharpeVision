import pandas as pd
from datetime import datetime
from typing import Dict, Any, List
import os
import json

class DataStorage:
    def __init__(self):
        self.base_path = 'data'
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        directories = ['raw', 'processed', 'metrics']
        for dir_name in directories:
            path = f"{self.base_path}/{dir_name}"
            os.makedirs(path, exist_ok=True)
    
    def save_company_facts(self, cik: str, facts_data: Dict[str, Any]):
        """Save raw company facts data"""
        timestamp = datetime.now().strftime('%Y%m%d')
        filename = f"{self.base_path}/raw/facts_{cik}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(facts_data, f)
    
    def process_financial_statements(self, facts_data: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
        """Process raw facts into financial statements"""
        statements = {
            'income_statement': [],
            'balance_sheet': [],
            'cash_flow': []
        }
        
        # Implementation for processing statements
        # This will need to be expanded based on the specific metrics needed
        
        return {k: pd.DataFrame(v) for k, v in statements.items()}
    
    def calculate_metrics(self, financials: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Calculate financial metrics and ratios"""
        metrics = []
        # Implementation for calculating various metrics
        return pd.DataFrame(metrics) 