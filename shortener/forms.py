from django import forms

from shortener.models import ShortenedURL


class ShortenedURLForm(forms.ModelForm):
    template_name = "shortener/forms/url.html"

    class Meta:
        model = ShortenedURL
        fields = [
            "original_url",
        ]
        widgets = {
            "original_url": forms.URLInput(
                attrs={
                    "placeholder": "Enter the URL to shorten",
                },
            ),
        }
