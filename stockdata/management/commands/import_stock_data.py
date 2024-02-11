from django.core.management.base import BaseCommand
from stockdata.models import General, Description, Highlights, Valuation, Technicals, SplitsDividends, AnalystRatings, BalanceSheet, CashFlow, IncomeStatement
from django.utils.dateparse import parse_date
import requests
from datetime import datetime, timedelta
from django.utils.timezone import make_aware, now
import os

def parse_date(date_string):
    try:
        return datetime.strptime(date_string, '%Y-%m-%d').date() if date_string and date_string != '0000-00-00' else None
    except ValueError:
        return None
    
def import_tickers(api_token, exchange='LSE'):
    ticker_url = f'https://eodhd.com/api/exchange-symbol-list/{exchange}?api_token={api_token}&fmt=json'
    response = requests.get(ticker_url)

    if response.status_code == 200:
        ticker_data = response.json()

        for entry in ticker_data:
            uid = f"{entry['Code']}.{exchange}"

            if len(uid) > 10:
                print(f"Skipping ticker {uid} because it's longer than 10 characters.")
                continue

            General.objects.update_or_create(
                uid=uid,
                defaults={
                    'code': entry['Code'],
                }
            )
        print(f'Successfully imported tickers for {exchange}.')
    else:
        print(f'Failed to download ticker list for {exchange}. Status code: {response.status_code}')    

class Command(BaseCommand):
    help = 'Imports stock data from the EOD Historical Data API'

    def handle(self, *args, **kwargs):
        api_token = config('API_TOKEN')
        # import_tickers(api_token)
        stocks = General.objects.filter(uid__endswith='.LSE')

        print(f"Total stocks found: {stocks.count()}")

        start_index = 793 - 1
        for index, stock in enumerate(stocks[start_index:], start=start_index):
            print(f"Processing stock {index + 1}/{stocks.count()}: {stock.uid}")
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
                'most_recent_quarter': parse_date(highlights_data.get('MostRecentQuarter')),
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
            
        valuation_data = data.get('Valuation', {})
        if valuation_data:
            Valuation.objects.update_or_create(
                general=stock,
                defaults={
                    'trailing_pe': valuation_data.get('TrailingPE'),
                    'forward_pe': valuation_data.get('ForwardPE'),
                    'price_sales_ttm': valuation_data.get('PriceSalesTTM'),
                    'price_book_mrq': valuation_data.get('PriceBookMRQ'),
                    'enterprise_value': valuation_data.get('EnterpriseValue'),
                    'enterprise_value_revenue': valuation_data.get('EnterpriseValueRevenue'),
                    'enterprise_value_ebitda': valuation_data.get('EnterpriseValueEbitda'),
                }
        )
        
        technicals_data = data.get('Technicals', {})
        if technicals_data:
            Technicals.objects.update_or_create(
                general=stock,
                defaults={
                    'beta': technicals_data.get('Beta'),
                    'fifty_two_week_high': technicals_data.get('52WeekHigh'),
                    'fifty_two_week_low': technicals_data.get('52WeekLow'),
                    'fifty_day_ma': technicals_data.get('50DayMA'),
                    'two_hundred_day_ma': technicals_data.get('200DayMA'),
                    'shares_short': technicals_data.get('SharesShort'),
                    'shares_short_prior_month': technicals_data.get('SharesShortPriorMonth'),
                    'short_ratio': technicals_data.get('ShortRatio'),
                    'short_percent': technicals_data.get('ShortPercent'),
                }
            )

        splits_dividends_data = data.get('SplitsDividends', {})
        if splits_dividends_data:
            SplitsDividends.objects.update_or_create(
                general=stock,
                defaults={
                    'forward_annual_dividend_rate': splits_dividends_data.get('ForwardAnnualDividendRate'),
                    'forward_annual_dividend_yield': splits_dividends_data.get('ForwardAnnualDividendYield'),
                    'payout_ratio': splits_dividends_data.get('PayoutRatio'),
                    'dividend_date': parse_date(splits_dividends_data.get('DividendDate')),
                    'ex_dividend_date': parse_date(splits_dividends_data.get('ExDividendDate')),
                    'last_split_factor': splits_dividends_data.get('LastSplitFactor'),
                    'last_split_date': parse_date(splits_dividends_data.get('LastSplitDate')),
                }
            )


        analyst_ratings_data = data.get('AnalystRatings', {})
        if analyst_ratings_data:
            AnalystRatings.objects.update_or_create(
                general=stock,
                defaults={
                    'rating': analyst_ratings_data.get('Rating'),
                    'target_price': analyst_ratings_data.get('TargetPrice'),
                    'strong_buy': analyst_ratings_data.get('StrongBuy'),
                    'buy': analyst_ratings_data.get('Buy'),
                    'hold': analyst_ratings_data.get('Hold'),
                    'sell': analyst_ratings_data.get('Sell'),
                    'strong_sell': analyst_ratings_data.get('StrongSell'),
                }
            )             

       # Process Balance Sheet data
        for sheet_type in ['yearly', 'quarterly']:
            balance_sheet_data = data.get('Financials', {}).get('Balance_Sheet', {}).get(sheet_type, {})
            for key, sheet_data in balance_sheet_data.items():
                try:
                    date_obj = datetime.strptime(key, '%Y-%m-%d').date()
                    datetime_obj = make_aware(datetime.combine(date_obj, datetime.min.time()))
                except ValueError:
                    self.stdout.write(self.style.ERROR(f"Invalid date format for {key} in {sheet_type} data."))
                    continue

                if date_obj.year < now().year - 5:
                    continue

                try:
                    balance_sheet, created = BalanceSheet.objects.update_or_create(
                        general=stock,
                        date=datetime_obj,
                        type=sheet_type,
                        defaults={
                            'filing_date': parse_date(sheet_data.get('filing_date')),
                            'currency_symbol': sheet_data.get('currency_symbol', ''),
                            'total_assets': float(sheet_data.get('totalAssets')) if sheet_data.get('totalAssets') else None,
                            'intangible_assets': float(sheet_data.get('intangibleAssets')) if sheet_data.get('intangibleAssets') else None,
                            'earning_assets': float(sheet_data.get('earningAssets')) if sheet_data.get('earningAssets') else None,
                            'other_current_assets': float(sheet_data.get('otherCurrentAssets')) if sheet_data.get('otherCurrentAssets') else None,
                            'total_liabilities': float(sheet_data.get('totalLiab')) if sheet_data.get('totalLiab') else None,
                            'total_stockholder_equity': float(sheet_data.get('totalStockholderEquity')) if sheet_data.get('totalStockholderEquity') else None,
                            'deferred_long_term_liabilities': float(sheet_data.get('deferredLongTermLiab')) if sheet_data.get('deferredLongTermLiab') else None,
                            'other_current_liabilities': float(sheet_data.get('otherCurrentLiab')) if sheet_data.get('otherCurrentLiab') else None,
                            'common_stock': float(sheet_data.get('commonStock')) if sheet_data.get('commonStock') else None,
                            'capital_stock': float(sheet_data.get('capitalStock')) if sheet_data.get('capitalStock') else None,
                            'retained_earnings': float(sheet_data.get('retainedEarnings')) if sheet_data.get('retainedEarnings') else None,
                            'other_liabilities': float(sheet_data.get('otherLiab')) if sheet_data.get('otherLiab') else None,
                            'goodwill': float(sheet_data.get('goodWill')) if sheet_data.get('goodWill') else None,
                            'other_assets': float(sheet_data.get('otherAssets')) if sheet_data.get('otherAssets') else None,
                            'cash': float(sheet_data.get('cash')) if sheet_data.get('cash') else None,
                            'cash_and_equivalents': float(sheet_data.get('cashAndEquivalents')) if sheet_data.get('cashAndEquivalents') else None,
                            'total_current_liabilities': float(sheet_data.get('totalCurrentLiabilities')) if sheet_data.get('totalCurrentLiabilities') else None,
                            'current_deferred_revenue': float(sheet_data.get('currentDeferredRevenue')) if sheet_data.get('currentDeferredRevenue') else None,
                            'net_debt': float(sheet_data.get('netDebt')) if sheet_data.get('netDebt') else None,
                            'short_term_debt': float(sheet_data.get('shortTermDebt')) if sheet_data.get('shortTermDebt') else None,
                            'short_long_term_debt': float(sheet_data.get('shortLongTermDebt')) if sheet_data.get('shortLongTermDebt') else None,
                            'short_long_term_debt_total': float(sheet_data.get('shortLongTermDebtTotal')) if sheet_data.get('shortLongTermDebtTotal') else None,
                            'other_stockholder_equity': float(sheet_data.get('otherStockholderEquity')) if sheet_data.get('otherStockholderEquity') else None,
                            'property_plant_equipment': float(sheet_data.get('propertyPlantEquipment')) if sheet_data.get('propertyPlantEquipment') else None,
                            'total_current_assets': float(sheet_data.get('totalCurrentAssets')) if sheet_data.get('totalCurrentAssets') else None,
                            'long_term_investments': float(sheet_data.get('longTermInvestments')) if sheet_data.get('longTermInvestments') else None,
                            'net_tangible_assets': float(sheet_data.get('netTangibleAssets')) if sheet_data.get('netTangibleAssets') else None,
                            'short_term_investments': float(sheet_data.get('shortTermInvestments')) if sheet_data.get('shortTermInvestments') else None,
                            'net_receivables': float(sheet_data.get('netReceivables')) if sheet_data.get('netReceivables') else None,
                            'long_term_debt': float(sheet_data.get('longTermDebt')) if sheet_data.get('longTermDebt') else None,
                            'inventory': float(sheet_data.get('inventory')) if sheet_data.get('inventory') else None,
                            'accounts_payable': float(sheet_data.get('accountsPayable')) if sheet_data.get('accountsPayable') else None,
                            'total_permanent_equity': float(sheet_data.get('totalPermanentEquity')) if sheet_data.get('totalPermanentEquity') else None,
                            'noncontrolling_interest_in_consolidated_entity': float(sheet_data.get('noncontrollingInterestInConsolidatedEntity')) if sheet_data.get('noncontrollingInterestInConsolidatedEntity') else None,
                            'temporary_equity_redeemable_noncontrolling_interests': float(sheet_data.get('temporaryEquityRedeemableNoncontrollingInterests')) if sheet_data.get('temporaryEquityRedeemableNoncontrollingInterests') else None,
                            'accumulated_other_comprehensive_income': float(sheet_data.get('accumulatedOtherComprehensiveIncome')) if sheet_data.get('accumulatedOtherComprehensiveIncome') else None,
                            'additional_paid_in_capital': float(sheet_data.get('additionalPaidInCapital')) if sheet_data.get('additionalPaidInCapital') else None,
                            'common_stock_total_equity': float(sheet_data.get('commonStockTotalEquity')) if sheet_data.get('commonStockTotalEquity') else None,
                            'preferred_stock_total_equity': float(sheet_data.get('preferredStockTotalEquity')) if sheet_data.get('preferredStockTotalEquity') else None,
                            'retained_earnings_total_equity': float(sheet_data.get('retainedEarningsTotalEquity')) if sheet_data.get('retainedEarningsTotalEquity') else None,
                            'treasury_stock': float(sheet_data.get('treasuryStock')) if sheet_data.get('treasuryStock') else None,
                            'accumulated_amortization': float(sheet_data.get('accumulatedAmortization')) if sheet_data.get('accumulatedAmortization') else None,
                            'non_current_assets_other': float(sheet_data.get('nonCurrrentAssetsOther')) if sheet_data.get('nonCurrrentAssetsOther') else None,
                            'deferred_long_term_asset_charges': float(sheet_data.get('deferredLongTermAssetCharges')) if sheet_data.get('deferredLongTermAssetCharges') else None,
                            'non_current_assets_total': float(sheet_data.get('nonCurrentAssetsTotal')) if sheet_data.get('nonCurrentAssetsTotal') else None,
                            'capital_lease_obligations': float(sheet_data.get('capitalLeaseObligations')) if sheet_data.get('capitalLeaseObligations') else None,
                            'long_term_debt_total': float(sheet_data.get('longTermDebtTotal')) if sheet_data.get('longTermDebtTotal') else None,
                            'non_current_liabilities_other': float(sheet_data.get('nonCurrentLiabilitiesOther')) if sheet_data.get('nonCurrentLiabilitiesOther') else None,
                            'non_current_liabilities_total': float(sheet_data.get('nonCurrentLiabilitiesTotal')) if sheet_data.get('nonCurrentLiabilitiesTotal') else None,
                            'negative_goodwill': float(sheet_data.get('negativeGoodwill')) if sheet_data.get('negativeGoodwill') else None,
                            'warrants': float(sheet_data.get('warrants')) if sheet_data.get('warrants') else None,
                            'preferred_stock_redeemable': float(sheet_data.get('preferredStockRedeemable')) if sheet_data.get('preferredStockRedeemable') else None,
                            'capital_surplus': float(sheet_data.get('capitalSurplus')) if sheet_data.get('capitalSurplus') else None,
                            'liabilities_and_stockholders_equity': float(sheet_data.get('liabilitiesAndStockholdersEquity')) if sheet_data.get('liabilitiesAndStockholdersEquity') else None,
                            'cash_and_short_term_investments': float(sheet_data.get('cashAndShortTermInvestments')) if sheet_data.get('cashAndShortTermInvestments') else None,
                            'property_plant_and_equipment_gross': float(sheet_data.get('propertyPlantAndEquipmentGross')) if sheet_data.get('propertyPlantAndEquipmentGross') else None,
                            'property_plant_and_equipment_net': float(sheet_data.get('propertyPlantAndEquipmentNet')) if sheet_data.get('propertyPlantAndEquipmentNet') else None,
                            'accumulated_depreciation': float(sheet_data.get('accumulatedDepreciation')) if sheet_data.get('accumulatedDepreciation') else None,
                            'net_working_capital': float(sheet_data.get('netWorkingCapital')) if sheet_data.get('netWorkingCapital') else None,
                            'net_invested_capital': float(sheet_data.get('netInvestedCapital')) if sheet_data.get('netInvestedCapital') else None,
                            'common_stock_shares_outstanding': float(sheet_data.get('commonStockSharesOutstanding')) if sheet_data.get('commonStockSharesOutstanding') else None,
               }
            )
                except Exception as e:
                    # Log the error and include the stock's UID for clarity
                    self.stdout.write(self.style.ERROR(f"Error updating/creating balance sheet for {stock.uid}: {e}"))

def try_float(value):
    try:
        return float(value) if value else None
    except ValueError:
        self.stdout.write(self.style.ERROR(f"Error converting {value} to float"))
        return None
                
        # Process Cash Flow data
        for sheet_type in ['yearly', 'quarterly']:
            cash_flow_data = data.get('Financials', {}).get('Cash_Flow', {}).get(sheet_type, {})
            for key, sheet_data in cash_flow_data.items():
                try:
                    date_obj = datetime.strptime(key, '%Y-%m-%d').date()
                    datetime_obj = make_aware(datetime.combine(date_obj, datetime.min.time()))
                except ValueError:
                    self.stdout.write(self.style.ERROR(f"Invalid date format for {key} in {sheet_type} data."))
                    continue

                if date_obj.year < now().year - 5:
                    continue

                cash_flow, created = CashFlow.objects.update_or_create(
                    general=stock,
                    date=datetime_obj,
                    type=sheet_type,
                    defaults={
                        'filing_date': datetime.strptime(sheet_data.get('filing_date'), '%Y-%m-%d').date() if sheet_data.get('filing_date') else None,
                        'currency_symbol': sheet_data.get('currency_symbol', ''),
                        'investments': float(sheet_data.get('investments')) if sheet_data.get('investments') else None,
                        'change_to_liabilities': float(sheet_data.get('changeToLiabilities')) if sheet_data.get('changeToLiabilities') else None,
                        'total_cashflows_from_investing_activities': float(sheet_data.get('totalCashflowsFromInvestingActivities')) if sheet_data.get('totalCashflowsFromInvestingActivities') else None,
                        'net_borrowings': float(sheet_data.get('netBorrowings')) if sheet_data.get('netBorrowings') else None,
                        'total_cash_from_financing_activities': float(sheet_data.get('totalCashFromFinancingActivities')) if sheet_data.get('totalCashFromFinancingActivities') else None,
                        'change_to_operating_activities': float(sheet_data.get('changeToOperatingActivities')) if sheet_data.get('changeToOperatingActivities') else None,
                        'net_income': float(sheet_data.get('netIncome')) if sheet_data.get('netIncome') else None,
                        'change_in_cash': float(sheet_data.get('changeInCash')) if sheet_data.get('changeInCash') else None,
                        'begin_period_cash_flow': float(sheet_data.get('beginPeriodCashFlow')) if sheet_data.get('beginPeriodCashFlow') else None,
                        'end_period_cash_flow': float(sheet_data.get('endPeriodCashFlow')) if sheet_data.get('endPeriodCashFlow') else None,
                        'total_cash_from_operating_activities': float(sheet_data.get('totalCashFromOperatingActivities')) if sheet_data.get('totalCashFromOperatingActivities') else None,
                        'issuance_of_capital_stock': float(sheet_data.get('issuanceOfCapitalStock')) if sheet_data.get('issuanceOfCapitalStock') else None,
                        'depreciation': float(sheet_data.get('depreciation')) if sheet_data.get('depreciation') else None,
                        'other_cashflows_from_investing_activities': float(sheet_data.get('otherCashflowsFromInvestingActivities')) if sheet_data.get('otherCashflowsFromInvestingActivities') else None,
                        'dividends_paid': float(sheet_data.get('dividendsPaid')) if sheet_data.get('dividendsPaid') else None,
                        'change_to_inventory': float(sheet_data.get('changeToInventory')) if sheet_data.get('changeToInventory') else None,
                        'change_to_account_receivables': float(sheet_data.get('changeToAccountReceivables')) if sheet_data.get('changeToAccountReceivables') else None,
                        'sale_purchase_of_stock': float(sheet_data.get('salePurchaseOfStock')) if sheet_data.get('salePurchaseOfStock') else None,
                        'other_cashflows_from_financing_activities': float(sheet_data.get('otherCashflowsFromFinancingActivities')) if sheet_data.get('otherCashflowsFromFinancingActivities') else None,
                        'change_to_netincome': float(sheet_data.get('changeToNetincome')) if sheet_data.get('changeToNetincome') else None,
                        'capital_expenditures': float(sheet_data.get('capitalExpenditures')) if sheet_data.get('capitalExpenditures') else None,
                        'change_receivables': float(sheet_data.get('changeReceivables')) if sheet_data.get('changeReceivables') else None,
                        'cash_flows_other_operating': float(sheet_data.get('cashFlowsOtherOperating')) if sheet_data.get('cashFlowsOtherOperating') else None,
                        'exchange_rate_changes': float(sheet_data.get('exchangeRateChanges')) if sheet_data.get('exchangeRateChanges') else None,
                        'cash_and_cash_equivalents_changes': float(sheet_data.get('cashAndCashEquivalentsChanges')) if sheet_data.get('cashAndCashEquivalentsChanges') else None,
                        'change_in_working_capital': float(sheet_data.get('changeInWorkingCapital')) if sheet_data.get('changeInWorkingCapital') else None,
                        'stock_based_compensation': float(sheet_data.get('stockBasedCompensation')) if sheet_data.get('stockBasedCompensation') else None,
                        'other_non_cash_items': float(sheet_data.get('otherNonCashItems')) if sheet_data.get('otherNonCashItems') else None,
                        'free_cash_flow': float(sheet_data.get('freeCashFlow')) if sheet_data.get('freeCashFlow') else None,
                    }
                )     

       # Process Income Statement data
        for sheet_type in ['yearly', 'quarterly']:
            income_statement_data = data.get('Financials', {}).get('Income_Statement', {}).get(sheet_type, {})
            for key, sheet_data in income_statement_data.items():
                try:
                    date_obj = datetime.strptime(key, '%Y-%m-%d').date()
                except ValueError:
                    self.stdout.write(self.style.ERROR(f"Invalid date format for {key} in {sheet_type} data."))
                    continue

                # Ensure we only process data within the last 5 years
                if date_obj.year < datetime.now().year - 5:
                    continue

                income_statement, created = IncomeStatement.objects.update_or_create(
                    general=stock,
                    date=date_obj,
                    type=sheet_type,
                    defaults={
                        'filing_date': datetime.strptime(sheet_data.get('filing_date'), '%Y-%m-%d').date() if sheet_data.get('filing_date') else None,
                        'currency_symbol': sheet_data.get('currency_symbol', ''),
                        'research_development': float(sheet_data.get('researchDevelopment')) if sheet_data.get('researchDevelopment') else None,
                        'effect_of_accounting_charges': float(sheet_data.get('effectOfAccountingCharges')) if sheet_data.get('effectOfAccountingCharges') else None,
                        'income_before_tax': float(sheet_data.get('incomeBeforeTax')) if sheet_data.get('incomeBeforeTax') else None,
                        'minority_interest': float(sheet_data.get('minorityInterest')) if sheet_data.get('minorityInterest') else None,
                        'net_income': float(sheet_data.get('netIncome')) if sheet_data.get('netIncome') else None,
                        'selling_general_administrative': float(sheet_data.get('sellingGeneralAdministrative')) if sheet_data.get('sellingGeneralAdministrative') else None,
                        'selling_and_marketing_expenses': float(sheet_data.get('sellingAndMarketingExpenses')) if sheet_data.get('sellingAndMarketingExpenses') else None,
                        'gross_profit': float(sheet_data.get('grossProfit')) if sheet_data.get('grossProfit') else None,
                        'reconciled_depreciation': float(sheet_data.get('reconciledDepreciation')) if sheet_data.get('reconciledDepreciation') else None,
                        'ebit': float(sheet_data.get('ebit')) if sheet_data.get('ebit') else None,
                        'ebitda': float(sheet_data.get('ebitda')) if sheet_data.get('ebitda') else None,
                        'depreciation_and_amortization': float(sheet_data.get('depreciationAndAmortization')) if sheet_data.get('depreciationAndAmortization') else None,
                        'non_operating_income_net_other': float(sheet_data.get('nonOperatingIncomeNetOther')) if sheet_data.get('nonOperatingIncomeNetOther') else None,
                        'operating_income': float(sheet_data.get('operatingIncome')) if sheet_data.get('operatingIncome') else None,
                        'other_operating_expenses': float(sheet_data.get('otherOperatingExpenses')) if sheet_data.get('otherOperatingExpenses') else None,
                        'interest_expense': float(sheet_data.get('interestExpense')) if sheet_data.get('interestExpense') else None,
                        'tax_provision': float(sheet_data.get('taxProvision')) if sheet_data.get('taxProvision') else None,
                        'interest_income': float(sheet_data.get('interestIncome')) if sheet_data.get('interestIncome') else None,
                        'net_interest_income': float(sheet_data.get('netInterestIncome')) if sheet_data.get('netInterestIncome') else None,
                        'extraordinary_items': float(sheet_data.get('extraordinaryItems')) if sheet_data.get('extraordinaryItems') else None,
                        'non_recurring': float(sheet_data.get('nonRecurring')) if sheet_data.get('nonRecurring') else None,
                        'other_items': float(sheet_data.get('otherItems')) if sheet_data.get('otherItems') else None,
                        'income_tax_expense': float(sheet_data.get('incomeTaxExpense')) if sheet_data.get('incomeTaxExpense') else None,
                        'total_revenue': float(sheet_data.get('totalRevenue')) if sheet_data.get('totalRevenue') else None,
                        'total_operating_expenses': float(sheet_data.get('totalOperatingExpenses')) if sheet_data.get('totalOperatingExpenses') else None,
                        'cost_of_revenue': float(sheet_data.get('costOfRevenue')) if sheet_data.get('costOfRevenue') else None,
                        'total_other_income_expense_net': float(sheet_data.get('totalOtherIncomeExpenseNet')) if sheet_data.get('totalOtherIncomeExpenseNet') else None,
                        'discontinued_operations': float(sheet_data.get('discontinuedOperations')) if sheet_data.get('discontinuedOperations') else None,
                        'net_income_from_continuing_ops': float(sheet_data.get('netIncomeFromContinuingOps')) if sheet_data.get('netIncomeFromContinuingOps') else None,
                        'net_income_applicable_to_common_shares': float(sheet_data.get('netIncomeApplicableToCommonShares')) if sheet_data.get('netIncomeApplicableToCommonShares') else None,
                        'preferred_stock_and_other_adjustments': float(sheet_data.get('preferredStockAndOtherAdjustments')) if sheet_data.get('preferredStockAndOtherAdjustments') else None,
                    }
                )

        print(f"Updated all data for {stock.uid}")