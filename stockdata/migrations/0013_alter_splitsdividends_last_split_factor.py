# Generated by Django 4.1.13 on 2024-02-09 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stockdata", "0012_alter_balancesheet_currency_symbol"),
    ]

    operations = [
        migrations.AlterField(
            model_name="splitsdividends",
            name="last_split_factor",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]