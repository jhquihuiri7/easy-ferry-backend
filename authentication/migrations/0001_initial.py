# Generated by Django 5.2.3 on 2025-07-07 13:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reports', '0018_remove_owner_business_delete_crew_delete_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crew',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('crew_capacity', models.PositiveIntegerField(default=0)),
                ('passenger_capacity', models.PositiveIntegerField(default=0)),
                ('responsible_name', models.CharField(default='', max_length=100)),
                ('responsible_passport', models.CharField(default='', max_length=20)),
                ('responsible_phone', models.CharField(default='', max_length=15)),
                ('captain_name', models.CharField(default='', max_length=100)),
                ('captain_password', models.CharField(default='', max_length=20)),
                ('sailor1_name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('sailor1_passport', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('sailor2_name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('sailor2_passport', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.business')),
            ],
            options={
                'db_table': 'crew',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100)),
                ('ruc', models.CharField(default='', max_length=13)),
                ('phone', models.CharField(default='', max_length=15)),
                ('email', models.EmailField(default='', max_length=254)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.business')),
            ],
            options={
                'db_table': 'owner',
            },
        ),
    ]
