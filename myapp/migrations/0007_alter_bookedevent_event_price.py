# Generated by Django 5.0 on 2024-03-21 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_bookedevent_num_people_alter_bookedevent_event_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookedevent',
            name='event_price',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]
