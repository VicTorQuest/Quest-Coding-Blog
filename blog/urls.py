from django.urls import path
from .views import post_detail, like_post,dislike_post, category, search, authors, author, blogposts



urlpatterns = [
    path('search/', search, name='search'),
    path('<slug:slug>/', post_detail,name='post_detail'),
    path('like-post/<slug:slug>/', like_post, name='like_post'),
    path('dislike-post/<slug:slug>/', dislike_post, name='dislike_post'),
    path('authors', authors, name='authors'),
    path('author/<slug:slug>/', author, name="author"),
    path('category/<slug:slug>/', category, name='category')
]
