from django.contrib.sitemaps import Sitemap
from .models import Product

class productSitmaps(Sitemap):
    protocol = 'https'
    def items(self):
        return Product.objects.all()