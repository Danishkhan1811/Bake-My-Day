# Generated by Django 5.0.3 on 2024-03-25 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_usermodels_user_models_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user_models',
            table='custom_user_models',
        ),
    ]
