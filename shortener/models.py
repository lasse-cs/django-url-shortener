from django.db import models


class ShortenedURL(models.Model):
    short_slug = models.SlugField(max_length=8, primary_key=True)
    original_url = models.URLField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.short_slug} -> {self.original_url}"
