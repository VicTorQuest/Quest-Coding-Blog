import uuid
import time
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from blog.models import Category, Post
from hitcount.models import HitCount
from .models import Customer, Order, OrderItem, Product, ShippingAddress, Review
from .utils import cookiecart, cartdata, guestorder

# Create your views here.
def store(request):

    categories = Category.objects.all()

    posts = Post.objects.filter(status=Post.ACTIVE)

    recent = list(posts)
    recent_posts = recent[:3]

    products = Product.objects.all()

    data = cartdata(request)
    cartitems = data['cartitems']

    response = render(request, 'store/store.html', {
        "categories": categories,
        'recent_posts': recent_posts,
        'products': products,
        'cartitems': cartitems
    })
   
    return response

def view_product(request, name):
    product = get_object_or_404(Product, name=name)
    
    data = cartdata(request)
    cartitems = data['cartitems']
    items = data['items']
    try:
        current_item = items.get(product=product)
    except:
        current_item = {'quantity': 0}

    categories = Category.objects.all()

    posts = Post.objects.filter(status=Post.ACTIVE)

    recent = list(posts)
    recent_posts = recent[:3]


    return render(request, 'store/view_product.html', {
        'current_item': current_item,
        'items': items,
        'cartitems': cartitems,
        'product': product,
        "categories": categories,
        'recent_posts': recent_posts,
    })

def getting_item_number(request):
    id = int(request.GET['product_id'])
    try:
        product = Product.objects.get(id=id)
        data = cartdata(request)
        items = data['items']
        item = items.get(product=product)
        product_quantity = item.quantity
    except:
        product_quantity= 0
    

    return JsonResponse({'quantity': product_quantity})


def getting_cart_total(request):
    data = cartdata(request)
    cartitems = data['cartitems']
    return JsonResponse({'cartitems': cartitems})
    

def getting_cart_items(request):
    data = cartdata(request)
    cartitems = data['cartitems']
    carttotal = data['carttotal']
    item = data['items']
    data = []
    for i in item:
        if request.user.is_authenticated:
            items = {
                'quantity': i.quantity,
                'get_total': i.get_total,
                'product': {'id': i.product.id, 'name': i.product.name, 'price': i.product.price, 'imageURL': i.product.imageURL}
            }
            data.append(items)
        else:
            items = {
                'quantity': i['quantity'],
                'get_total': i['get_total'],
                'product': {'id': i['product']['id'], 'name': i['product']['name'], 'price': i['product']['price'], 'imageURL': i['product']['imageURL']}
            }
            data.append(items)
    return JsonResponse({'cartitems': cartitems, 'carttotal':carttotal, 'items': data})

def rating_product(request):
    if request.method == 'POST':
        print(request.POST)
        rating = request.POST.get('rating')
        comment = request.POST.get('review')
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        review, created =  Review.objects.get_or_create(product=product, user=request.user)
        review.review = comment
        review.rating = rating
        review.save()
        
        
        # product.rated_by.add(request.user)
        # new_total_ratings = product.total_ratings + 1
        # product.total_ratings = new_total_ratings
        # new_combined_ratings = product.combined_ratings + int(rating)
        # product.combined_ratings = new_combined_ratings
        # product.rating = new_combined_ratings / new_total_ratings
        # product.save()
        time.sleep(1)
        return JsonResponse({'image': review.user.avatar.url, 'review': review.review, 'rating': review.rating, 'date': review.date.strftime('%b %d, %Y'), 'email': review.user.email})
    return JsonResponse({'success': 'false'})

def cart(request):
    
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

    context = {
        "posts": posts,
        'popular_posts': popular_posts,
        "categories": categories,
        'recent_posts': recent_posts,
        'items': items,
        'order': order,
        'cartitems': cartitems
    }
    
    return render(request, 'store/cart.html', context)



def checkout(request):
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
    try:
        billing_details = customer.shippingaddress_set.last()
    except:
        billing_details = None
    return render(request, 'store/checkout.html', {
        "posts": posts,
        'popular_posts': popular_posts,
        "categories": categories,
        'recent_posts': recent_posts,
        'items': items,
        'order': order,
        'cartitems': cartitems,
        'billing_details': billing_details
    })

@csrf_exempt
def updateitem(request):
    if request.method == 'POST':
        data = request.POST
        productId = data['productId']
        action = data['action']
        print('productId:', productId)
        print('action:', action)
        
        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        orderitem, created = OrderItem.objects.get_or_create(product=product, order=order)

        if action == 'add':
            orderitem.quantity = orderitem.quantity + 1
        elif action == 'remove':
            orderitem.quantity = orderitem.quantity - 1
        
        orderitem.save()
        if orderitem.quantity <= 0:
            orderitem.delete()
    return HttpResponse("Item was {} successfuly!!!!".format(action+'ed'))

def processorder(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transaction_id = str(uuid.uuid4()).replace('-', '')[:12]

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, completed=False)
            
            
            ShippingAddress.objects.create(customer = customer, order = order, address = data['shipping']['address'], country = data['shipping']['country'], state = data['shipping']['state'], city = data['shipping']['city'], zipcode = data['shipping']['zipcode'])
        else:
            customer, order = guestorder(request, data)

        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            order.completed = True
        order.save()
        ShippingAddress.objects.create(customer = customer, order = order, address = data['shipping']['address'], country = data['shipping']['country'], state = data['shipping']['state'], city = data['shipping']['city'], zipcode = data['shipping']['zipcode'])
    return JsonResponse('Payment complete!!', safe=False)