from django.core.management.base import BaseCommand
from stockdata.models import General

class Command(BaseCommand):
    help = 'Deletes stocks where type is not "Common Stock"'

    def handle(self, *args, **kwargs):
        stocks_to_delete = General.objects.exclude(type="Common Stock")

        count = stocks_to_delete.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS('No non-"Common Stock" types to delete.'))
            return

        self.stdout.write(f'Found {count} stocks where type is not "Common Stock".')

        confirm = input('Do you want to delete these stocks? [yes/no]: ')

        if confirm.lower() != 'yes':
            self.stdout.write(self.style.NOTICE('Deletion cancelled.'))
            return

        for stock in stocks_to_delete.iterator():
            self.stdout.write(f'Deleting stock: {stock.name} ({stock.code}) with type: {stock.type}')
            stock.delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} non-"Common Stock" stocks.'))
