from django.core.management.base import BaseCommand
from stockdata.models import General, StockPrices, SplitsDividends
import requests
from datetime import datetime
from decouple import config


class Command(BaseCommand):
    help = (
        'Fetches stock prices, adjusts for stock splits, and calculates CAGR '
        'for each stock'
    )

    def fetch_stock_prices(self, uid):
        api_token = config('API_TOKEN')
        url = (
            f'https://eodhd.com/api/eod/{uid}?api_token={api_token}&fmt=json'
        )
        response = requests.get(url)
        if response.ok:
            try:
                return response.json()
            except ValueError:
                self.stdout.write(
                    self.style.ERROR(f'Invalid JSON response for UID: {uid}')
                )
        else:
            self.stdout.write(
                self.style.ERROR(
                    f'Failed to fetch data for UID: {uid}, HTTP Status Code: '
                    f'{response.status_code}'
                )
            )
        return []

    def calculate_cagr(self, initial_value, final_value, years):
        if initial_value and final_value and years > 0:
            return (final_value / initial_value) ** (1 / years) - 1
        return None

    def filter_end_of_year_prices(self, stock_prices):
        current_year = datetime.now().year
        start_year = current_year - 6
        end_of_year_prices = {}

        for record in stock_prices:
            date = datetime.strptime(record['date'], '%Y-%m-%d').date()
            if start_year <= date.year <= current_year and date.month == 12:
                if (
                    date.year not in end_of_year_prices or
                    date.day > end_of_year_prices[date.year]['date'].day
                ):
                    end_of_year_prices[date.year] = {
                        'date': date,
                        'price': record['close']
                    }

        return end_of_year_prices

    def adjust_for_splits(self, sorted_prices, splits_dividends):
        adjusted_prices = []
        for year, price_data in sorted_prices:
            adjusted_price = price_data['price']
            if (
                splits_dividends and splits_dividends.last_split_date and
                splits_dividends.last_split_factor and
                price_data['date'] < splits_dividends.last_split_date
            ):
                split_factor_parts = splits_dividends.last_split_factor.split(
                    ':'
                )
                if len(split_factor_parts) == 2:
                    split_factor = (
                        float(split_factor_parts[1]) /
                        float(split_factor_parts[0])
                    )
                    adjusted_price *= split_factor
            adjusted_prices.append(adjusted_price)
        return adjusted_prices

    def handle(self, *args, **kwargs):
        for general in General.objects.all():
            # Fetch stock prices and split/dividend data
            stock_prices = self.fetch_stock_prices(general.uid)
            end_of_year_prices = self.filter_end_of_year_prices(stock_prices)
            splits_dividends = SplitsDividends.objects.filter(
                general=general
            ).first()

            # Sort and adjust prices for stock splits
            sorted_prices = sorted(
                end_of_year_prices.items(),
                key=lambda x: x[0],
                reverse=True
            )
            adjusted_prices = self.adjust_for_splits(
                sorted_prices,
                splits_dividends
            )

            # Calculate CAGR
            cagr_5_years = (
                self.calculate_cagr(adjusted_prices[4], adjusted_prices[0], 5)
                if len(adjusted_prices) >= 5 else None
            )

            # Save the data to the database
            StockPrices.objects.update_or_create(
                general=general,
                defaults={
                    f'Y{idx + 1}': price for idx, price in enumerate(
                        adjusted_prices
                    )
                } | {
                    'cagr_5_years': cagr_5_years,
                }
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully updated stock prices for {general.uid}'
                )
            )
