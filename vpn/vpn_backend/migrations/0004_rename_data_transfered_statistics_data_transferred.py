# Generated by Django 4.2.7 on 2023-11-15 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vpn_backend', '0003_alter_statistics_user_alter_website_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statistics',
            old_name='data_transfered',
            new_name='data_transferred',
        ),
    ]