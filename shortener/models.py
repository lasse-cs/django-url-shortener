from string import ascii_letters, digits
import random
from django.db import models
from django.urls import reverse
from tenacity import retry, stop_after_attempt


class ShortenedURL(models.Model):
    slug = models.SlugField(max_length=8, primary_key=True)
    original_url = models.URLField(max_length=2000, help_text="Original URL to shorten")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.slug} -> {self.original_url}"

    def get_absolute_url(self):
        return reverse("detail_short_url", args=(self.slug,))

    def get_redirect_url(self):
        return reverse("redirect_short_url", args=(self.slug,))

    def save(self, **kwargs):
        if self.slug:
            return super().save(**kwargs)
        else:
            self._save(**kwargs)

    @retry(reraise=True, stop=stop_after_attempt(3))
    def _save(self, **kwargs):
        self.slug = ShortenedURL.generate_random_slug()
        self.save(**kwargs)

    @staticmethod
    def generate_random_slug(length=8):
        characters = ascii_letters + digits
        return "".join(random.choices(characters, k=length))
