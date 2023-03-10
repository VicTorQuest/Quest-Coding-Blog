# Generated by Django 4.0.2 on 2022-11-07 20:30

import blog.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_comment_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(max_length=254, validators=[blog.validators.validate_email, blog.validators.restrict_vulger_words]),
        ),
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(max_length=25, validators=[blog.validators.validate_name, blog.validators.restrict_vulger_words]),
        ),
    ]
