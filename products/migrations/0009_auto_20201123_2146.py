# Generated by Django 3.1.3 on 2020-11-23 12:46

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20201103_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_digital',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='ProductFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\promo\\Desktop\\heroku\\media_root\\protected_media'), upload_to=products.models.upload_product_file_loc)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
