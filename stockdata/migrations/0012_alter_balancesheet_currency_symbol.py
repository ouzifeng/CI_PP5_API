# Generated by Django 4.1.13 on 2024-02-09 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stockdata", "0011_general_uid_alter_general_primary_ticker"),
    ]

    operations = [
        migrations.AlterField(
            model_name="balancesheet",
            name="currency_symbol",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
