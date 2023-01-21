from django.contrib import admin
from blog.models import Category, Author, Post, FeaturedPost, Comment
from blog.forms import PostForm

# Register your models here.
class CommentItemInline(admin.TabularInline):
    model = Comment
    raw_id_fields = ['post']

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title']
    prepopulated_fields = {'slug': ['title']}

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'portifolio']
    search_fields = ['name', 'user__username']
    prepopulated_fields = {'slug': ['name']}

class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'body']
    list_display = ['title', 'author', 'created_at', 'slug', 'status',]
    list_filter = ['title', 'category', 'created_at', 'status']
    prepopulated_fields = {'slug': ['title']}

    inlines = [CommentItemInline]
    form = PostForm

class FeaturedPostAdmin(admin.ModelAdmin):
    list_display = ['post', 'github_link', 'youtube_link']

class CommentAdmin(admin.ModelAdmin):
    search_fields = ["name", "email", "body"]
    list_display = ['__str__', 'post', 'created_at']
    list_filter = ['name', 'email', 'post', 'created_at']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(FeaturedPost, FeaturedPostAdmin)
admin.site.register(Comment, CommentAdmin)
