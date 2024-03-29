# Generated by Django 4.1.13 on 2024-02-11 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stockdata", "0015_general_logo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="general",
            name="country_iso",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="general",
            name="currency_code",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="general",
            name="currency_symbol",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="general",
            name="primary_ticker",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="general",
            name="uid",
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
