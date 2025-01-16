from flask import Blueprint, render_template, jsonify
from app.services.edgar_service import EdgarService
from app.services.cik_service import CIKService
from app.services.polygon_service import PolygonService
from app.models.company_facts import CompanyFacts

main = Blueprint('main', __name__)
edgar_service = EdgarService()
cik_service = CIKService()
polygon_service = PolygonService()

@main.route('/')
def dashboard():
    return render_template('dashboard.html')

@main.route('/api/stock/<ticker>')
def get_stock_data(ticker):
    try:
        # Get market data from Polygon
        market_data = polygon_service.get_ticker_details(ticker)
        price_data = polygon_service.get_latest_price(ticker)
        chart_data = polygon_service.get_daily_bars(ticker)
        
        # Get fundamental data from EDGAR
        cik = cik_service.get_cik(ticker)
        if not cik:
            return jsonify({'error': f'No CIK found for ticker {ticker}'}), 404
        
        facts_data = edgar_service.get_company_facts(cik)
        if facts_data:
            financials = edgar_service.get_latest_financials(facts_data)
            company = CompanyFacts(ticker, financials)
            
            # Combine all data
            return jsonify({
                'fundamentals': company.to_dict(),
                'market_data': market_data,
                'price': price_data,
                'chart': chart_data
            })
        else:
            return jsonify({'error': 'Unable to fetch company data'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500 

@main.route('/test/polygon/<ticker>')
def test_polygon(ticker):
    try:
        details = polygon_service.get_ticker_details(ticker)
        price = polygon_service.get_latest_price(ticker)
        bars = polygon_service.get_daily_bars(ticker)
        
        return jsonify({
            'details': details,
            'price': price,
            'bars': bars
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 

@main.route('/analysis')
def analysis_dashboard():
    """Industry/Sector analysis dashboard"""
    sectors = cik_service.get_sectors()
    return render_template('analysis.html', sectors=sectors)

@main.route('/api/analysis/sector/<sector>')
def get_sector_analysis(sector):
    try:
        # Get all companies in sector
        companies = cik_service.get_companies_by_sector(sector)
        results = []
        
        for company in companies[:20]:  # Limit for testing
            ticker = company['ticker']
            cik = company['cik_str']
            
            # Get fundamental data
            facts_data = edgar_service.get_company_facts(cik)
            if facts_data:
                financials = edgar_service.get_latest_financials(facts_data)
                company_facts = CompanyFacts(ticker, financials)
                
                # Get market data
                market_data = polygon_service.get_ticker_details(ticker)
                
                results.append({
                    'ticker': ticker,
                    'name': market_data.get('name') if market_data else '',
                    'sector': sector,
                    'metrics': company_facts.to_dict()
                })
                
        return jsonify({
            'sector': sector,
            'companies': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 