import json
import os
import requests
import pandas as pd
from typing import Optional, Dict, List
from datetime import datetime

class CIKService:
    def __init__(self):
        self.cik_map = {}
        self.bulk_data_url = "https://www.sec.gov/files/company_tickers.json"
        self.headers = {
            'User-Agent': 'SharpeVision/1.0',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'www.sec.gov'
        }
        self._load_cik_map()
    
    def _load_cik_map(self):
        """Load CIK map from SEC's company tickers file"""
        try:
            response = requests.get(
                self.bulk_data_url, 
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            # Convert SEC's data into a DataFrame
            data = response.json()
            df = pd.DataFrame.from_dict(data, orient='index')
            
            # Clean and format CIKs
            df['cik_str'] = df['cik_str'].astype(str).str.zfill(10)
            
            # Store as both DataFrame and map
            self.cik_df = df
            self.cik_map = dict(zip(df['ticker'], df['cik_str']))
            
            # Save to CSV for record
            timestamp = datetime.now().strftime('%Y%m%d')
            os.makedirs('app/data', exist_ok=True)  # Updated path
            df.to_csv(f'app/data/cik_data_{timestamp}.csv', index=False)
            
        except Exception as e:
            print(f"Error loading CIK map: {e}")
            # Try to load from cached file if available
            self._load_from_cache()
    
    def _load_from_cache(self):
        """Load CIK data from most recent cached file"""
        try:
            if not os.path.exists('app/data'):  # Updated path
                return
                
            files = [f for f in os.listdir('app/data') if f.startswith('cik_data_')]  # Updated path
            if not files:
                return
                
            latest_file = max(files)
            df = pd.read_csv(f'app/data/{latest_file}')  # Updated path
            self.cik_df = df
            self.cik_map = dict(zip(df['ticker'], df['cik_str']))
            print(f"Loaded CIK data from cache: {latest_file}")
        except Exception as e:
            print(f"Error loading from cache: {e}")
    
    def get_cik(self, ticker: str) -> Optional[str]:
        """Get CIK for a given ticker"""
        return self.cik_map.get(ticker.upper())
    
    def get_all_active_tickers(self) -> List[Dict]:
        """Get all active tickers with their CIKs"""
        return self.cik_df.to_dict('records')
    
    def refresh_data(self):
        """Manually refresh the CIK data"""
        self._load_cik_map() 
    
    def get_companies_by_sector(self, sector: str) -> List[Dict]:
        """Get all companies in a given sector"""
        try:
            # Filter companies by sector
            sector_companies = self.cik_df[
                self.cik_df['title'].str.contains(sector, case=False, na=False)
            ]
            return sector_companies.to_dict('records')
        except Exception as e:
            print(f"Error getting companies by sector: {e}")
            return []
    
    def get_sectors(self) -> List[str]:
        """Get list of all available sectors"""
        try:
            # Extract unique sectors from company titles
            # This is a simple approach; might need refinement
            sectors = set()
            for title in self.cik_df['title']:
                # Common sector keywords
                for sector in ['Technology', 'Healthcare', 'Financial', 'Energy', 'Consumer']:
                    if sector.lower() in title.lower():
                        sectors.add(sector)
            return sorted(list(sectors))
        except Exception as e:
            print(f"Error getting sectors: {e}")
            return [] 