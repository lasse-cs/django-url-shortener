from django.db import IntegrityError
from django.urls import reverse
import pytest
from django.core.exceptions import ValidationError
from pytest_django.asserts import assertRedirects
from shortener.models import ShortenedURL
from unittest import mock


@pytest.fixture
def short_url():
    yield ShortenedURL.objects.create(
        slug="test1234", original_url="http://example.com"
    )


@pytest.mark.django_db
def test_unique_slugs(short_url):
    second_url = ShortenedURL(
        slug=short_url.slug, original_url="http://another-example.com"
    )
    with pytest.raises(ValidationError):
        second_url.full_clean()


@pytest.mark.django_db
def test_redirect_short_url(client, short_url):
    response = client.get(reverse("redirect_short_url", args=(short_url.slug,)))
    assertRedirects(
        response,
        short_url.original_url,
        status_code=302,
        fetch_redirect_response=False,
    )


@pytest.mark.django_db
def test_create_short_url(client):
    original_url = "http://example.com"
    data = {"original_url": original_url}
    response = client.post(reverse("index"), data)

    shortened_url = ShortenedURL.objects.get(original_url=original_url)

    assertRedirects(
        response,
        reverse("detail_short_url", args=(shortened_url.slug,)),
    )


@pytest.mark.django_db(transaction=True)
@mock.patch("shortener.models.ShortenedURL.generate_random_slug")
def test_attempts_save_multiple_times(mock_generate_slug, short_url):
    mock_generate_slug.return_value = short_url.slug
    new_url = ShortenedURL(original_url="http://new-example.com")
    with pytest.raises(IntegrityError):
        new_url.save()
    assert mock_generate_slug.call_count > 1
