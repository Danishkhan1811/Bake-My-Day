# Generated by Django 5.0.3 on 2024-04-16 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='product_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
