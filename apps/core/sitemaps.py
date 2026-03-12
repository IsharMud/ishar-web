"""Dynamic sitemap generation for isharmud.com."""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""
    protocol = "https"
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return [
            "index",
            "faq",
            "start",
            "history",
            "patches",
            "help",
            "clients",
            "support",
            "world",
            "connect",
            "events",
            "news",
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        priorities = {
            "index": 1.0,
            "connect": 0.9,
            "start": 0.9,
            "faq": 0.8,
            "help": 0.8,
            "clients": 0.8,
            "world": 0.7,
            "news": 0.7,
            "events": 0.7,
            "patches": 0.6,
            "history": 0.6,
            "support": 0.5,
        }
        return priorities.get(item, 0.5)

    def changefreq(self, item):
        frequencies = {
            "index": "daily",
            "news": "daily",
            "events": "daily",
            "patches": "weekly",
            "help": "weekly",
            "faq": "monthly",
            "start": "monthly",
            "clients": "monthly",
            "world": "monthly",
            "history": "yearly",
            "support": "yearly",
            "connect": "monthly",
        }
        return frequencies.get(item, "weekly")
