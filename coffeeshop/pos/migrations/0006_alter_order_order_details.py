# Generated by Django 5.1.4 on 2025-01-09 21:53

import pos.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0005_order_alter_drink_drink_name_alter_size_size_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_details',
            field=models.JSONField(default=list, encoder=pos.models.CustomJSONEncoder),
        ),
    ]
