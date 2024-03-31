# Generated by Django 5.0 on 2024-03-27 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_alter_bookedevent_amount_due_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='amount_due',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='history',
            name='amount_paid',
            field=models.PositiveBigIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='history',
            name='attempt',
            field=models.PositiveBigIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='history',
            name='created_at',
            field=models.PositiveBigIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='history',
            name='razor_id',
            field=models.CharField(blank=True, default=0, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='history',
            name='status',
            field=models.CharField(blank=True, default=0, max_length=100, null=True),
        ),
    ]