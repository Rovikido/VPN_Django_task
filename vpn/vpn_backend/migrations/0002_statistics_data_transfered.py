# Generated by Django 4.2.7 on 2023-11-15 17:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpn_backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistics',
            name='data_transfered',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]