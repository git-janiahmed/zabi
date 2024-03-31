# Generated by Django 5.0 on 2024-03-23 08:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_alter_bookedevent_event_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookedevent',
            name='event_price',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bookedevent',
            name='num_people',
            field=models.PositiveIntegerField(default=1, help_text='|'),
        ),
        migrations.CreateModel(
            name='history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_date', models.DateField()),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('client_name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('num_people', models.PositiveIntegerField(default=1, help_text='|')),
                ('event_price', models.PositiveBigIntegerField(default=0)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.event')),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.timeslot')),
            ],
            options={
                'unique_together': {('event', 'event_date', 'slot')},
            },
        ),
        migrations.DeleteModel(
            name='BookedSlot',
        ),
    ]