from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from shortener.forms import ShortenedURLForm
from shortener.models import ShortenedURL


def index(request):
    if request.method == "POST":
        form = ShortenedURLForm(request.POST)
        if form.is_valid():
            short_url = form.save()
            return redirect(short_url)
    else:
        form = ShortenedURLForm()
    context = {
        "form": form,
    }
    return render(request, "shortener/index.html", context)


def redirect_short_url(request, slug):
    short_url = cache.get(slug)
    if not short_url:
        short_url = get_object_or_404(ShortenedURL, slug=slug)
        cache.set(slug, short_url, timeout=60 * 60)
    return HttpResponseRedirect(short_url.original_url)


def detail_short_url(request, slug):
    short_url = get_object_or_404(ShortenedURL, slug=slug)
    context = {
        "short_url": short_url,
    }
    return render(request, "shortener/detail.html", context)
