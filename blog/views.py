import random
import time
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core import serializers
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from store.utils import cartdata
from .forms import CommentForm, CreatePostForm
from .models import Post, Category, Comment, Author
from .permissions import BlogpostApiPermission
from .serializers import PostSerializer, CreatePostSerializer
from .thread import SendThreadEmail
from hitcount.models import HitCount
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.template.defaultfilters import register

from_this_email = getattr(settings, 'APPLICATION_EMAIL', "questcoding2001gmail.com")
domain_name = getattr(settings, 'DOMAIN_NAME', 'questcoding.blog')
User = get_user_model()
user = User.objects.get(username="Quest")
main_author = Author.objects.get(user=user)

@staff_member_required
def create_blog_post(request):
    all_posts = Post.objects.filter(status=Post.ACTIVE)
    recent = list(all_posts)
    recent_posts = recent[:3]
    categories = Category.objects.all()


    form = CreatePostForm()

    if request.method == 'POST':
        form = CreatePostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post was successfully uploaded')
            return redirect('create_blog_post')
        else:
            messages.success(request, 'Please fix the errors below')

    return render(request, 'blog/create_post.html', {
        'author': main_author,
        'categories': categories,
        'recent_posts': recent_posts,
        'form': form
    })


decorators = [login_required, staff_member_required]
@method_decorator(decorators, name='dispatch')
class CreateBlogPost(FormView):
    form_class = CreatePostForm
    template_name = "blog/create_post.html"
    success_url = 'create_blog_post'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_posts = Post.objects.filter(status=Post.ACTIVE)
        recent = list(all_posts)
        recent_posts = recent[:3]
        categories = Category.objects.all()
        context['author'] = main_author
        context['categories'] = categories
        context['recent_posts'] = recent_posts
        return context
    
    def form_invalid(self, form):
        response = super(CreateBlogPost, self).form_invalid(form)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(form.errors, status=400)
        else:
            return response

    
    def form_valid(self, form):
        response = super(CreateBlogPost, self).form_valid(form)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            newpost = form.save()
            post_url = domain_name + reverse('post_detail', kwargs={'slug': newpost.slug})
            return JsonResponse({'post_url': post_url})
        else:
            return response

@login_required
@staff_member_required
def create_post_api(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        author_id = int(request.POST.get('author'))
        author = Author.objects.get(id=author_id)
        category = request.POST.get('category').split()
        title = request.POST.get('title')
        intro = request.POST.get('intro')
        post_img = request.FILES.get('post_img')
        content = request.POST.get('content')
        
        categories = [int(num) for num in category[0].split(',')]
        
        newpost = Post.objects.create(author=author,  title=title, intro=intro, post_img=post_img, content=content)
        for i in categories:
            category = Category.objects.get(id=i)
            newpost.category.add(category)
        newpost.save()

        post_url = domain_name + reverse('post_detail', kwargs={'slug': newpost.slug})
        
    return JsonResponse({'message': 'Good', 'post_url': post_url})




class CreatePostApi(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = CreatePostSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [SessionAuthentication]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Get the created object from the response data
        created_object = response.data
        new_post = Post.objects.get(title=created_object['title'])
        post_url = domain_name + reverse('post_detail', kwargs={'slug': new_post.slug})
        # add the post url to the response
        extra_data = {'post_url': post_url}
        created_object.update(extra_data)
        return Response(created_object, status=response.status_code)




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

    related_posts = list(related_posts)
    def reducerelated(post_list):
        if len(post_list) <= 5:
            return post_list
        else:
            post_list.pop()

            return reducerelated(post_list)

    final_related_posts = reducerelated(related_posts) 
    
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
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, 'You must pass the reCAPTCHA ')
                    continue
                messages.error(request, error)



    data = cartdata(request)
    cartitems = data['cartitems']

    context = {
        'post': post,
        'form': form,
        'posts': posts,
        'related_posts': final_related_posts,
        'categories': categories,
        'recent_posts': recent_posts,
        'next_post': next_post,
        'prev_post': prev_post,
        'cartitems': cartitems,
        'author': main_author
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
        'cartitems': cartitems,
        'author': main_author
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
        'cartitems': cartitems,
        'author': main_author
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
        'cartitems': cartitems,
        'author': main_author
    })


class blogposts(ListAPIView):
    queryset = Post.objects.filter(status=Post.ACTIVE)
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [BlogpostApiPermission]

def testapi(request):
    all_posts = Post.objects.filter(status=Post.ACTIVE)
    categories = Category.objects.all()
    recent = list(all_posts)
    recent_posts = recent[:3]
    return render(request, 'test_api.html', {
        'author': main_author,
        'categories': categories,
        'recent_posts': recent_posts,
    })
    



def search(request):
    q = request.GET.get('query', '')
    if q != "" or None:
        vector = SearchVector('title', weight='A') + \
            SearchVector('intro', weight='B') + \
                SearchVector('content', weight='C') + \
                    SearchVector('author__name', weight='D') 
        # vector = SearchVector('title', 'intro', 'content', 'author__name')
        query = SearchQuery(q)
        # posts = Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(intro__icontains=query) | Q(content__icontains=query) | Q(author__name__icontains=query))
        posts = Post.objects.annotate(rank=SearchRank(vector, query, cover_density=True)).filter(rank__gte=0.001).order_by('-rank').filter(status=Post.ACTIVE)
        # posts = Post.objects.annotate(search=vector).filter(search=query)
    else:
        posts = []    
        
    all_posts = Post.objects.filter(status=Post.ACTIVE)
    categories = Category.objects.all()
    
    recent = list(all_posts)
    recent_posts = recent[:3]   
    this_page = Paginator(posts, 4)
    page = request.GET.get("page")
    current_page = this_page.get_page(page)


    hitcount = HitCount.objects.order_by('-hits')[:3]
    popular_posts = []
    for i in hitcount:
        popular_posts.append(get_object_or_404(Post, pk=i.object_pk))
    return render(request, 'blog/search.html', {
        'posts': posts,
        'query': q,
        'categories': categories,
        'recent_posts': recent_posts,
        'current_page': current_page,
        'popular_posts': popular_posts,
        'author': main_author
    })


def search_query(request):
    q = request.GET.get('query', '')
    if q != "" or None:
        vector = SearchVector('title', weight='A') + \
            SearchVector('intro', weight='B') + \
                SearchVector('content', weight='C') + \
                    SearchVector('author__name', weight='D') 
        query = SearchQuery(q)
        posts = Post.objects.annotate(rank=SearchRank(vector, query, cover_density=True)).filter(rank__gte=0.001).order_by('-rank').filter(status=Post.ACTIVE).explain(analyze=True)
        print(posts)
        post_data = []
        # for post in posts:
        #     item = {
        #         'title': post.title,
        #         'author': post.author.name,
        #         'author_url': post.author.get_absolute_url(),
        #         'author_img': post.author.avatar.url,
        #         'category': [i.title for i in post.category.all()],
        #         'category_url': [i.get_absolute_url() for i in post.category.all()],
        #         'intro': post.intro,
        #         'post_img': post.post_img.url,
        #         'post_url': post.get_absolute_url(),
        #         'date': post.created_at.date().strftime('%b  %d, %Y'),
        #         'total_comments': Comment.objects.total().filter(post=post).count(),
        #         'hitcount': get_hitcount_model().objects.get_for_object(post).hits
        #     }
        #     post_data.append(item)
        return JsonResponse({'posts': post_data, 'query': q})
    else:
        return JsonResponse({'query': q})
