# Generated by Django 5.0 on 2024-03-21 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EventBooking',
            new_name='BookedEvent',
        ),
    ]
