# Generated by Django 4.0.2 on 2022-12-05 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_rename_combined_rating_product_combined_ratings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='combined_ratings',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=1000),
        ),
    ]
