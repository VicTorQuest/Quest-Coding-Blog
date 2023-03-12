import random
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from mainapp.models import User
from django_countries.fields import CountryField



def generate_order_id():
    number = str(random.randint(0, 10))
    code = str(uuid.uuid4()).replace('-', number)
    code_exists = Order.objects.filter(order_id=code).exists()
    if code_exists:
        generate_order_id()
    return code
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=15, null=True)

    def __str__(self):
        if self.name == None:
            return self.user.username
        else:
            return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    file = models.FileField(upload_to="files", null=True)
    image = models.ImageField(default='placeholder.png', upload_to='product_images', blank=True, null=True)
    digital = models.BooleanField(default=True, null=True)
    rating = models.DecimalField(default=0, validators=[MaxValueValidator(5.0), MinValueValidator(0.0)], decimal_places=1, max_digits=2)
    rated_by = models.ManyToManyField(User, blank=True)
    combined_ratings = models.DecimalField(default=0, decimal_places=1, max_digits=1000)
    total_ratings = models.IntegerField(default=0, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def get_absolute_url(self):
        return reverse("view_product", kwargs={'name': self.name})
    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    review = models.TextField(null=True)
    rating = models.DecimalField(default=0, validators=[MaxValueValidator(5.0), MinValueValidator(0.0)], decimal_places=1, max_digits=2, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} > {} - {} stars".format(self.user, self.product, self.rating)




class Order(models.Model):
    customer = models.ForeignKey(Customer, models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    order_id = models.CharField(max_length=200, default='', unique=True, blank=True , null=True)
    transaction_id = models.CharField(max_length=200, unique=True, blank=True , null=True)

    def __str__(self):
        return "{}".format(self.order_id)
    

    def save(self, *args, **kwargs):
        if self.order_id == '' or None:
            code = generate_order_id()
            self.order_id = code
        super(Order, self).save(*args, **kwargs)



    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, models.SET_NULL, null=True)
    order = models.ForeignKey(Order, models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - x{}".format(self.product, self.quantity)
        

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class BillingAddress(models.Model):
    customer = models.ForeignKey(Customer, models.SET_NULL, null=True)
    order = models.ForeignKey(Order, models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True)
    country = CountryField(null=True, blank_label="Select country")
    state = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Billing addresses'

    def __str__(self):
        return "{}".format(self.address)

REFUND_STATUS = (
    ("Accepted", "Accepted"),
    ("Rejected", "Rejected"),
    ("Sent", "Sent")
)

class Refund(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    order_id = models.CharField(max_length=50, unique=True, blank=True)
    items = models.ManyToManyField(OrderItem)
    status = models.CharField(max_length=12, choices=REFUND_STATUS, default='Sent')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Refund - {} items".format(sum([i.quantity for i in self.items.all()]))

    def save(self, *args, **kwargs):
        if self.order_id == "" or self.order_id is None:
            code = generate_order_id()
            self.order_id = code
        if self.status == "Accepted":
            orders = [i.order for i in self.items.all()]
            completed_order = Order.objects.get(order_id=orders[0])
            completed_order.delete()
        super(Refund, self).save(*args, **kwargs)


class Download(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    
