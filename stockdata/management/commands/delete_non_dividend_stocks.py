from django.core.management.base import BaseCommand
from django.db.models import Q
from stockdata.models import General, Highlights

class Command(BaseCommand):
    help = 'Deletes stocks with Highlights dividend_yield blank or 0.00'

    def handle(self, *args, **kwargs):
        stocks_to_delete = General.objects.filter(
            Q(highlights__dividend_yield__isnull=True) | 
            Q(highlights__dividend_yield=0.00)
        )

        count = stocks_to_delete.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS('No stocks to delete based on dividend_yield criteria.'))
            return

        self.stdout.write(f'Found {count} stocks with dividend_yield blank or 0.00.')

        confirm = input('Do you want to delete these stocks? [yes/no]: ')

        if confirm.lower() != 'yes':
            self.stdout.write(self.style.NOTICE('Deletion cancelled.'))
            return

        for stock in stocks_to_delete.iterator():
            self.stdout.write(f'Deleting stock: {stock.name} ({stock.code}) due to dividend_share criteria.')
            stock.delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} stocks based on dividend_share criteria.'))
