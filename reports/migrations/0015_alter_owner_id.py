# Generated by Django 5.2.3 on 2025-07-04 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0014_crew'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
