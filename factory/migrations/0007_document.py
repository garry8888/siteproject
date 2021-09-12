# Generated by Django 3.0.5 on 2021-09-12 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factory', '0006_auto_20210201_2106'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(upload_to='')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
