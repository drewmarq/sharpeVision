import requests
import time
from typing import Optional, Dict, Any

class EdgarService:
    def __init__(self):
        self.base_url = "https://data.sec.gov/api/xbrl/companyfacts"
        self.headers = {
            'User-Agent': 'SharpeVision/1.0 (douglas.shipp@example.com)',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'data.sec.gov'
        }
        
    def get_company_facts(self, cik: str) -> Optional[Dict[str, Any]]:
        """Fetch company facts from EDGAR API"""
        try:
            # Ensure CIK is properly formatted (10 digits with leading zeros)
            cik = str(cik).zfill(10)
            url = f"{self.base_url}/CIK{cik}.json"
            
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # SEC rate limiting - be nice to their API
            time.sleep(0.1)
            
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching company facts: {e}")
            return None
            
    def get_latest_financials(self, facts_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract the most recent financial metrics from facts data"""
        metrics = {}
        
        try:
            if 'facts' in facts_data:
                us_gaap = facts_data['facts'].get('us-gaap', {})
                
                # Get revenue
                if 'Revenues' in us_gaap:
                    metrics['revenue'] = self._get_latest_value(us_gaap['Revenues'])
                elif 'RevenueFromContractWithCustomerExcludingAssessedTax' in us_gaap:
                    metrics['revenue'] = self._get_latest_value(
                        us_gaap['RevenueFromContractWithCustomerExcludingAssessedTax']
                    )
                
                # Get net income
                if 'NetIncomeLoss' in us_gaap:
                    metrics['net_income'] = self._get_latest_value(us_gaap['NetIncomeLoss'])
                
                # Get total assets
                if 'Assets' in us_gaap:
                    metrics['total_assets'] = self._get_latest_value(us_gaap['Assets'])
                
                # Get total liabilities
                if 'Liabilities' in us_gaap:
                    metrics['total_liabilities'] = self._get_latest_value(us_gaap['Liabilities'])
                
        except Exception as e:
            print(f"Error processing financial data: {e}")
            
        return metrics
    
    def _get_latest_value(self, metric_data: Dict[str, Any]) -> Optional[float]:
        """Helper method to get the most recent value from a metric"""
        try:
            # Filter for annual reports (10-K)
            annual_values = [
                unit for unit in metric_data.get('units', {}).get('USD', [])
                if unit.get('form') == '10-K'
            ]
            
            if annual_values:
                # Sort by end date and get the most recent
                latest = sorted(annual_values, key=lambda x: x['end'])[-1]
                return latest['val']
                
        except Exception as e:
            print(f"Error getting latest value: {e}")
            
        return None 