# Generated by Django 4.0.2 on 2023-03-08 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_alter_product_rated_by'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShippingAddress',
            new_name='BillingAddress',
        ),
        migrations.AlterModelOptions(
            name='billingaddress',
            options={'verbose_name_plural': 'Billing addresses'},
        ),
    ]