import json
import uuid
from .models import Product, Order, Customer, BillingAddress, OrderItem

def cookiecart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
        order_id = cart['order_id']
    except:     
        cart = {'items': {},}
        order_id = ""
    items = []
    order = {'get_cart_items': 0, 'get_cart_total': 0, 'order_id': order_id} 
    cartitems = order['get_cart_items']
    carttotal = order['get_cart_total']

    for i in cart['items']:
        try:
            cartitems += cart['items'][i]['quantity']

            product = Product.objects.get(id=i)

            total = (product.price * cart['items'][i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart['items'][i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart["items"][i]['quantity'], 
                'get_total': total,
            }
            items.append(item)

        except Exception as exc:
            raise
    return {'cartitems': cartitems, 'carttotal': carttotal, 'order': order, 'items': items}

def cartdata(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
        carttotal = order.get_cart_total
    else:
        cookie_data = cookiecart(request)
        cartitems = cookie_data['cartitems']
        order = cookie_data['order']
        carttotal = order['get_cart_total'] 
        items = cookie_data['items']
        customer = None
    return {'cartitems': cartitems, 'order': order, 'items': items, 'customer': customer, 'carttotal': carttotal}

def guestorder(request, data):
    name = "{} {}".format(data['form']['first_name'], data['form']['last_name'])
    email = data['form']['email']
    cookiedata = cookiecart(request)
    items = cookiedata['items']
    customer, created = Customer.objects.get_or_create(email=email, )
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, completed=False)

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderitem = OrderItem.objects.create(product=product, order=order, quantity=item['quantity'])

    return customer, order