# Generated by Django 5.0.3 on 2024-04-16 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='assets/'),
        ),
    ]
