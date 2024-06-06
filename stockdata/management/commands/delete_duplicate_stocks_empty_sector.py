from django.core.management.base import BaseCommand
from django.db.models import Count
from stockdata.models import General


class Command(BaseCommand):
    help = 'Deletes stocks with duplicated names where sector is blank'

    def handle(self, *args, **kwargs):
        # Identify duplicated names
        duplicated_names = (
            General.objects.values('name')
            .annotate(name_count=Count('id'))
            .filter(name_count__gt=1)
        )

        # Filter stocks with those duplicated names where sector is blank
        stocks_to_delete = General.objects.filter(
            name__in=[item['name'] for item in duplicated_names],
            sector__in=[None, '']
        )

        count = stocks_to_delete.count()

        if count == 0:
            self.stdout.write(
                self.style.SUCCESS('No stocks to delete based on criteria.')
            )
            return

        self.stdout.write(
            f'{count} stocks found with duplicated names and blank sector.'
        )

        confirm = input('Do you want to delete these stocks? [yes/no]: ')

        if confirm.lower() != 'yes':
            self.stdout.write(self.style.NOTICE('Deletion cancelled.'))
            return

        for stock in stocks_to_delete.iterator():
            self.stdout.write(
                f'Deleting stock: {stock.name} ({stock.code}) with '
                f'ID: {stock.id}'
            )
            stock.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully deleted {count} stocks based on criteria.'
            )
        )
