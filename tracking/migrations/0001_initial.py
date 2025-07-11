# Generated by Django 5.2.3 on 2025-06-17 20:38

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reports', '0007_business_ferry'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinates',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lat', models.FloatField()),
                ('long', models.FloatField()),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coordinates', to='reports.business')),
            ],
            options={
                'db_table': 'coordinates',
                'managed': True,
            },
        ),
    ]
