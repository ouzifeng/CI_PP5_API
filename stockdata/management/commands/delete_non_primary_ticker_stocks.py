from django.core.management.base import BaseCommand
from django.db.models import F
from .models import General

class Command(BaseCommand):
    help = 'Deletes stocks where uid != primary_ticker and primary_ticker is not blank'

    def handle(self, *args, **kwargs):
        stocks_to_delete = General.objects.filter(primary_ticker__isnull=False).exclude(uid=F('primary_ticker'))

        count = stocks_to_delete.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS('No stocks to delete.'))
            return

        self.stdout.write(f'{count} stocks found where uid != primary_ticker and primary_ticker is not blank.')

        confirm = input('Do you want to delete these stocks? [yes/no]: ')

        if confirm.lower() != 'yes':
            self.stdout.write(self.style.NOTICE('Deletion cancelled.'))
            return

        for stock in stocks_to_delete.iterator():
            self.stdout.write(f'Deleting stock: {stock.name} ({stock.code}) with UID: {stock.uid} and Primary Ticker: {stock.primary_ticker}')
            stock.delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} stocks.'))
