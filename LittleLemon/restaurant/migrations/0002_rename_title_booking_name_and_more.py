# Generated by Django 4.1.6 on 2023-08-31 21:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='Title',
            new_name='Name',
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='Inventory',
            new_name='No_of_guests',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='No_of_guests',
            new_name='Inventory',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='Name',
            new_name='Title',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='price',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='Bookingdate',
        ),
        migrations.AddField(
            model_name='booking',
            name='Bookingdate',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='menu',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]