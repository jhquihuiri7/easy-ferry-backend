# Generated by Django 5.2.3 on 2025-06-24 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0007_business_ferry'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='notes',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='sale',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
