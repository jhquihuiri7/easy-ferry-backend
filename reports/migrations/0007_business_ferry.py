# Generated by Django 5.2.3 on 2025-06-17 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_alter_sale_intermediary'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='ferry',
            field=models.CharField(default='', max_length=255),
        ),
    ]
