from django.core.management.base import BaseCommand
from stockdata.models import General, Prices
import requests
from decouple import config
from decimal import Decimal, ROUND_HALF_UP

class Command(BaseCommand):
    help = 'Download EOD prices for listed exchanges and update Prices model if there is a change'

    def handle(self, *args, **options):
        api_token = config('API_TOKEN')
        exchanges = [
            'LSE', 'XETRA', 'VI', 'PA', 'BR', 'MC', 'SW', 'LS', 'AS', 'IR', 
            'HE', 'OL', 'CO', 'ST', 'BUD', 'WAR', 'AT', 'RO'
        ]

        for exchange in exchanges:
            url = f'https://eodhd.com/api/eod-bulk-last-day/{exchange}?api_token={api_token}&fmt=json'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                for item in data:
                    uid = f"{item['code']}.{item['exchange_short_name']}"
                    general = General.objects.filter(uid=uid).first()
                    
                    if general:
                        current_close = Decimal(item.get('close')).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
                        last_price = Prices.objects.filter(general=general).first()

                        if last_price:
                            last_recorded_close = Decimal(last_price.close).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

                            if last_recorded_close == current_close:
                                self.stdout.write(f"No change for {uid}, skipping update")
                                continue
                            else:
                                self.stdout.write(f"Price change detected for {uid}: {last_recorded_close} to {current_close}")
                        else:
                            self.stdout.write(f"First price entry for {uid}")

                        # Proceed only if there is no last_price or the close price has changed
                        if not last_price or last_price.close != current_close:
                            # Define previous close if last_price exists
                            prev_close = last_price.close if last_price else None
                            # Calculate change and change percentage if prev_close exists
                            change = current_close - prev_close if prev_close else None
                            change_p = (change / prev_close * 100) if prev_close else None

                            Prices.objects.update_or_create(
                                general=general,
                                defaults={
                                    'close': current_close,
                                    'prev_close': prev_close,
                                    'change': change,
                                    'change_p': change_p,
                                }
                            )
                            self.stdout.write(f"Updated prices for {uid}")
                        else:
                            self.stdout.write(f"No change for {uid}, skipping update")
                    else:
                        self.stdout.write(f"No General entry found for {uid}, skipping")
            else:
                self.stdout.write(f"Failed to download data for {exchange}, status code {response.status_code}")
