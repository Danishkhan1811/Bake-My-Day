# Generated by Django 5.0.3 on 2024-04-21 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_orders_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
    ]
