# Generated by Django 3.0.5 on 2020-10-27 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bankstatements',
            old_name='type_transaction_id',
            new_name='type_transaction',
        ),
    ]