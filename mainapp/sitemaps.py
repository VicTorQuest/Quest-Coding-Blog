from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitmap(Sitemap):
    priority = 0.7
    changefreq = "daily"
    protocol = 'https'
    def items(self):
        return [
            "home",
            "contact",
            "videos"
        ]

    def location(self, item):
        return reverse(item)
