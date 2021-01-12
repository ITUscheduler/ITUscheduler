from django.contrib import sitemaps
from django.urls import reverse


class IndexViewSitemap(sitemaps.Sitemap):
    priority = 1

    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.9

    def items(self):
        return ['courses', 'signup', 'login']

    def location(self, item):
        return reverse(item)
