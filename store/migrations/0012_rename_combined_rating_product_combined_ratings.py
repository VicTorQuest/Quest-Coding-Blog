# Generated by Django 4.0.2 on 2022-12-05 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_product_combined_rating_alter_product_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='combined_rating',
            new_name='combined_ratings',
        ),
    ]