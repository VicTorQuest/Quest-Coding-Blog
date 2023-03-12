from django.contrib import admin
from .models import *

# Register your models here.
class CustomerFormat(admin.ModelAdmin):
    search_fields = ['user__username', 'name', 'email', 'phone_number']
    list_display = ['user', 'name', 'email', 'phone_number']
    list_filter = ['user', 'name', 'email', 'phone_number']

class OrderFormat(admin.ModelAdmin):
    search_fields = ['customer__name', 'date_ordered', 'completed', 'order_id', 'transaction_id']
    list_display = ['customer', 'date_ordered', 'order_id', 'completed', 'transaction_id']
    list_filter = ['customer', 'date_ordered', 'order_id', 'completed', 'transaction_id']

class OrderItemFormat(admin.ModelAdmin):
    search_fields = ['product__name', 'quantity', 'order__order_id']
    list_display = ['product', 'quantity', 'order']
    list_filter = ['product', 'order']

class ProductReviewInline(admin.TabularInline):
    model = Review
    raw_id_fields = ['product']

class ProductFormat(admin.ModelAdmin):
    search_fields = ['name', 'digital']
    list_display = ['name', 'price', 'digital']
    list_filter = ['name', 'digital']
    inlines = [ProductReviewInline]

class ReviewFormat(admin.ModelAdmin):
    search_fields = ['user__username','product__name']
    list_display = ['user', 'product', 'rating', 'review']
    list_filter = ['product', 'rating']

class BillingAddressFormat(admin.ModelAdmin):
    search_fields = ['customer__name', 'order__order_id', 'address', 'country']
    list_display = ['customer', 'order', 'address', 'country']
    list_filter = ['customer', 'order', 'address', 'country']

class RefundFormat(admin.ModelAdmin):
    list_display = ['__str__', 'status', 'date']

class DownloadFormat(admin.ModelAdmin):
    search_fields = ['user__username', 'item', 'order__order_id']
    list_filter = ['user', 'item', 'order', 'date']
    list_display = ['user', 'item', 'order', 'date']
    

admin.site.register(Customer, CustomerFormat)
admin.site.register(Order, OrderFormat)
admin.site.register(OrderItem, OrderItemFormat)
admin.site.register(Product, ProductFormat)
admin.site.register(Review, ReviewFormat)
admin.site.register(BillingAddress, BillingAddressFormat)
admin.site.register(Refund, RefundFormat)
admin.site.register(Download, DownloadFormat)
