# Generated by Django 5.0 on 2024-03-21 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_rename_availableslot_bookedslot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='price',
            field=models.PositiveIntegerField(),
        ),
    ]
