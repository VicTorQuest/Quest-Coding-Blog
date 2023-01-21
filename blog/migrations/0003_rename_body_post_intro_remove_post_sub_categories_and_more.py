# Generated by Django 4.0.2 on 2022-11-06 02:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='body',
            new_name='intro',
        ),
        migrations.RemoveField(
            model_name='post',
            name='sub_categories',
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(related_name='categories', to='blog.Category'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_img',
            field=models.ImageField(default='default.png', upload_to='post_images'),
        ),
        migrations.DeleteModel(
            name='SubCategory',
        ),
    ]
