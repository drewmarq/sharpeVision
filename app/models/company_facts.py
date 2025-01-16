from typing import Dict, Any, Optional

class CompanyFacts:
    def __init__(self, ticker: str, facts_data: Dict[str, Any]):
        self.ticker = ticker
        self.facts_data = facts_data
        self._process_data()
    
    def _process_data(self):
        """Process raw facts data into useful metrics"""
        self.metrics = {
            'revenue': None,
            'net_income': None,
            'total_assets': None,
            'total_liabilities': None
        }
        
        if self.facts_data:
            for key, value in self.facts_data.items():
                self.metrics[key] = value
    
    @property
    def revenue_growth(self) -> Optional[float]:
        """Calculate year-over-year revenue growth"""
        if self.metrics.get('revenue'):
            # Implementation needed for historical comparison
            return None
        return None
    
    @property
    def gross_margin(self) -> Optional[float]:
        """Calculate gross margin"""
        if self.metrics.get('revenue') and self.metrics.get('net_income'):
            return (self.metrics['net_income'] / self.metrics['revenue']) * 100
        return None
    
    @property
    def debt_to_equity(self) -> Optional[float]:
        """Calculate debt to equity ratio"""
        if self.metrics.get('total_liabilities') and self.metrics.get('total_assets'):
            equity = self.metrics['total_assets'] - self.metrics['total_liabilities']
            if equity != 0:
                return self.metrics['total_liabilities'] / equity
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert company facts to dictionary format"""
        return {
            'ticker': self.ticker,
            'metrics': self.metrics,
            'ratios': {
                'revenue_growth': self.revenue_growth,
                'gross_margin': self.gross_margin,
                'debt_to_equity': self.debt_to_equity
            }
        } 