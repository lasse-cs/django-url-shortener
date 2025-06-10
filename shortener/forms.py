from django import forms

from shortener.models import ShortenedURL


class ShortenedURLForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["original_url"].widget.attrs.update(
            {
                "placeholder": "Enter the URL to shorten",
            }
        )

    class Meta:
        model = ShortenedURL
        fields = [
            "original_url",
        ]
