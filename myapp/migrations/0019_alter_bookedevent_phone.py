# Generated by Django 5.0 on 2024-03-28 09:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_alter_history_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookedevent',
            name='phone',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+919999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]