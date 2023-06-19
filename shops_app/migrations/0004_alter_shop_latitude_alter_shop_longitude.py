# Generated by Django 4.2.2 on 2023-06-19 16:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops_app', '0003_shop_city_shop_created_at_shop_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='latitude',
            field=models.FloatField(help_text='Latitude in decimal degrees', validators=[django.core.validators.MaxValueValidator(90), django.core.validators.MinValueValidator(-90)]),
        ),
        migrations.AlterField(
            model_name='shop',
            name='longitude',
            field=models.FloatField(help_text='Longitude in decimal degrees', validators=[django.core.validators.MaxValueValidator(180), django.core.validators.MinValueValidator(-180)]),
        ),
    ]
