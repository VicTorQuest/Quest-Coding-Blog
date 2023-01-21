# Generated by Django 4.0.2 on 2022-11-05 21:30

import blog.validators
import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=15)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, validators=[blog.validators.restrict_vulger_words, blog.validators.validate_name])),
                ('email', models.EmailField(max_length=254, validators=[blog.validators.restrict_vulger_words, blog.validators.validate_email])),
                ('body', models.TextField(max_length=700, validators=[blog.validators.restrict_vulger_words])),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='FeaturedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('github_link', models.URLField()),
                ('youtube_link', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, null=True)),
                ('slug', models.SlugField(null=True, unique=True)),
                ('body', models.TextField(null=True)),
                ('post_img', models.ImageField(default='default.jpg', upload_to='post_images')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('draft', 'Draft')], default='active', max_length=10)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=35)),
                ('slug', models.SlugField(unique=True)),
                ('parent_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.category')),
            ],
            options={
                'verbose_name_plural': 'Sub-categories',
            },
        ),
    ]
