# Generated by Django 4.1.13 on 2024-02-09 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("stockdata", "0009_dividendyielddata"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="general",
            name="logo_url",
        ),
    ]
