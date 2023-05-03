from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from mainapp.models import User
from django.utils.translation import gettext_lazy as _
from .validators import  validate_email, validate_name
from ckeditor_uploader.fields import RichTextUploadingField

domain_name = getattr(settings, 'DOMAIN_NAME', 'questcoding.blog')

#Managers
class CommentManager(models.Manager):
    #only comments
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    #both replies and comments
    def total(self):
        qs = super(CommentManager, self).filter(id__gte=1)
        return qs

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=15)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ("title",)
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})


class Author(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True)
    bio = models.TextField(max_length=100, null=True)
    location = models.CharField(max_length=30, null=True, help_text="your state, country")
    portifolio = models.URLField(null=True)
    github = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    avatar = models.ImageField(upload_to="profile_pics", blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug is None:
            self.slug = slugify(self.name)

        if self.avatar is None or self.avatar == "":
            self.avatar = self.user.avatar
        super(Author, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("author", kwargs={"slug": self.slug})
    




class Post(models.Model):
    ACTIVE = 'active'
    DRAFT = 'draft'

    CHOICES_STATUS = (
        (ACTIVE, 'Active'),
        (DRAFT, 'Draft')
    )
    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name='categories')
    title = models.CharField(max_length=150, blank=False, null=True)
    slug = models.SlugField(blank=False, null=True, unique=True)
    intro = models.TextField(null=True)
    post_img = models.ImageField(default="default.png", upload_to="post_images")
    content = RichTextUploadingField(null=True)
    likes = models.ManyToManyField(User,  related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField(User,  related_name='post_dislikes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=ACTIVE)

    def __str__(self):
        return self.title

    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})
    
    @property
    def get_post_url(self):
        return domain_name + reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug is None:
            newslug = slugify(self.title)
            self.slug = newslug
        super(Post, self).save(*args, **kwargs)

class FeaturedPost(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, blank=False, unique=True)
    github_link = models.URLField(null=True, blank=True)
    youtube_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.post.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=25, validators=[validate_name])
    email = models.EmailField(validators=[validate_email], max_length=254)
    body = models.TextField(max_length=700)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE, blank=True)

    objects = CommentManager()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return "{}: {}....".format(self.name, self.body[:25])

    def children(self):
        return Comment.objects.filter(parent=self).order_by('created_at')

    def get_absolute_url(self):
        return '/%s/#%s:%s' % (self.post.slug, self.email, self.created_at.strftime("%b-%d-%Y"))
    

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True