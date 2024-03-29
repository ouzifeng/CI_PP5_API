# Generated by Django 4.1.13 on 2024-02-13 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stockdata", "0019_rename_today_prices_close_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prices",
            name="close",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="prices",
            name="prev_close",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
    ]
