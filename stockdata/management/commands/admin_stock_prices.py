from django.core.management.base import BaseCommand
from stockdata.models import General, Prices
from django.utils.dateparse import parse_date
import requests
from datetime import datetime, timedelta
from django.utils.timezone import make_aware, now
from decouple import config
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.db.utils import DataError

class Command(BaseCommand):
    help = 'Download EOD prices for listed exchanges and update Prices model'

    def handle(self, *args, **options):
        api_token = config('API_TOKEN')
        exchanges = [
            'LSE', 
            #'XETRA', 'VI', 'PA', 'BR', 'MC', 'SW', 'LS', 'AS', 'IR', 
            #'HE', 'OL', 'CO', 'ST', 'BUD', 'WAR', 'AT', 'RO'
        ]

        for exchange in exchanges:
            url = f'https://eodhd.com/api/eod-bulk-last-day/{exchange}?api_token={api_token}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                for item in data:
                    uid = f"{item['code']}/{item['exchange_short_name']}"
                    general = General.objects.filter(uid=uid).first()
                    
                    if general:
                        Prices.objects.update_or_create(
                            general=general,
                            defaults={
                                'close': item.get('close'),
                                'prev_close': item.get('prev_close'),
                                'change': item.get('change'),
                                'change_p': item.get('change_p'),
                            }
                        )
                        self.stdout.write(f"Updated prices for {uid}.")
                    else:
                        self.stdout.write(f"No General entry found for {uid}, skipping.")
            else:
                self.stdout.write(f"Failed to download data for {exchange}, status code {response.status_code}")
