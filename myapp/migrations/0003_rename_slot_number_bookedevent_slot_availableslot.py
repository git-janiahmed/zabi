# Generated by Django 5.0 on 2024-03-21 18:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_rename_eventbooking_bookedevent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookedevent',
            old_name='slot_number',
            new_name='slot',
        ),
        migrations.CreateModel(
            name='AvailableSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_date', models.DateField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.event')),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.timeslot')),
            ],
            options={
                'unique_together': {('event', 'event_date', 'slot')},
            },
        ),
    ]