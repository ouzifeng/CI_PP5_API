from django.core.management.base import BaseCommand
from django.db import transaction
from stockdata.models import General, StockPrices, DividendYieldData, BalanceSheet, CashFlow
from django.core.exceptions import ValidationError

class Command(BaseCommand):
    help = 'Calculate and store dividend yields and CAGR for each stock, handling cases with missing dividend data'

    def calculate_dividend_yield(self, dividends_paid, shares_outstanding, stock_price):
        try:
            if dividends_paid and shares_outstanding and stock_price and shares_outstanding > 0 and stock_price > 0:
                return (dividends_paid / shares_outstanding) / stock_price
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error calculating dividend yield: {e}"))
        return None

    def calculate_cagr(self, initial_value, final_value, years):
        try:
            if initial_value and final_value and years > 0:
                initial_value = float(initial_value)
                final_value = float(final_value)
                return (final_value / initial_value) ** (1 / years) - 1
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error calculating CAGR: {e}"))
        return None

    def handle(self, *args, **kwargs):
        for general in General.objects.all():
            try:
                stock_prices = StockPrices.objects.filter(general=general).first()
                cash_flow_records = CashFlow.objects.filter(general=general, type='yearly').order_by('-date')[:5]
                balance_sheet_records = BalanceSheet.objects.filter(general=general, type='yearly').order_by('-date')[:5]
                dividend_yields = []

                for idx, (cash_flow, balance_sheet) in enumerate(zip(cash_flow_records, balance_sheet_records)):
                    try:
                        stock_price = getattr(stock_prices, f'Y{idx + 1}', None)
                        dividend_yield = self.calculate_dividend_yield(
                            dividends_paid=cash_flow.dividends_paid,
                            shares_outstanding=balance_sheet.common_stock_shares_outstanding,
                            stock_price=stock_price
                        )
                        if dividend_yield is not None:
                            dividend_yields.append(dividend_yield)
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error processing stock {general.name} for year {idx + 1}: {e}"))

                # Calculate Dividend Yield CAGR only if there are at least 2 valid years of data
                cagr_5_years = None
                if len(dividend_yields) >= 2:
                    cagr_5_years = self.calculate_cagr(dividend_yields[-1], dividend_yields[0], len(dividend_yields) - 1)

                # Save the data to the DividendYieldData model
                with transaction.atomic():
                    dividend_yield_data, created = DividendYieldData.objects.update_or_create(
                        general=general,
                        defaults={
                            'yield_Y1': dividend_yields[0] if len(dividend_yields) > 0 else None,
                            'yield_Y2': dividend_yields[1] if len(dividend_yields) > 1 else None,
                            'yield_Y3': dividend_yields[2] if len(dividend_yields) > 2 else None,
                            'yield_Y4': dividend_yields[3] if len(dividend_yields) > 3 else None,
                            'yield_Y5': dividend_yields[4] if len(dividend_yields) > 4 else None,
                            'cagr_5_years': cagr_5_years
                        }
                    )
                    self.stdout.write(self.style.SUCCESS(f'Successfully calculated and stored dividend yield data for {general.name}'))
            except ValidationError as ve:
                self.stdout.write(self.style.ERROR(f"Validation error for {general.name}: {ve}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to process {general.name}: {e}"))
