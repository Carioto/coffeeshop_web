# Generated by Django 5.1.4 on 2024-12-28 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drink',
            name='drink_cost',
        ),
        migrations.AddField(
            model_name='drink',
            name='drink_cost_12oz',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='drink',
            name='drink_cost_16oz',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='drink',
            name='drink_cost_20oz',
            field=models.FloatField(default=0.0),
        ),
    ]
