# Generated by Django 3.0.5 on 2022-11-12 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('factory', '0009_bankstatementsdata_bank'),
        ('finance', '0023_bankstatements_bank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('short_name', models.CharField(max_length=20, null=True)),
                ('mcc_code', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='factory.Mcc')),
                ('type_expenses', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='finance.TypeExpenses')),
            ],
        ),
    ]
