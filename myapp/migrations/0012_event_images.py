# Generated by Django 5.0 on 2024-03-25 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_eventimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='images',
            field=models.ManyToManyField(related_name='items', to='myapp.eventimages'),
        ),
    ]