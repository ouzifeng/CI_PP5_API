from django.core.management.base import BaseCommand
from stockdata.models import General, Description, Highlights, Valuation, Technicals, SplitsDividends, AnalystRatings, BalanceSheet, CashFlow, IncomeStatement
from django.utils.dateparse import parse_date
import requests
from datetime import datetime

class Command(BaseCommand):
    help = 'Imports stock data from the EOD Historical Data API'

    def handle(self, *args, **kwargs):
        api_token = '649401f5eeff73.67939383'
        stocks = General.objects.filter(uid__endswith='.LSE')

        print(f"Total stocks found: {stocks.count()}")

        for i, stock in enumerate(stocks, start=1):
            print(f"Processing stock {i}/{stocks.count()}: {stock.uid}")
            url = f'https://eodhd.com/api/fundamentals/{stock.uid}?api_token={api_token}&fmt=json'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.update_stock(stock, data)
            else:
                print(f"Failed to fetch data for {stock.uid}. Status code: {response.status_code}")

    def update_stock(self, stock, data):
        # Assuming 'General' information is directly under the root of 'data'
        # Adjust the paths according to the actual structure of your API response
        general_info = data.get('General', {})
        
        # Update the General model
        # Here 'stock' is an instance of the General model already, so we directly update its fields
        General.objects.filter(uid=stock.uid).update(
            code=general_info.get('Code', stock.code),  # Default to existing values if not found
            type=general_info.get('Type', stock.type),
            name=general_info.get('Name', stock.name),
            primary_ticker=general_info.get('PrimaryTicker', stock.primary_ticker),
            exchange=general_info.get('Exchange', stock.exchange),
            currency_code=general_info.get('CurrencyCode', stock.currency_code),
            currency_name=general_info.get('CurrencyName', stock.currency_name),
            currency_symbol=general_info.get('CurrencySymbol', stock.currency_symbol),
            country_name=general_info.get('CountryName', stock.country_name),
            country_iso=general_info.get('CountryISO', stock.country_iso),
            isin=general_info.get('ISIN', stock.isin),
            fiscal_year_end=general_info.get('FiscalYearEnd', stock.fiscal_year_end),
            sector=general_info.get('Sector', stock.sector),
            industry=general_info.get('Industry', stock.industry),
            address=general_info.get('Address', stock.address),
            phone=general_info.get('Phone', stock.phone),
            web_url=general_info.get('WebURL', stock.web_url),
            full_time_employees=general_info.get('FullTimeEmployees', stock.full_time_employees),
            updated_at=parse_date(general_info.get('UpdatedAt')) if general_info.get('UpdatedAt') else stock.updated_at,
            
        )

        # Update the Description model related to this General instance
        description_text = general_info.get('Description', None)
        if description_text is not None:
            Description.objects.update_or_create(
                general=stock,  # Direct reference to the General instance
                defaults={'text': description_text}
            )
            
            
        highlights_data = data.get('Highlights', {})
        if highlights_data:
            Highlights.objects.update_or_create(
                general=stock,  # Direct reference to the General instance
                defaults={
                'market_capitalization': highlights_data.get('MarketCapitalization'),
                'ebitda': highlights_data.get('EBITDA'),
                'pe_ratio': highlights_data.get('PERatio'),
                'peg_ratio': highlights_data.get('PEGRatio'),
                'wall_street_target_price': highlights_data.get('WallStreetTargetPrice'),
                'book_value': highlights_data.get('BookValue'),
                'dividend_share': highlights_data.get('DividendShare'),
                'dividend_yield': highlights_data.get('DividendYield'),
                'earnings_share': highlights_data.get('EarningsShare'),
                'eps_estimate_current_year': highlights_data.get('EPSEstimateCurrentYear'),
                'eps_estimate_next_year': highlights_data.get('EPSEstimateNextYear'),
                'eps_estimate_next_quarter': highlights_data.get('EPSEstimateNextQuarter'),
                'eps_estimate_current_quarter': highlights_data.get('EPSEstimateCurrentQuarter'),
                'most_recent_quarter': datetime.strptime(highlights_data.get('MostRecentQuarter'), '%Y-%m-%d').date() if highlights_data.get('MostRecentQuarter') else None,
                'profit_margin': highlights_data.get('ProfitMargin'),
                'operating_margin_ttm': highlights_data.get('OperatingMarginTTM'),
                'return_on_assets_ttm': highlights_data.get('ReturnOnAssetsTTM'),
                'return_on_equity_ttm': highlights_data.get('ReturnOnEquityTTM'),
                'revenue_ttm': highlights_data.get('RevenueTTM'),
                'revenue_per_share_ttm': highlights_data.get('RevenuePerShareTTM'),
                'quarterly_revenue_growth_yoy': highlights_data.get('QuarterlyRevenueGrowthYOY'),
                'gross_profit_ttm': highlights_data.get('GrossProfitTTM'),
                'diluted_eps_ttm': highlights_data.get('DilutedEpsTTM'),
                'quarterly_earnings_growth_yoy': highlights_data.get('QuarterlyEarningsGrowthYOY'),
            }
        )            

        print(f"Updated all data for {stock.uid}")