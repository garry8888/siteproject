# Generated by Django 3.0.5 on 2020-11-01 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0012_auto_20201101_0151'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneytransaction',
            name='type_transaction_ru',
            field=models.CharField(max_length=50, null=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='places',
            name='type_place_ru',
            field=models.CharField(max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='typeexpenses',
            name='type_expenses_ru',
            field=models.CharField(max_length=100, null=True),
            preserve_default=False,
        ),
    ]
