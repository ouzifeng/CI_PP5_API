from django.core.management.base import BaseCommand
from stockdata.models import General, Description, Highlights, Valuation, Technicals, SplitsDividends, AnalystRatings, BalanceSheet, CashFlow, IncomeStatement
import requests
from datetime import datetime



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
        api_token = '649401f5eeff73.67939383'
        import_tickers(api_token)
