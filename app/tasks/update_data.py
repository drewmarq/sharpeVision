from app.services.cik_service import CIKService
from app.services.edgar_service import EdgarService
from app.services.data_storage import DataStorage
import time
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_company_data():
    """Update company data from SEC"""
    cik_service = CIKService()
    edgar_service = EdgarService()
    storage = DataStorage()
    
    # Get all active tickers
    active_companies = cik_service.get_all_active_tickers()
    
    for company in active_companies:
        try:
            # Fetch and store company facts
            facts = edgar_service.get_company_facts(company['cik_str'])
            if facts:
                storage.save_company_facts(company['cik_str'], facts)
                
                # Process financial statements
                financials = storage.process_financial_statements(facts)
                
                # Calculate metrics
                metrics = storage.calculate_metrics(financials)
                
                logger.info(f"Processed {company['ticker']}")
                
            # Be nice to SEC's API
            time.sleep(0.1)
            
        except Exception as e:
            logger.error(f"Error processing {company['ticker']}: {e}")

if __name__ == "__main__":
    logger.info(f"Starting data update at {datetime.now()}")
    update_company_data()
    logger.info(f"Completed data update at {datetime.now()}") 