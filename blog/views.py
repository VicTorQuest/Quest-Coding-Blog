import random
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404, redirect
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from .forms import CommentForm
from .models import Post, FeaturedPost, Category, Comment, Author
from store.utils import cartdata
from .thread import SendThreadEmail
from hitcount.models import HitCount

from_this_email = getattr(settings, 'APPLICATION_EMAIL', "questcoding2001gmail.com")
# Create your views here.
def post_detail(request, slug):

    all_posts = Post.objects.filter(status=Post.ACTIVE)
    
    post = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)
    next_post = Post.objects.filter(status='active', id__gt=post.id).order_by("id").first()
    prev_post = Post.objects.filter(status='active', id__lt=post.id).first()
    
    recent = list(all_posts)
    recent_posts = recent[:3]

    categories = Category.objects.all()
        
    current_post_categories = list(post.category.all())
    related_posts = []
    for i in all_posts:
        for j in i.category.all():
            if j in current_post_categories:
                related_posts.append(i)
    related_posts = set(related_posts)
    
    if post in related_posts:
        related_posts.remove(post)
    
    posts = list(all_posts)
    if post in posts:
        posts.remove(post)
    try:
        posts = random.sample(posts, 3)
    except:
        posts
   
    current_link = request.build_absolute_uri()
    link = current_link + "#comments"

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    parent_obj = parent_qs.first()
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.user = request.user
                comment.email = request.user.email
            else:
                comment.user = None
            comment.parent = parent_obj
            comment.save()
            
            
            SendThreadEmail(comment, post, link).start()
            return redirect("post_detail", slug=slug)
    



    data = cartdata(request)
    cartitems = data['cartitems']

    context = {
        'post': post,
        'form': form,
        'posts': posts,
        'related_posts': related_posts,
        'categories': categories,
        'recent_posts': recent_posts,
        'next_post': next_post,
        'prev_post': prev_post,
        'cartitems': cartitems
    }
    hit_count = get_hitcount_model().objects.get_for_object(post)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits
    return render(request, 'blog/post_detail.html', context)

@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
        disliked = False
    else:
        post.dislikes.remove(request.user)
        post.likes.add(request.user)
        liked = True
        disliked = False
    
    return JsonResponse({'liked': liked, 'likes': post.likes.count(), 'disliked': disliked, 'dislikes': post.dislikes.count()})

@login_required
def dislike_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
        disliked = False
        liked = False
    else:
        post.likes.remove(request.user)
        post.dislikes.add(request.user)
        disliked = True
        liked = False
    return JsonResponse({'disliked': disliked, 'dislikes': post.dislikes.count(), 'liked': liked, 'likes': post.likes.count()})

def authors(request):
    authors  = Author.objects.all()
    all_posts = Post.objects.filter(status=Post.ACTIVE)
       
    recent = list(all_posts)
    recent_posts = recent[:3]
    
    categories = Category.objects.all()
        
    data = cartdata(request)
    cartitems = data['cartitems']
    return render(request, 'blog/authors.html', {
        'authors': authors,
        'category':category,
        'categories': categories,
        'recent_posts': recent_posts,
        'cartitems': cartitems
    })

def author(request, slug):
    author = get_object_or_404(Author, slug=slug)
    all_posts = Post.objects.filter(status=Post.ACTIVE)
    all_authors_posts = all_posts.filter(author=author)
    this_page = Paginator(all_authors_posts, 7)
    page = request.GET.get('page')
    posts = this_page.get_page(page)
    recent = list(all_posts)
    recent_posts = recent[:3]
    categories = Category.objects.all()
    data = cartdata(request)
    cartitems = data['cartitems']
    return render(request, 'blog/author.html', {
        'all_authors_posts': all_authors_posts,
        'posts': posts,
        'author': author,
        'category':category,
        'categories': categories,
        'recent_posts': recent_posts,
        'cartitems': cartitems
    })

def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    
    all_posts = Post.objects.filter(status=Post.ACTIVE)
       
    recent = list(all_posts)
    recent_posts = recent[:3]

    posts = category.categories.filter(status = Post.ACTIVE)
    
    categories = Category.objects.all()
        
    data = cartdata(request)
    cartitems = data['cartitems']
    return render(request, 'blog/category.html', {
        'category':category,
        'posts': posts,
        'categories': categories,
        'recent_posts': recent_posts,
        'cartitems': cartitems
    })


def search(request):
    all_posts = Post.objects.filter(status=Post.ACTIVE)
    
    recent = list(all_posts)
    recent_posts = recent[:3]
    query = request.GET.get('query', '')
    

    categories = Category.objects.all()

    posts = Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(intro__icontains=query) | Q(content__icontains=query) | Q(author__name__icontains=query))
    this_page = Paginator(posts, 4)
    page = request.GET.get("page")
    current_page = this_page.get_page(page)



    hitcount = HitCount.objects.order_by('-hits')[:3]
    popular_posts = []
    for i in hitcount:
        popular_posts.append(get_object_or_404(Post, pk=i.object_pk))
    return render(request, 'blog/search.html', {
        'posts': posts,
        'query': query,
        'categories': categories,
        'recent_posts': recent_posts,
        'current_page': current_page,
        'popular_posts': popular_posts
    })