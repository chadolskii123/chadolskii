# Generated by Django 3.1.4 on 2020-12-18 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20201217_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=20),
        ),
    ]
