# Generated by Django 5.0.3 on 2024-04-21 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_orders_is_complete'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cake_flavor', models.CharField(max_length=100)),
                ('filling', models.CharField(blank=True, max_length=100, null=True)),
                ('frosting', models.CharField(max_length=100)),
                ('decoration_style', models.CharField(max_length=100)),
                ('color_scheme', models.CharField(max_length=100)),
                ('message_on_cake', models.CharField(max_length=100)),
                ('dietary_restrictions', models.CharField(blank=True, max_length=100, null=True)),
                ('special_instructions', models.TextField()),
                ('name', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
            ],
        ),
    ]
