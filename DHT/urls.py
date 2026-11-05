from django.urls import path
from .api import Dlist, Dhtviews

urlpatterns = [
    path("list/", Dlist, name="dht-list"),
    path("post/", Dhtviews.as_view(), name="dht-create"),
]
