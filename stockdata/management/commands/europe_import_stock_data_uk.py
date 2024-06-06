from django.core.management.base import BaseCommand
from stockdata.models import (
    General, Description, Highlights, Valuation, Technicals, SplitsDividends,
    AnalystRatings, BalanceSheet, CashFlow, IncomeStatement
)
from django.utils.dateparse import parse_date
import requests
from datetime import datetime
from django.utils.timezone import make_aware, now
from decouple import config
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.db.utils import DataError


def parse_date(date_string):
    try:
        return (
            datetime.strptime(date_string, '%Y-%m-%d').date()
            if date_string and date_string != '0000-00-00'
            else None
        )
    except ValueError:
        return None


def import_tickers(api_token, exchange='LSE'):
    ticker_url = (
        f'https://eodhd.com/api/exchange-symbol-list/{exchange}?api_token='
        f'{api_token}&fmt=json'
    )
    response = requests.get(ticker_url)

    if response.status_code == 200:
        ticker_data = response.json()

        for entry in ticker_data:
            uid = f"{entry['Code']}.{exchange}"

            if len(uid) > 20:
                print(
                    f"Skipping ticker {uid} because it's longer than 20 "
                    "characters."
                )
                continue

            General.objects.update_or_create(
                uid=uid,
                defaults={
                    'code': entry['Code'],
                }
            )
        print(f'Successfully imported tickers for {exchange}.')
    else:
        print(
            f'Failed to download ticker list for {exchange}. Status code: '
            f'{response.status_code}'
        )


class Command(BaseCommand):
    help = 'Imports stock data from the EOD Historical Data API'

    def add_arguments(self, parser):
        parser.add_argument('start_index', nargs='?', type=int, default=0)

    def handle(self, *args, **kwargs):
        api_token = config('API_TOKEN')
        # import_tickers(api_token)
        start_index = kwargs['start_index']

        # Fetch all stocks listed on the LSE from the General table
        stocks = General.objects.filter(uid__endswith='.LSE')

        print(f"Total stocks found: {stocks.count()}")

        for i, stock in enumerate(stocks, start=start_index + 1):
            print(f"Processing stock {i}/{stocks.count()}: {stock.uid}")
            url = (
                f'https://eodhd.com/api/fundamentals/{stock.uid}?api_token='
                f'{api_token}&fmt=json'
            )
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.update_stock(stock, data)
            else:
                print(
                    f"Failed to fetch data for {stock.uid}. Status code: "
                    f'{response.status_code}'
                )

    def update_stock(self, stock, data):
        try:
            general_info = data.get('General', {})
            logo_url = general_info.get('LogoURL')

            if logo_url and not stock.logo:
                full_logo_url = f"https://eodhd.com{logo_url}"

                try:
                    response = requests.get(full_logo_url, stream=True)
                    if response.status_code == 200:
                        logo_name = os.path.basename(logo_url)
                        file_path = default_storage.save(
                            f'logos/{logo_name}', ContentFile(response.content)
                        )
                        stock.logo = file_path
                        stock.save()
                        print(f"Downloaded and saved logo for {stock.code}")
                except requests.RequestException as e:
                    print(f"Failed to download logo for {stock.code}: {e}")

            General.objects.filter(uid=stock.uid).update(
                code=general_info.get('Code', stock.code),
                type=general_info.get('Type', stock.type),
                name=general_info.get('Name', stock.name),
                primary_ticker=general_info.get(
                    'PrimaryTicker', stock.primary_ticker
                ),
                exchange=general_info.get('Exchange', stock.exchange),
                currency_code=general_info.get(
                    'CurrencyCode', stock.currency_code
                ),
                currency_name=general_info.get(
                    'CurrencyName', stock.currency_name
                ),
                currency_symbol=general_info.get(
                    'CurrencySymbol', stock.currency_symbol
                ),
                country_name=general_info.get(
                    'CountryName', stock.country_name
                ),
                country_iso=general_info.get('CountryISO', stock.country_iso),
                isin=general_info.get('ISIN', stock.isin),
                fiscal_year_end=general_info.get(
                    'FiscalYearEnd', stock.fiscal_year_end
                ),
                sector=general_info.get('Sector', stock.sector),
                industry=general_info.get('Industry', stock.industry),
                address=general_info.get('Address', stock.address),
                phone=general_info.get('Phone', stock.phone),
                web_url=general_info.get('WebURL', stock.web_url),
                full_time_employees=general_info.get(
                    'FullTimeEmployees', stock.full_time_employees
                ),
                updated_at=parse_date(general_info.get('UpdatedAt'))
                if general_info.get('UpdatedAt')
                else stock.updated_at,
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
                defaults = {
                    'market_capitalization': highlights_data.get(
                        'MarketCapitalization'
                    ),
                    'ebitda': highlights_data.get('EBITDA'),
                    'pe_ratio': highlights_data.get('PERatio'),
                    'peg_ratio': highlights_data.get('PEGRatio'),
                    'wall_street_target_price': highlights_data.get(
                        'WallStreetTargetPrice'
                    ),
                    'book_value': highlights_data.get('BookValue'),
                    'dividend_share': highlights_data.get('DividendShare'),
                    'dividend_yield': highlights_data.get('DividendYield'),
                    'earnings_share': highlights_data.get('EarningsShare'),
                    'eps_estimate_current_year': highlights_data.get(
                        'EPSEstimateCurrentYear'
                    ),
                    'eps_estimate_next_year': highlights_data.get(
                        'EPSEstimateNextYear'
                    ),
                    'eps_estimate_next_quarter': highlights_data.get(
                        'EPSEstimateNextQuarter'
                    ),
                    'eps_estimate_current_quarter': highlights_data.get(
                        'EPSEstimateCurrentQuarter'
                    ),
                    'most_recent_quarter': parse_date(
                        highlights_data.get('MostRecentQuarter')
                    ),
                    'profit_margin': highlights_data.get('ProfitMargin'),
                    'operating_margin_ttm': highlights_data.get(
                        'OperatingMarginTTM'
                    ),
                    'return_on_assets_ttm': highlights_data.get(
                        'ReturnOnAssetsTTM'
                    ),
                    'return_on_equity_ttm': highlights_data.get(
                        'ReturnOnEquityTTM'
                    ),
                    'revenue_ttm': highlights_data.get('RevenueTTM'),
                    'revenue_per_share_ttm': highlights_data.get(
                        'RevenuePerShareTTM'
                    ),
                    'quarterly_revenue_growth_yoy': highlights_data.get(
                        'QuarterlyRevenueGrowthYOY'
                    ),
                    'gross_profit_ttm': highlights_data.get(
                        'GrossProfitTTM'
                    ),
                    'diluted_eps_ttm': highlights_data.get('DilutedEpsTTM'),
                    'quarterly_earnings_growth_yoy': highlights_data.get(
                        'QuarterlyEarningsGrowthYOY'
                    ),
                }

                try:
                    Highlights.objects.update_or_create(
                        general=stock,
                        defaults=defaults
                    )
                except DataError as e:
                    print(f"Skipping {stock.uid} due to data error: {e}")
                except Exception as e:
                    print(f"Skipping {stock.uid} due to unexpected error: {e}")

            valuation_data = data.get('Valuation', {})
            if valuation_data:
                Valuation.objects.update_or_create(
                    general=stock,
                    defaults={
                        'trailing_pe': valuation_data.get('TrailingPE'),
                        'forward_pe': valuation_data.get('ForwardPE'),
                        'price_sales_ttm': valuation_data.get('PriceSalesTTM'),
                        'price_book_mrq': valuation_data.get('PriceBookMRQ'),
                        'enterprise_value': valuation_data.get(
                            'EnterpriseValue'
                        ),
                        'enterprise_value_revenue': valuation_data.get(
                            'EnterpriseValueRevenue'
                        ),
                        'enterprise_value_ebitda': valuation_data.get(
                            'EnterpriseValueEbitda'
                        ),
                    }
                )

            technicals_data = data.get('Technicals', {})
            if technicals_data:
                Technicals.objects.update_or_create(
                    general=stock,
                    defaults={
                        'beta': technicals_data.get('Beta'),
                        'fifty_two_week_high': technicals_data.get(
                            '52WeekHigh'
                        ),
                        'fifty_two_week_low': technicals_data.get(
                            '52WeekLow'
                        ),
                        'fifty_day_ma': technicals_data.get('50DayMA'),
                        'two_hundred_day_ma': technicals_data.get('200DayMA'),
                        'shares_short': technicals_data.get('SharesShort'),
                        'shares_short_prior_month': technicals_data.get(
                            'SharesShortPriorMonth'
                        ),
                        'short_ratio': technicals_data.get('ShortRatio'),
                        'short_percent': technicals_data.get('ShortPercent'),
                    }
                )

            splits_dividends_data = data.get('SplitsDividends', {})
            if splits_dividends_data:
                SplitsDividends.objects.update_or_create(
                    general=stock,
                    defaults={
                        'forward_annual_dividend_rate':
                            splits_dividends_data.get(
                                'ForwardAnnualDividendRate'
                            ),
                        'forward_annual_dividend_yield':
                            splits_dividends_data.get(
                                'ForwardAnnualDividendYield'
                            ),
                        'payout_ratio':
                            splits_dividends_data.get(
                                'PayoutRatio'
                            ),
                        'dividend_date':
                            parse_date(
                                splits_dividends_data.get('DividendDate')
                            ),
                        'ex_dividend_date':
                            parse_date(
                                splits_dividends_data.get('ExDividendDate')
                            ),
                        'last_split_factor':
                            splits_dividends_data.get(
                                'LastSplitFactor'
                            ),
                        'last_split_date':
                            parse_date(
                                splits_dividends_data.get('LastSplitDate')
                            ),
                    }
                )

            analyst_ratings_data = data.get('AnalystRatings', {})
            if analyst_ratings_data:
                AnalystRatings.objects.update_or_create(
                    general=stock,
                    defaults={
                        'rating': analyst_ratings_data.get('Rating'),
                        'target_price': analyst_ratings_data.get(
                            'TargetPrice'
                        ),
                        'strong_buy': analyst_ratings_data.get('StrongBuy'),
                        'buy': analyst_ratings_data.get('Buy'),
                        'hold': analyst_ratings_data.get('Hold'),
                        'sell': analyst_ratings_data.get('Sell'),
                        'strong_sell': analyst_ratings_data.get(
                            'StrongSell'
                        ),
                    }
                )

            # Process Balance Sheet data
            for sheet_type in ['yearly', 'quarterly']:
                balance_sheet_data = data.get('Financials', {}).get(
                    'Balance_Sheet', {}
                ).get(sheet_type, {})
                for key, sheet_data in balance_sheet_data.items():
                    try:
                        date_obj = datetime.strptime(key, '%Y-%m-%d').date()
                        datetime_obj = make_aware(
                            datetime.combine(date_obj, datetime.min.time())
                        )
                    except ValueError:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Invalid date format for {key} in "
                                f'{sheet_type} data.'
                            )
                        )
                        continue

                    if date_obj.year < now().year - 5:
                        continue

                    try:
                        balance_sheet, created = \
                            BalanceSheet.objects.update_or_create(
                                general=stock,
                                date=datetime_obj,
                                type=sheet_type,
                                defaults={
                                    'common_stock_shares_outstanding': float(
                                        sheet_data.get(
                                            'commonStockSharesOutstanding'
                                        )
                                    )
                                    if sheet_data.get(
                                        'commonStockSharesOutstanding'
                                    )
                                    else None,
                                }
                            )
                    except Exception as e:
                        # Log the error and include the stock's UID for clarity
                        self.stdout.write(
                            self.style.ERROR(
                                f"Error updating/creating balance sheet for "
                                f'{stock.uid}: {e}'
                            )
                        )

            # Process Cash Flow data
            for sheet_type in ['yearly', 'quarterly']:
                cash_flow_data = data.get('Financials', {}).get(
                    'Cash_Flow', {}
                ).get(sheet_type, {})
                for key, sheet_data in cash_flow_data.items():
                    try:
                        date_obj = datetime.strptime(key, '%Y-%m-%d').date()
                        datetime_obj = make_aware(
                            datetime.combine(date_obj, datetime.min.time())
                        )
                    except ValueError:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Invalid date format for {key} in "
                                f'{sheet_type} data.'
                            )
                        )
                        continue

                    if date_obj.year < now().year - 5:
                        continue

                    cash_flow, created = CashFlow.objects.update_or_create(
                        general=stock,
                        date=datetime_obj,
                        type=sheet_type,
                        defaults={
                            'dividends_paid': float(
                                sheet_data.get('dividendsPaid')
                            )
                            if sheet_data.get('dividendsPaid')
                            else None,
                        }
                    )

            # Process Income Statement data
            for sheet_type in ['yearly', 'quarterly']:
                income_statement_data = data.get('Financials', {}).get(
                    'Income_Statement', {}
                ).get(sheet_type, {})
                for key, sheet_data in income_statement_data.items():
                    try:
                        date_obj = datetime.strptime(key, '%Y-%m-%d').date()
                    except ValueError:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Invalid date format for {key} in "
                                f'{sheet_type} data.'
                            )
                        )
                        continue

                    # Ensure we only process data within the last 5 years
                    if date_obj.year < datetime.now().year - 5:
                        continue

                    income_statement, created = \
                        IncomeStatement.objects.update_or_create(
                            general=stock,
                            date=date_obj,
                            type=sheet_type,
                            defaults={
                                'net_income': float(
                                    sheet_data.get('netIncome')
                                )
                                if sheet_data.get('netIncome')
                                else None,
                                'gross_profit': float(
                                    sheet_data.get('grossProfit')
                                )
                                if sheet_data.get('grossProfit')
                                else None,
                                'total_revenue': float(
                                    sheet_data.get('totalRevenue')
                                )
                                if sheet_data.get('totalRevenue')
                                else None,
                            }
                        )

            print(f"Updated all data for {stock.uid}")

        except DataError as e:
            print(f"Skipping {stock.uid} due to data error: {e}")
        except Exception as e:
            print(f"Skipping {stock.uid} due to unexpected error: {e}")
