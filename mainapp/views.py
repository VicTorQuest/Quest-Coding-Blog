import json
import re
import time
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.template.loader import get_template
from django.views.generic import CreateView
from .forms import EditAccount, EditBillingAddress, EditCustomer
from blog.models import Post, Category, FeaturedPost, Author
from mainapp.models import User
from newsletter.models import Subscriber
from newsletter.thread import EmailThreading
from store.models import BillingAddress, Customer, Refund, Order, Download
from store.forms import RefundForm
from store.utils import cartdata
from hitcount.models import HitCount
from maintenance_mode.core import get_maintenance_mode, set_maintenance_mode

domain_name = getattr(settings, 'DOMAIN_NAME', 'questcoding.blog')
site_email = getattr(settings, 'APPLICATION_EMAIL', "admin@questcoding.blog")
user = User.objects.filter(username="Quest").first()
author = Author.objects.get(user=user)
# Create your views here.
def home(request):
  
    categories = Category.objects.all()
    posts = Post.objects.filter(status=Post.ACTIVE)

    hitcount = HitCount.objects.order_by('-hits')[:3]
    popular_posts = []
    for i in hitcount:
        popular_posts.append(get_object_or_404(Post, pk=i.object_pk))

    recent = list(posts)
    recent_posts = recent[:3]


    featured_post = FeaturedPost.objects.all()



    #setting up pagination

  
    this_page = Paginator(posts, 4)
    page = request.GET.get("page")
    current_page = this_page.get_page(page)

    data = cartdata(request)
    cartitems = data['cartitems']
    carttotal = data['cartitems']

    user = User.objects.filter(username="Quest").first()
    author = Author.objects.get(user=user)
    return  render(request,'home.html', {
        "posts": posts,
        'popular_posts': popular_posts,
        'current_page': current_page,
        "categories": categories,
        'recent_posts': recent_posts,
        'featured_post': featured_post,
        'cartitems': cartitems,
        'author': author,
        "carttotal": carttotal
    })


def account(request):
    categories = Category.objects.all()
    
    posts = Post.objects.filter(status=Post.ACTIVE)
        
    
    hitcount = HitCount.objects.order_by('-hits')[:3]
    popular_posts = []
    for i in hitcount:
        popular_posts.append(get_object_or_404(Post, pk=i.object_pk))
    recent = list(posts)
    recent_posts = recent[:3]

    if request.method == 'POST':
        if request.POST.get('form_type') == 'register':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            if User.objects.filter(username=username).exists():
                messages.error(request, 'An account is already registered with this username. Please log in.')
                return redirect('my_account')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'An account is already registered with this email address. Please log in.')
                return redirect('my_account')
            
       
            subscriber = request.POST.get('subscribing')
            if subscriber:
                if Subscriber.objects.filter(email=email).exists():
                    edit_preference_email = ''
                    unsubscribe_email = email
                    pass
                else:
                    Subscriber.objects.create(email=email, first_name="", last_name="")
                    edit_preference_email = email
                    unsubscribe_email = ''

            User.objects.create_user(username=username, email=email, password=password)

            html_template_path = "welcome_email.html"
            context_data = {'username': username, 'my_account': domain_name + reverse('my_account')}
            email_html_template = get_template(html_template_path).render(context_data)
            receiver_email = email
            email_msg = EmailMessage("Your account has been created", email_html_template, site_email, [receiver_email], reply_to=[site_email])
            email_msg.content_subtype = 'html'
            EmailThreading(email=email_msg).start()


            messages.success(request, '{}, Your account was created successfully'.format(username))
            return redirect('my_account')
        elif request.POST.get('form_type') == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')
            isanemail = re.match("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", username)
            if isanemail:
                try:
                    userobj = User.objects.get(email=username)
                except:
                    messages.error(request, "Unknown email address. Check again or try your username.")
                    return redirect("my_account")

                
                if userobj:
                    objusername = userobj.username
                    user = authenticate(request, username=objusername, password=password)
                    if user != None:
                        login(request, user)
                        return redirect('my_account')
                    else:
                        messages.error(request, "The password you entered for the email '{}' is incorrect".format(username))
                        return redirect('my_account')

                else:
                    messages.error(request, "Unknown email address. Check again or try your username.")
                    return redirect("my_account")
            else:
                if User.objects.filter(username=username).exists() == False:
                    messages.error(request, "The username '{}' is not registered on this site. If you are unsure of your username, try your email address instead.".format(username))
                    return redirect("my_account")

                user = authenticate(request, username=username, password=password)
                if user != None:
                    login(request, user)
                    return redirect('my_account')
                else:
                    messages.error(request, "The password you entered for the username '{}' is incorrect".format(username))

    data = cartdata(request)
    cartitems = data['cartitems']      
    return render(request, 'account.html', {
        "posts": posts,
        'popular_posts': popular_posts,
        "categories": categories,
        'recent_posts': recent_posts,
        'cartitems': cartitems,
        'author': author
    })

@login_required
def edit_account(request):
    categories = Category.objects.all()
    posts = Post.objects.filter(status=Post.ACTIVE)

    hitcount = HitCount.objects.order_by('-hits')[:3]
    popular_posts = []
    for i in hitcount:
        popular_posts.append(get_object_or_404(Post, pk=i.object_pk))
    
    recent = list(posts)
    recent_posts = recent[:3]


    form = EditAccount(instance = request.user)

    
    if request.method == "POST":
        form = EditAccount(request.POST or None, instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Profile updated succesfully')
            return redirect('edit_account')
        else:
            messages.error(request, "Profile update failed, please rectify your error")
   
    data = cartdata(request)
    cartitems = data['cartitems']
    return render(request, 'edit_account.html', {
        "posts": posts,
        'popular_posts': popular_posts,
        "categories": categories,
        'recent_posts': recent_posts,
        'form': form,
        'cartitems': cartitems,
        'author': author
    })


@login_required
def address(request):
    categories = Category.objects.all()
   
    posts = Post.objects.filter(status=Post.ACTIVE)
    
    hitcount = HitCount.objects.order_by('-hits')[:3]
    popular_posts = []
    for i in hitcount:
        popular_posts.append(get_object_or_404(Post, pk=i.object_pk))
    
    recent = list(posts)
    recent_posts = recent[:3]

    data = cartdata(request)
    cartitems = data['cartitems']
    order = data['order']
    items = data['items']
    customer = data['customer']

    customer_form = EditCustomer(instance = customer)

    billing_obj, created = BillingAddress.objects.get_or_create(customer = customer, id=customer.id)
    billing_form = EditBillingAddress(instance = billing_obj)

    
    if request.method == "POST":
        customer_form = EditCustomer(request.POST or None, instance = customer)
        billing_form = EditBillingAddress(request.POST or None, instance = billing_obj)
        if customer_form.is_valid() and billing_form.is_valid():
            customer_form.save()
            billing_form.save()
            messages.success(request, f'Address updated succesfully')
            return redirect('address')
        else:
            messages.error(request, "Address update failed, please rectify your error")
   

    data = cartdata(request)
    cartitems = data['cartitems']
    return render(request, 'address.html', {
        "posts": posts,
        'popular_posts': popular_posts,
        "categories": categories,
        'recent_posts': recent_posts,
        'items': items,
        'order': order,
        'cartitems': cartitems,
        'customer_form': customer_form,
        'billing_form': billing_form,
        'cartitems': cartitems,
        'author': author
    })


@login_required
def recent_order(request):
    categories = Category.objects.all()
        
    posts = Post.objects.filter(status=Post.ACTIVE)
 
    
    recent = list(posts)
    recent_posts = recent[:3]

    data = cartdata(request)
    cartitems = data['cartitems']
    order = data['order']
    items = data['items']
    return render(request, 'orders.html', {
        "posts": posts,
        "categories": categories,
        'recent_posts': recent_posts,
        'items': items,
        'order': order,
        'cartitems': cartitems,
        'author': author
    })


class RequestRefund(CreateView):
    model = Refund
    form_class = RefundForm
    template_name = 'request_refund.html'
    success_url = reverse_lazy('request_refund')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(status=Post.ACTIVE)
        recent = list(posts)
        data = cartdata(self.request)
        cartitems = data['cartitems']
        try:
            refund = Refund.objects.get(user=self.request.user)
        except Refund.DoesNotExist:
            refund = None
        customer = Customer.objects.get(user = self.request.user)
        completed_order =Order.objects.filter(customer=customer, completed=True).first()
        context["categories"] = Category.objects.all()
        context["posts"] = posts
        context["recent_posts"] = recent[:3]
        context["data"] = data
        context["cartitems"] = cartitems
        context["refund"] = refund
        context["completed_order"] = completed_order
        context['author'] = author
        return context

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(RequestRefund, self).get_form_kwargs()
        customer = Customer.objects.get(user = self.request.user)
        kwargs['request'] = self.request
        kwargs['order_queryset'] = Order.objects.filter(customer=customer, completed=True).first()
        return kwargs

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        items = form.cleaned_data.get('items')
        form.instance.user = self.request.user
        email_msg = EmailMessage(subject="New refund request from {}".format(self.request.user), body="{} is requesting refund for these items: {}".format(self.request.user.email, *[i.product for i in items]), from_email=self.request.user.email, to=[site_email], reply_to=[self.request.user.email])
        EmailThreading(email_msg).start()
        messages.success(request=self.request, message="Warranty request sent, We'll get back to you soon")
        return super().form_valid(form)


@login_required
def logout_page(request):
    logout(request)
    return redirect("my_account")


def contact(request):
    categories = Category.objects.all()
    posts = Post.objects.filter(status=Post.ACTIVE)
    
    hitcount = HitCount.objects.order_by('-hits')[:3]
    popular_posts = []
    for i in hitcount:
        popular_posts.append(get_object_or_404(Post, pk=i.object_pk))
    recent = list(posts)
    recent_posts = recent[:3]

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        email_msg = EmailMessage(subject='{}({}): {}'.format(name, email, subject), body=message, from_email=email, to=[site_email], reply_to=[email])
        email_msg.content_subtype = 'html'
        EmailThreading(email_msg).start()
        messages.success(request, "Your email was sent successfully.")
        redirect('contact')
    return render(request, 'contact.html', {
        "posts": posts,
        'popular_posts': popular_posts,
        "categories": categories,
        'recent_posts': recent_posts,
        'author': author
    })

def terms(request):
    categories = Category.objects.all()
    posts = Post.objects.filter(status=Post.ACTIVE)
    recent = list(posts)
    recent_posts = recent[:3]
    return render(request, 'terms.html', {
        "posts": posts,
        "categories": categories,
        'recent_posts': recent_posts,
        'author': author
    })

def refund_policy(request):
    categories = Category.objects.all()
    posts = Post.objects.filter(status=Post.ACTIVE)
    
    hitcount = HitCount.objects.order_by('-hits')[:3]
    popular_posts = []
    for i in hitcount:
        popular_posts.append(get_object_or_404(Post, pk=i.object_pk))
    recent = list(posts)
    recent_posts = recent[:3]
    return render(request, 'refund.html', {
        "posts": posts,
        'popular_posts': popular_posts,
        "categories": categories,
        'recent_posts': recent_posts,
        'author': author
    })


def privacy_policy(request):
    categories = Category.objects.all()

    posts = Post.objects.filter(status=Post.ACTIVE)
    
    
 
    hitcount = HitCount.objects.order_by('-hits')[:3]
    popular_posts = []
    for i in hitcount:
        popular_posts.append(get_object_or_404(Post, pk=i.object_pk))
    recent = list(posts)
    recent_posts = recent[:3]
    return render(request, 'privacy.html', {
        "posts": posts,
        'popular_posts': popular_posts,
        "categories": categories,
        'recent_posts': recent_posts,
        'author': author
    })

@login_required
def downloads(request):
    categories = Category.objects.all()
    posts = Post.objects.filter(status=Post.ACTIVE)
    hitcount = HitCount.objects.order_by('-hits')[:3]
    popular_posts = []
    for i in hitcount:
        popular_posts.append(get_object_or_404(Post, pk=i.object_pk))
    recent = list(posts)
    recent_posts = recent[:3]
    all_downloads = Download.objects.filter(user=request.user)
    return render(request, 'downloads.html', {
        "posts": posts,
        'popular_posts': popular_posts,
        "categories": categories,
        'recent_posts': recent_posts,
        'author': author,
        "downloads": all_downloads
    })

def videos(request):
    categories = Category.objects.all()
    posts = Post.objects.filter(status=Post.ACTIVE)

    hitcount = HitCount.objects.order_by('-hits')[:3]
    popular_posts = []
    for i in hitcount:
        popular_posts.append(get_object_or_404(Post, pk=i.object_pk))
    recent = list(posts)
    recent_posts = recent[:3]
    return render(request, 'videos.html', {
        "posts": posts,
        'popular_posts': popular_posts,
        "categories": categories,
        'recent_posts': recent_posts,
        'author': author
    })

@staff_member_required
def toggle_maintenance(request):
    return render(request, 'toggle_maintenance.html')

@staff_member_required
def maintenance_switch(request):
    mode = json.loads(request.POST.get('mode')) 
    set_maintenance_mode(mode)
  
    if get_maintenance_mode():
        current_mode = 'On'
        message = 'Maintenance mode has been turned on'
    else:
        current_mode = 'Off'
        message = 'Maintenance mode has been turned off'
    time.sleep(1.5)
    return JsonResponse({'mode': current_mode, 'message': message})

def robots_txt(request):
    text = [
        "User-agent: *",
        "Disallow: /admin/",
    ]

    return HttpResponse("\n".join(text), content_type="text/plain")


def customhandler404(request, exception):
    categories = Category.objects.all()

    
    posts = Post.objects.filter(status=Post.ACTIVE)
       
    
    
    recent = list(posts)
    recent_posts = recent[:3]
    return render(request, '404.html', {
        'categories': categories,
        'recent_posts': recent_posts,
        'author': author
    })

def customhandler403(request, exception=None):
    categories = Category.objects.all()
    posts = Post.objects.filter(status=Post.ACTIVE)
    recent = list(posts)
    recent_posts = recent[:3]
    return render(request, '403.html', {
        'categories': categories,
        'recent_posts': recent_posts,
        'author': author
    })

def customhandler500(request):
    categories = Category.objects.all()
    posts = Post.objects.filter(status=Post.ACTIVE)

    recent = list(posts)
    recent_posts = recent[:3]
    return render(request, '500.html', {
        'categories': categories,
        'recent_posts': recent_posts,
        'author': author
    })