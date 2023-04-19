from django.urls import path
from .views import (
    cart,
    checkout,
    store,
    view_product,
    updateitem,
    processorder,
    getting_cart_total,
    getting_cart_items,
    getting_item_number,
    rating_product,
    show_productfiles,
    download_file,
    paid_items
)


urlpatterns = [
    path('store/', store, name='store'),
    path('store/<str:name>/', view_product, name='view_product'),
    path('getting_cart_total/', getting_cart_total, name='getting_cart_total'),
    path('getting_cart_items/', getting_cart_items, name='getting_cart_items'),
    path('getting_item_number/', getting_item_number, name='getting_item_number'),
    path('rate/', rating_product, name='rating_product'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('update-item/', updateitem, name='update_item'),
    path('process-order/', processorder, name='process_order'),
    path('show-files/', show_productfiles, name='show-files'),
    path('order-completed/<str:order_id>/', paid_items, name='order_complete'),
    path('download-files/<int:id>/<str:order_id>/', download_file, name='download_file'),
]
