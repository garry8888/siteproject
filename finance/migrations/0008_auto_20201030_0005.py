# Generated by Django 3.0.5 on 2020-10-29 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0007_auto_20201029_2259'),
    ]

    operations = [
        migrations.RenameField(
            model_name='countries',
            old_name='index',
            new_name='index_c',
        ),
    ]