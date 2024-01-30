# Generated by Django 4.2 on 2024-01-23 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("stockdata", "0004_cashflow"),
    ]

    operations = [
        migrations.CreateModel(
            name="IncomeStatement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("filing_date", models.DateField()),
                (
                    "currency_symbol",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                (
                    "research_development",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "effect_of_accounting_charges",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "income_before_tax",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "minority_interest",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "net_income",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "selling_general_administrative",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "selling_and_marketing_expenses",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "gross_profit",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "reconciled_depreciation",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "ebit",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "ebitda",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "depreciation_and_amortization",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "non_operating_income_net_other",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "operating_income",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "other_operating_expenses",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "interest_expense",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "tax_provision",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "interest_income",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "net_interest_income",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "extraordinary_items",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "non_recurring",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "other_items",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "income_tax_expense",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "total_revenue",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "total_operating_expenses",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "cost_of_revenue",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "total_other_income_expense_net",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "discontinued_operations",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "net_income_from_continuing_ops",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "net_income_applicable_to_common_shares",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "preferred_stock_and_other_adjustments",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("yearly", "Yearly"), ("quarterly", "Quarterly")],
                        default="yearly",
                        max_length=10,
                    ),
                ),
                (
                    "general",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="income_statements",
                        to="stockdata.general",
                    ),
                ),
            ],
        ),
    ]
