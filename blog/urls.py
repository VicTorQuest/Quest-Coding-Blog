from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import CreateBlogPost, create_blog_post, CreatePostApi, create_post_api, post_detail, like_post,dislike_post, category, search, authors, author, blogposts, testapi, search_query
from django.contrib.admin.views.decorators import staff_member_required


urlpatterns = [
    path('create-blog-post/', create_blog_post, name='create_blog_post'),
    path('create-post-api/', CreatePostApi.as_view(), name='create_post_api'),
    path('search/', search, name='search'),
    path('search-query/', search_query, name='search_query'),
    path('<slug:slug>/', post_detail,name='post_detail'),
    path('blogposts/api/', blogposts.as_view() ,name='blogposts'),
    path('blogposts/token/', obtain_auth_token, name='blogposts_token'),
    path('blogposts/test-api/', testapi, name='test_blogapi'),
    path('like-post/<slug:slug>/', like_post, name='like_post'),
    path('dislike-post/<slug:slug>/', dislike_post, name='dislike_post'),
    path('authors', authors, name='authors'),
    path('author/<slug:slug>/', author, name="author"),
    path('category/<slug:slug>/', category, name='category')
]
