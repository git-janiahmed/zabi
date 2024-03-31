# Generated by Django 5.0 on 2024-03-24 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_bookedevent_amount_paid_bookedevent_attempt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookedevent',
            name='amount_due',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bookedevent',
            name='attempt',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]