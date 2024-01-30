from django.core.management.base import BaseCommand
from stockdata.models import IncomeStatement, CAGR, General
from django.db.models import Q
import datetime
from decimal import Decimal

class Command(BaseCommand):
    help = 'Calculate and store CAGR values for Income Statements.'

    def calculate_metric_cagr(self, start_value, end_value, periods=5):
        # Ensure start_value is not zero to avoid division by zero error
        if start_value and end_value and start_value != Decimal('0'):
            # Convert Decimal to float for calculation
            start_value = float(start_value)
            end_value = float(end_value)
            # CAGR formula: [(End Value/Start Value) ** (1/Periods)] - 1
            cagr = (end_value / start_value) ** (1.0 / periods) - 1
            return cagr
        else:
            # Return None or 0 or any other value you consider appropriate when CAGR cannot be calculated
            return None

    def handle(self, *args, **options):
        # Define the date 5 years ago from today
        five_years_ago = datetime.date.today() - datetime.timedelta(days=5*365)

        for general in General.objects.all():
            income_statements = IncomeStatement.objects.filter(
                general=general,
                date__gte=five_years_ago,
                type='yearly'
            ).order_by('-date')  # Order by date descending

            if income_statements.count() >= 5:
                # Extract values for the oldest and newest records
                newest = income_statements.first()  # The first after ordering by date descending
                oldest = income_statements.order_by('date').first()  # Reordering to get the oldest

                # Calculate CAGR for each metric
                total_revenue_cagr = self.calculate_metric_cagr(oldest.total_revenue, newest.total_revenue)
                gross_profit_cagr = self.calculate_metric_cagr(oldest.gross_profit, newest.gross_profit)
                net_income_cagr = self.calculate_metric_cagr(oldest.net_income, newest.net_income)

                # Fetch or create a CAGR instance for the general
                cagr, created = CAGR.objects.get_or_create(general=general)
                cagr.total_revenue_cagr = total_revenue_cagr
                cagr.gross_profit_cagr = gross_profit_cagr
                cagr.net_income_cagr = net_income_cagr
                cagr.save()

                self.stdout.write(self.style.SUCCESS(f'Successfully calculated CAGR for {general.name}'))

