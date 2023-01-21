from django.contrib.sitemaps import Sitemap
from .models import Category, Post, Comment, Author


class CategorySitemaps(Sitemap):
    priority = 0.9
    protocol = 'https'
    def items(self):
        return Category.objects.all()

class PostSitemaps(Sitemap):
    priority = 1.0
    protocol = 'https'
    def items(self):
        return Post.objects.filter(status=Post.ACTIVE)

    def lastmod(self, obj):
        return obj.last_modified

class AuthorSitemaps(Sitemap):
    priority = 0.6
    protocol = 'https'
    def items(self):
        return Author.objects.all()

    


class  CommentSiteMaps(Sitemap):
    priority = 0.8
    protocol = 'https'
    def items(self):
        return Comment.objects.total()
    
    def lastmod(self, obj):
        return obj.created_at