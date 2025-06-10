from django.urls import path
from shortener import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:slug>/", views.redirect_short_url, name="redirect_short_url"),
    path("<str:slug>/detail/", views.detail_short_url, name="detail_short_url"),
]
