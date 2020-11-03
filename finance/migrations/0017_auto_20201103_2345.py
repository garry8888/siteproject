# Generated by Django 3.0.5 on 2020-11-03 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0016_auto_20201103_2331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankstatements',
            name='type_place',
        ),
        migrations.AddField(
            model_name='bankstatements',
            name='type_expenses',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='finance.TypeExpenses'),
        ),
    ]
