# Generated by Django 3.0.5 on 2020-10-29 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_auto_20201029_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='abbreviation',
            field=models.CharField(max_length=50),
        ),
    ]
